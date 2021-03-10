#! /usr/bin/python3
from tkinter import ttk, Label, LabelFrame, Entry, StringVar, Tk, CENTER, W, E, END, Toplevel
from clienteCorporativo import ClienteCorporativo
from clienteParticular import ClienteParticular
from repositorioClientes import RepositorioClientes
from repositorioTrabajos import RepositorioTrabajos
from trabajo import Trabajo
from datetime import *

import sqlite3

class Product:

    nombre_bd = 'base_datos.sqlite'

    def __init__(self, window):
        self.wind = window
        self.wind.title('Sistema de gestion de trabajos')
        self.rc = RepositorioClientes()
        self.lista_clientes = self.rc.get_all_particulares()
        self.rt = RepositorioTrabajos()

        #Frame
        frame = LabelFrame(self.wind, text = 'Menu principal')
        frame.grid(row = 0, column = 0, columnspan = 8, pady = 20)

        # Botonera
        ttk.Button(frame, text = "Agregar cliente particular", command = self.add_clientspart_window).grid(row = 1 , column = 4, columnspan = 2, sticky = W + E)
        ttk.Button(frame, text = "Agregar cliente corporativo", command = self.add_clientscorp_window).grid(row = 2, column = 4 ,columnspan = 2, sticky = W + E)
        ttk.Button(frame, text = "Agregar un trabajo", command = self.add_works_window).grid(row = 3, column = 4, columnspan = 2, sticky = W + E)

        # Mensajes de salida
        self.message = Label(text = '', fg = 'red')
        self.message.grid(row = 8, column = 0, columnspan = 2, sticky = W + E)

        # Tabla
        self.tree = ttk.Treeview(height = 5, columns = ("#1","#2","#3",'#4'))
        self.tree.grid(row = 9, column = 0, columnspan = 6)

        self.tree.heading('#0', text = 'Nombre', anchor = CENTER)
        self.tree.heading('#1', text = 'Apellido', anchor = CENTER)
        self.tree.heading('#2', text = 'Teléfono', anchor = CENTER)
        self.tree.heading('#3', text = 'Mail', anchor = CENTER)
        self.tree.heading('#4', text = 'ID', anchor = CENTER)

        # Tabla clientes corporativos
        self.tree2 = ttk.Treeview(height = 5, columns = ("#1","#2","#3","#4",'#5'))
        self.tree2.grid(row = 11, column = 0, columnspan = 6)

        self.tree2.heading('#0', text = 'Nombre de la Empresa', anchor = CENTER)
        self.tree2.heading('#1', text = 'Nombre de Contacto', anchor = CENTER)
        self.tree2.heading('#2', text = 'Teléfono', anchor = CENTER)
        self.tree2.heading('#3', text = 'Teléfono de contacto', anchor = CENTER)
        self.tree2.heading('#4', text = 'Mail', anchor = CENTER)
        self.tree2.heading('#5', text = 'ID', anchor = CENTER)

        # Tabla trabajos
        self.tree3 = ttk.Treeview(height = 5, columns = ("#1","#2","#3","#4",'#5','#6'))
        self.tree3.grid(row = 13, column = 0, columnspan = 6)

        self.tree3.heading('#0', text = 'ID de trabajo', anchor = CENTER)
        self.tree3.heading('#1', text = 'Nombre de cliente', anchor = CENTER)
        self.tree3.heading('#2', text = 'Fecha de Ingreso', anchor = CENTER)
        self.tree3.heading('#3', text = 'Fecha de Entrega Propuesta', anchor = CENTER)
        self.tree3.heading('#4', text = 'Fecha de Entrega Real', anchor = CENTER)
        self.tree3.heading('#5', text = 'Descripción', anchor = CENTER)
        self.tree3.heading('#6', text = 'Entregado', anchor = CENTER)

        # Botonera 2
        ttk.Button(text = "Editar cliente particular", command = self.edit_clients_part_window).grid(row = 10, column = 1, columnspan = 2)
        ttk.Button(text = "Eliminar cliente particular", command = self.delete_clients_part).grid(row = 10, column = 3, columnspan = 2)

        ttk.Button(text = "Editar cliente corporativo", command = self.edit_clients_corp_window).grid(row = 12, column = 0, columnspan = 3)
        ttk.Button(text = "Eliminar cliente corporativo", command = self.delete_clients_corp).grid(row = 12, column = 3, columnspan = 3)
        
        ttk.Button(text = "Finalizar trabajo", command = self.trabajo_finalizado).grid(row = 14, column = 0, columnspan = 2)
        ttk.Button(text = "Entregar el trabajo", command = self.trabajo_entregado).grid(row = 14, column = 1, columnspan = 2)
        ttk.Button(text = "Modificar datos del trabajo", command = self.edit_trabajos_window).grid(row = 14, column = 2, columnspan = 2)
        ttk.Button(text = "Cancelar trabajo", command = self.eliminar_trabajo_confirmacion).grid(row = 14, column = 3, columnspan = 2)
        ttk.Button(text = "Informe de trabajos pendientes", command = self.informe).grid(row = 14, column = 4, columnspan = 2)
        
        self.get_clients()
        self.get_works()

    def run_query (self, query, parameters = ()):
        with sqlite3.connect(self.nombre_bd) as Conectar:
            cursor = Conectar.cursor()
            resultado = cursor.execute(query, parameters)
            Conectar.commit()
        return resultado
     
    def get_clients(self, lista = None):
        # Limpio la tabla antes de arrancar la query
        records = self.tree.get_children()
        records2 = self.tree2.get_children()
        for element in records:
            self.tree.delete(element)
        for element2 in records2:
            self.tree2.delete(element2)
        
        # Muestro clientes
        query = 'SELECT * FROM cliente JOIN cliente_particular ON cliente.id=cliente_particular.id_cliente ORDER BY id ASC'
        query1 = 'SELECT * FROM cliente JOIN cliente_corporativo ON cliente.id=cliente_corporativo.id_cliente ORDER BY id ASC'
        db_rows = self.run_query(query)
        db_rows1 = self.run_query(query1)
        #Particulares       
        for row in db_rows:
            self.tree.insert('', 0, text = (row[4]), values = (row[5],row[1], row[2],row[3]))
        #Corporativos
        for fila in db_rows1:
            self.tree2.insert('', 0, text = (fila[4]), values = (fila[5], fila[1], fila[6],fila[2],fila[3]))
    
    def get_works(self, lista = None):
        # Limpio la tabla antes de arrancar la query
        registros = self.tree3.get_children()
        for element3 in registros:
            self.tree3.delete(element3)
        
        # Muestro los trabajos
        query = 'SELECT trabajos.id_cliente, trabajos.fecha_ingreso, trabajos.fecha_entrega_propuesta, cliente.id,\
             trabajos.fecha_entrega_real, trabajos.descripcion, trabajos.retirado, trabajos.id, \
                 cliente_corporativo.nombre_contacto \
                     FROM trabajos \
                         JOIN cliente ON trabajos.id_cliente = cliente.id \
                             JOIN cliente_corporativo ON cliente.id = cliente_corporativo.id_cliente'
        query2 = 'SELECT trabajos.id_cliente, trabajos.fecha_ingreso, trabajos.fecha_entrega_propuesta, cliente.id,\
             trabajos.fecha_entrega_real, trabajos.descripcion, trabajos.retirado, trabajos.id, \
                 cliente_particular.nombre,cliente_particular.apellido \
                     FROM trabajos \
                         JOIN cliente ON trabajos.id_cliente = cliente.id \
                             JOIN cliente_particular ON cliente.id = cliente_particular.id_cliente'
        filas_db = self.run_query(query)
        filas2_db = self.run_query(query2)
        for filas in filas_db:
            self.tree3.insert('', 0, text = (filas[7]), values = (filas[8],filas[1], filas[2],filas[4], filas[5],filas[6]))
        for filas2 in filas2_db:
            self.tree3.insert('', 0, text = (filas2[7]), values = (filas2[8]+' '+filas2[9],filas2[1], filas2[2],filas2[4], filas2[5],filas2[6]))

    def validations_particular(self):
        '''Valida que no haya espacios en blanco'''
        return  len(self.name.get()) !=0 and len(self.surname.get()) !=0 and len(self.phone.get()) !=0 and len(self.mail.get()) !=0

    def validations_corporativo(self):
        '''Valida que no haya espacios en blanco'''
        return  len(self.company_name.get()) !=0 and len(self.contact_name.get()) !=0 and len(self.contact_phone.get()) !=0 and len(self.phone.get()) !=0 and len(self.mail.get()) !=0

    def add_clientspart_window(self):

        self.add_window_part = Toplevel()
        self.add_window_part.title = 'Agregar cliente'

        # Input Nombre
        Label(self.add_window_part, text = 'Nombre: ').grid(row = 1, column = 0)
        Entry(self.add_window_part, textvariable = StringVar(self.add_window_part), state = 'readonly')
        self.name = Entry(self.add_window_part)
        self.name.focus()
        self.name.grid(row = 1, column = 1)

        # Input Apellido
        Label(self.add_window_part, text = 'Apellido: ').grid(row = 2, column = 0)
        Entry(self.add_window_part)
        self.surname = Entry(self.add_window_part)
        self.surname.grid(row = 2, column = 1)

        # Input Telefono
        Label(self.add_window_part, text = 'Telefono: ').grid(row = 3, column = 0)
        Entry(self.add_window_part)
        self.phone = Entry(self.add_window_part)
        self.phone.grid(row = 3, column = 1)

        # Input Mail
        Label(self.add_window_part, text = 'Mail: ').grid(row = 4, column = 0)
        Entry(self.add_window_part)
        self.mail = Entry(self.add_window_part)
        self.mail.grid(row = 4, column = 1)
        
        # Botonera
        ttk.Button(self.add_window_part, text = "Guardar", command = self.add_client_particular).grid(row = 5, columnspan = 2, sticky = W + E)

    def add_clientscorp_window(self):

        self.add_window_corp = Toplevel()
        self.add_window_corp.title = 'Agregar cliente corporativo'

        # Input Nombre Empresa
        Label(self.add_window_corp, text = 'Nombre Empresa: ').grid(row = 1, column = 0)
        Entry(self.add_window_corp, textvariable = StringVar(self.add_window_corp), state = 'readonly')
        self.company_name = Entry(self.add_window_corp)
        self.company_name.focus()
        self.company_name.grid(row = 1, column = 1)

        # Input Nombre Contacto
        Label(self.add_window_corp, text = 'Nombre Contacto: ').grid(row = 2, column = 0)
        Entry(self.add_window_corp)
        self.contact_name = Entry(self.add_window_corp)
        self.contact_name.grid(row = 2, column = 1)

        # Input Telefono
        Label(self.add_window_corp, text = 'Telefono: ').grid(row = 3, column = 0)
        Entry(self.add_window_corp)
        self.phone = Entry(self.add_window_corp)
        self.phone.grid(row = 3, column = 1)

        # Input Telefono de Contacto
        Label(self.add_window_corp, text = 'Telefono de contacto: ').grid(row = 4, column = 0)
        Entry(self.add_window_corp)
        self.contact_phone = Entry(self.add_window_corp)
        self.contact_phone.grid(row = 4, column = 1)

        # Input Mail
        Label(self.add_window_corp, text = 'Mail: ').grid(row = 5, column = 0)
        Entry(self.add_window_corp)
        self.mail = Entry(self.add_window_corp)
        self.mail.grid(row = 5, column = 1)
        
        # Botonera
        ttk.Button(self.add_window_corp, text = "Guardar", command = self.add_client_corporativo).grid(row = 6, columnspan = 2, sticky = W + E)

    def add_client_particular(self):
            #si las validaciones son correctas
            if self.validations_particular():
                parameters = ClienteParticular(self.name.get(), self.surname.get(), self.phone.get(), self.mail.get())
                parameters.id_cliente = self.rc.store(parameters)
                self.lista_clientes.append(parameters)
                self.message['text'] = 'El cliente personal {0} {1} ha sido añadido correctamente'.format(self.name.get(), self.surname.get())
                self.name.delete(0, END)
                self.surname.delete(0, END)
                self.phone.delete(0, END)
                self.mail.delete(0, END)
                self.get_clients()
                return parameters
            else:
                self.message['text'] = 'Nombre, Apellido, Teléfono y Mail son requeridos'

    def add_client_corporativo(self):
            #si las validaciones son correctas
            if self.validations_corporativo():
                parameters = ClienteCorporativo(self.company_name.get(), self.contact_name.get(), self.contact_phone.get(), self.phone.get() ,self.mail.get())
                parameters.id_cliente = self.rc.store(parameters)
                self.lista_clientes.append(parameters)
                self.message['text'] = 'El cliente corporativo {0} de la empresa {1} ha sido añadido correctamente'.format(self.contact_name.get(), self.company_name.get())
                self.company_name.delete(0, END)
                self.contact_name.delete(0, END)
                self.contact_phone.delete(0, END)
                self.phone.delete(0, END)
                self.mail.delete(0, END)
                self.get_clients()
                return parameters
            else:
                self.message['text'] = 'Nombre, Apellido, Teléfono y Mail son requeridos'

    def edit_clients_part_window(self):
        '''Ventana para editar un cliente particular'''
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['text'][0]
        except IndexError:
            self.message['text'] = 'Por favor, seleccione un registro'
            return
        old_name = self.tree.item(self.tree.selection())['text']
        old_surname = self.tree.item(self.tree.selection())['values'][0]
        old_phone = self.tree.item(self.tree.selection())['values'][1]
        old_mail = self.tree.item(self.tree.selection())['values'][2]
        id_cliente1 = self.tree.item(self.tree.selection())['values'][3]
        self.edit_window = Toplevel()
        self.edit_window.title = 'Editar cliente'

        # ID
        Label(self.edit_window, text = 'ID: ').grid(row = 1, column = 1)
        Entry(self.edit_window, textvariable = StringVar(self.edit_window, value = id_cliente1), state = 'readonly').grid(row = 1, column = 2)

        # Nombre Anterior
        Label(self.edit_window, text = 'Nombre anterior: ').grid(row = 2, column = 1)
        Entry(self.edit_window, textvariable = StringVar(self.edit_window, value = old_name), state = 'readonly').grid(row = 2, column = 2)

        # Nombre Actual
        Label(self.edit_window, text = 'Nombre actual: ').grid(row = 3, column = 1)
        new_name = Entry(self.edit_window)
        new_name.grid(row = 3, column = 2)

        # Apellido Anterior
        Label(self.edit_window, text = 'Apellido Anterior: ').grid(row = 4, column = 1)
        Entry(self.edit_window, textvariable = StringVar(self.edit_window, value = old_surname), state = 'readonly').grid(row = 4, column = 2)

        # Nuevo Apellido
        Label(self.edit_window, text = 'Apellido Actual: ').grid(row = 5, column = 1)
        new_surname = Entry(self.edit_window)
        new_surname.grid(row = 5, column = 2)

        # Telefono Anterior
        Label(self.edit_window, text = 'Telefono Anterior: ').grid(row = 6, column = 1)
        Entry(self.edit_window, textvariable = StringVar(self.edit_window, value = old_phone), state = 'readonly').grid(row = 6, column = 2)

        # Nuevo Telefono
        Label(self.edit_window, text = 'Telefono Actual: ').grid(row = 7, column = 1)
        new_phone = Entry(self.edit_window)
        new_phone.grid(row = 7, column = 2)

        # Mail anterior
        Label(self.edit_window, text = 'Mail Anterior: ').grid(row = 8, column = 1)
        Entry(self.edit_window, textvariable = StringVar(self.edit_window, value = old_mail), state = 'readonly').grid(row = 8, column = 2)

        # Nuevo mail
        Label(self.edit_window, text = 'Mail Actual: ').grid(row = 9, column = 1)
        new_mail = Entry(self.edit_window)
        new_mail.grid(row = 9, column = 2)

        # Botón de guardar cambios
        ttk.Button(self.edit_window, text = 'Actualizar', command = lambda: self.edit_clients_part(new_name.get(),new_surname.get(),new_phone.get(),new_mail.get(),id_cliente1)).grid(row = 10, columnspan = 3, sticky = W + E)
    
    def edit_clients_part(self, new_name, new_surname, new_phone, new_mail, id_cliente):
        '''Editar un cliente particular'''
        parameters = ClienteParticular(new_name,new_surname,new_phone,new_mail , id_cliente)
        self.rc.update(parameters)
        self.edit_window.destroy()
        self.message['text'] = 'El cliente {0} {1} sido editado correctamente'.format(new_name, new_surname)
        self.get_clients()
    
    def edit_clients_corp_window(self):
        '''Ventana para editar un cliente corporativo'''
        self.message['text'] = ''
        try:
            self.tree2.item(self.tree2.selection())['text'][0]
        except IndexError:
            self.message['text'] = 'Por favor, seleccione un registro'
            return
        old_company_name = self.tree2.item(self.tree2.selection())['text']
        old_contact_name = self.tree2.item(self.tree2.selection())['values'][0]
        old_contact_phone = self.tree2.item(self.tree2.selection())['values'][1]
        old_phone = self.tree2.item(self.tree2.selection())['values'][2]
        old_mail = self.tree2.item(self.tree2.selection())['values'][3]
        id_cliente = self.tree2.item(self.tree2.selection())['values'][4]
        self.edit_window2 = Toplevel()
        self.edit_window2.title = 'Editar cliente'

        # ID
        Label(self.edit_window2, text = 'ID: ').grid(row = 0, column = 1)
        Entry(self.edit_window2, textvariable = StringVar(self.edit_window2, value = id_cliente), state = 'readonly').grid(row = 0, column = 2)

        # Nombre de la empresa Anterior
        Label(self.edit_window2, text = 'Nombre de la empresa anterior: ').grid(row = 1, column = 1)
        Entry(self.edit_window2, textvariable = StringVar(self.edit_window2, value = old_company_name), state = 'readonly').grid(row = 1, column = 2)

        # Nombre de la empresa Actual
        Label(self.edit_window2, text = 'Nombre de la empresa actual: ').grid(row = 2, column = 1)
        new_company_name = Entry(self.edit_window2)
        new_company_name.grid(row = 2, column = 2)

        # Nombre de contacto Anterior
        Label(self.edit_window2, text = 'Nombre de contacto anterior: ').grid(row = 3, column = 1)
        Entry(self.edit_window2, textvariable = StringVar(self.edit_window2, value = old_contact_name), state = 'readonly').grid(row = 3, column = 2)

        # Nombre de contacto Actual
        Label(self.edit_window2, text = 'Nombre de contacto actual: ').grid(row = 4, column = 1)
        new_contact_name = Entry(self.edit_window2)
        new_contact_name.grid(row = 4, column = 2)

        # Telefono Anterior
        Label(self.edit_window2, text = 'Telefono Anterior: ').grid(row = 5, column = 1)
        Entry(self.edit_window2, textvariable = StringVar(self.edit_window2, value = old_phone), state = 'readonly').grid(row = 5, column = 2)

        # Nuevo Telefono
        Label(self.edit_window2, text = 'Telefono Actual: ').grid(row = 6, column = 1)
        new_phone = Entry(self.edit_window2)
        new_phone.grid(row = 6, column = 2)

        # Telefono de contacto Anterior
        Label(self.edit_window2, text = 'Telefono de contacto anterior: ').grid(row = 7, column = 1)
        Entry(self.edit_window2, textvariable = StringVar(self.edit_window2, value = old_contact_phone), state = 'readonly').grid(row = 7, column = 2)

        # Telefono de contacto actual
        Label(self.edit_window2, text = 'Telefono de contacto actual: ').grid(row = 8, column = 1)
        new_contact_phone = Entry(self.edit_window2)
        new_contact_phone.grid(row = 8, column = 2)

        # Mail Anterior
        Label(self.edit_window2, text = 'Mail anterior: ').grid(row = 9, column = 1)
        Entry(self.edit_window2, textvariable = StringVar(self.edit_window2, value = old_mail), state = 'readonly').grid(row = 9, column = 2)

        # Mail actual
        Label(self.edit_window2, text = 'Mail actual: ').grid(row = 10, column = 1)
        new_mail = Entry(self.edit_window2)
        new_mail.grid(row = 10, column = 2)

        # Botón de guardar cambios
        ttk.Button(self.edit_window2, text = 'Actualizar', command = lambda: self.edit_clients_corp(new_company_name.get(),new_contact_name.get(),new_contact_phone.get(), new_phone.get(), new_mail.get(), id_cliente)).grid(row = 11, columnspan = 3, sticky = W + E)

    def edit_clients_corp(self, new_company_name, new_contact_name, new_contact_phone, new_phone, new_mail, id_cliente):
        '''Editar un cliente corporativo'''
        parameters = ClienteCorporativo(new_company_name,new_contact_name,new_contact_phone,new_phone,new_mail,id_cliente)
        self.rc.update(parameters)
        self.edit_window2.destroy()
        self.message['text'] = 'El cliente {0} de la empresa {1} ha sido editado correctamente'.format(new_contact_name, new_company_name)
        self.get_clients()

    def delete_clients_part(self):
        '''Eliminar a un cliente particular'''
        name = self.tree.item(self.tree.selection())['text']
        surname = self.tree.item(self.tree.selection())['values'][0]
        phone = self.tree.item(self.tree.selection())['values'][1]
        mail = self.tree.item(self.tree.selection())['values'][2]
        id_cliente1 = self.tree.item(self.tree.selection())['values'][3]
        try:
            self.tree.item(self.tree.selection())['text']
        except IndexError:
            self.message['text'] = 'Seleccione a un cliente'
        name = self.tree.item(self.tree.selection())['text']
        parameters = ClienteParticular(name,surname,phone,mail,id_cliente1)
        self.rc.delete(parameters)
        self.message['text'] = 'El cliente {0} {1} sido editado correctamente'.format(name, surname)
        self.get_clients()

    def delete_clients_corp(self):
       '''Eliminar a un cliente corporativo'''
       company_name = self.tree2.item(self.tree2.selection())['text']
       contact_name = self.tree2.item(self.tree2.selection())['values'][0]
       contact_phone = self.tree2.item(self.tree2.selection())['values'][1]
       phone = self.tree2.item(self.tree2.selection())['values'][2]
       mail = self.tree2.item(self.tree2.selection())['values'][3]
       id_cliente1 = self.tree2.item(self.tree2.selection())['values'][4]
       try:
           self.tree.item(self.tree2.selection())['text']
       except IndexError:
           self.message['text'] = 'Seleccione a un cliente'
       parameters = ClienteCorporativo(company_name,contact_name,contact_phone,phone,mail,id_cliente1)
       self.rc.delete(parameters)
       self.message['text'] = 'El cliente {0} de la empresa {1} sido eliminado correctamente'.format(contact_name, company_name)
       self.get_clients()

    def add_works_window(self):

        self.add_window_work = Toplevel()
        self.add_window_work.title = 'Agregar trabajo'
        
        # Input ID
        
        Label(self.add_window_work, text = 'ID del cliente: ').grid(row = 1, column = 0)
        self.id_cliente_entry = Entry(self.add_window_work)
        self.id_cliente_entry.focus()
        self.id_cliente_entry.grid(row = 1, column = 1)

        # Input Fecha de Ingreso
        Label(self.add_window_work, text = 'Fecha de Ingreso: ').grid(row = 2, column = 0)
        self.entry_date = Entry(self.add_window_work)
        self.entry_date.grid(row = 2, column = 1)

        # Input Fecha de Entrega Propuesta
        Label(self.add_window_work, text = 'Fecha de Entrega Propuesta: ').grid(row = 3, column = 0)
        self.proposal_delivery_date = Entry(self.add_window_work)
        self.proposal_delivery_date.grid(row = 3, column = 1)
      
        # Input Descripcion
        Label(self.add_window_work, text = 'Descripcion: ').grid(row = 5, column = 0)
        self.description = Entry(self.add_window_work)
        self.description.grid(row = 5, column = 1)

        # Botonera
        ttk.Button(self.add_window_work, text = "Guardar", command = self.add_work).grid(row = 7, columnspan = 2, sticky = W + E)

    def validations_work(self):
        #'''Valida que no haya espacios en blanco'''
        return  len(self.id_cliente_entry.get())

    def add_work(self):
        #si las validaciones son correctass
        if self.validations_work():
            self.message['text'] = ''
            obj_cliente = None
            obj_cliente = self.rc.get_one(self.id_cliente_entry.get())
            fe_entrada = datetime.strptime(self.entry_date.get(), '%d-%m-%Y')
            fe_entrada.strftime('%Y-%m-%d')
            fecha_ent_pro = ''
            
            # En caso de que la fecha propuesta esté en blanco, asignar None
            if fecha_ent_pro != '':
                fecha_ent_pro = datetime.strptime(self.proposal_delivery_date.get(), '%d-%m-%Y')
                fecha_ent_pro.strftime('%Y-%m-%d')
            else:
                fecha_ent_pro = None

            parameters = Trabajo(obj_cliente, fe_entrada, fecha_ent_pro, None, self.description.get(), False, None)
            a = self.rt.store(parameters)
            print(parameters,a)
            if a:
                self.message['text'] = 'El trabajo del cliente {0} ha sido añadido correctamente'.format(self.id_cliente_entry.get())
                self.get_works()
                self.id_cliente_entry.delete(0, END)
                self.entry_date.delete(0, END)
                self.proposal_delivery_date.delete(0, END)
                self.description.delete(0, END)
            else:
                self.message['text'] = 'El trabajo del cliente no se ha sido añadido. Código de error: 0'
                print (fecha_ent_pro)
        
        else:
            self.message['text'] = 'Todos los campos son requeridos'

    def retirado(self):
       '''Se cambia su estado de retirado a True'''
       try:
           self.tree3.item(self.tree3.selection())['text']
       except IndexError:
           self.message['text'] = 'Seleccione un trabajo'
       
       self.message['text'] = 'El trabajo ha sido entregado correctamente'
       self.get_works()

    def edit_trabajos_window(self):
        '''Ventana para editar un trabajo'''
        self.message['text'] = ''
        try:
            self.tree3.item(self.tree3.selection())['values'][0]
        except IndexError:
            self.message['text'] = 'Por favor, seleccione un registro'
            return
        old_description = self.tree3.item(self.tree3.selection())['values'][4]
        old_entry_date = self.tree3.item(self.tree3.selection())['values'][1]
        id_cliente = self.tree3.item(self.tree3.selection())['values'][0]
        proposal_delivery_date = self.tree3.item(self.tree3.selection())['values'][2]
        real_delivery_date = self.tree3.item(self.tree3.selection())['values'][3]
        withdrawn = self.tree3.item(self.tree3.selection())['values'][5]
        id_trabajo = self.tree3.item(self.tree3.selection())['text']
        self.edit_work_window = Toplevel()
        self.edit_work_window.title = 'Editar trabajo'

        # ID
        Label(self.edit_work_window, text = 'ID: ').grid(row = 1, column = 1)
        Entry(self.edit_work_window, textvariable = StringVar(self.edit_work_window, value = id_trabajo), state = 'readonly').grid(row = 1, column = 2)

        # Descripcion Anterior
        Label(self.edit_work_window, text = 'Descripcion anterior: ').grid(row = 2, column = 1)
        Entry(self.edit_work_window, textvariable = StringVar(self.edit_work_window, value = old_description), state = 'readonly').grid(row = 2, column = 2)

        # Descripcion Actual
        Label(self.edit_work_window, text = 'Descripcion actual: ').grid(row = 3, column = 1)
        new_description = Entry(self.edit_work_window)
        new_description.grid(row = 3, column = 2)

        # Fecha de Ingreso Anterior
        Label(self.edit_work_window, text = 'Fecha de ingreso anterior: ').grid(row = 4, column = 1)
        Entry(self.edit_work_window, textvariable = StringVar(self.edit_work_window, value = old_entry_date), state = 'readonly').grid(row = 4, column = 2)

        # Fecha de Ingreso Actual
        Label(self.edit_work_window, text = 'Fecha de ingreso actual: ').grid(row = 5, column = 1)
        new_entry_date = Entry(self.edit_work_window)
        new_entry_date.grid(row = 5, column = 2)

        # Botón de guardar cambios
        ttk.Button(self.edit_work_window, text = 'Actualizar', command = lambda: self.edit_works_desc(id_cliente,new_entry_date.get(), proposal_delivery_date, real_delivery_date,new_description.get(),withdrawn,id_trabajo)).grid(row = 6, columnspan = 3, sticky = W + E)

    def edit_works_desc(self, id_cliente, new_entry_date, proposal_delivery_date, real_delivery_date, new_description,withdrawn, id_trabajo):
        '''Editar descripcion y fecha de ingreso'''
        nueva_fecha = datetime.strptime(new_entry_date, '%d-%m-%Y')
        nueva_fecha.strftime('%Y-%m-%d')
        fecha_ent_pro = datetime.strptime(proposal_delivery_date, '%Y-%m-%d')
        fecha_ent_pro.strftime('%Y-%m-%d')
        fecha_ent_re = datetime.strptime(real_delivery_date, '%Y-%m-%d')
        fecha_ent_re.strftime('%Y-%m-%d')
        print(nueva_fecha)
        parameters = Trabajo(id_cliente,nueva_fecha,fecha_ent_pro,fecha_ent_re,new_description,withdrawn, id_trabajo)
        print (parameters)
        a = self.rt.update(parameters)
        if a:
            self.edit_work_window.destroy()
            self.message['text'] = 'El trabajo sido editado correctamente'
        else:
            self.message['text'] = 'El trabajo no ha sido editado'
        self.get_works()

    def trabajo_finalizado(self):
        '''Cambiar el estado a finalizado, modificando su fecha de entrega real a hoy'''
        # Obtengo la fecha de hoy
        hoy = date.today()
        hoy.strftime('%d, %m, %Y')

        # Obtengo los datos actuales del objeto en cuestión
        description = self.tree3.item(self.tree3.selection())['values'][4]
        entry_date = self.tree3.item(self.tree3.selection())['values'][1]
        id_cliente = self.tree3.item(self.tree3.selection())['values'][0]
        proposal_delivery_date = self.tree3.item(self.tree3.selection())['values'][2]
        #old_real_delivery_date = self.tree3.item(self.tree3.selection())['values'][3]
        withdrawn = self.tree3.item(self.tree3.selection())['values'][5]
        id_trabajo = self.tree3.item(self.tree3.selection())['text']

        # Formateo las fechas
        nueva_fecha = datetime.strptime(entry_date, '%Y-%m-%d')
        nueva_fecha.strftime('%Y-%m-%d')
        fecha_ent_pro = datetime.strptime(proposal_delivery_date, '%Y-%m-%d')
        fecha_ent_pro.strftime('%Y-%m-%d')

        # Paso parametros al obj Trabajo
        parameters = Trabajo(id_cliente,nueva_fecha,fecha_ent_pro,hoy,description,withdrawn, id_trabajo)
        print (parameters)
        a = self.rt.update(parameters)
        if a:
            self.message['text'] = 'El trabajo sido editado correctamente'
        else:
            self.message['text'] = 'El trabajo no ha sido editado'
        self.get_works()

    def trabajo_entregado(self):
        '''Cambiar el estado a entregado'''

        # Obtengo los datos actuales del objeto en cuestión
        description = self.tree3.item(self.tree3.selection())['values'][4]
        entry_date = self.tree3.item(self.tree3.selection())['values'][1]
        id_cliente = self.tree3.item(self.tree3.selection())['values'][0]
        proposal_delivery_date = self.tree3.item(self.tree3.selection())['values'][2]
        real_delivery_date = self.tree3.item(self.tree3.selection())['values'][3]
        #withdrawn = self.tree3.item(self.tree3.selection())['values'][5]
        id_trabajo = self.tree3.item(self.tree3.selection())['text']

        # Formateo las fechas
        nueva_fecha = datetime.strptime(entry_date, '%Y-%m-%d')
        nueva_fecha.strftime('%Y-%m-%d')
        fecha_ent_pro = datetime.strptime(proposal_delivery_date, '%Y-%m-%d')
        fecha_ent_pro.strftime('%Y-%m-%d')
        fecha_ent_real = datetime.strptime(real_delivery_date, '%Y-%m-%d')
        fecha_ent_real.strftime('%Y-%m-%d')

        withdrawn = True

        # Paso parametros al obj Trabajo
        parameters = Trabajo(id_cliente,nueva_fecha,fecha_ent_pro,fecha_ent_real,description,withdrawn, id_trabajo)
        print (parameters)
        a = self.rt.update(parameters)
        if a:
            self.message['text'] = 'El trabajo {0} sido entregado correctamente'.format(id_trabajo)
        else:
            self.message['text'] = 'El trabajo no ha sido editado'
        self.get_works()

    def eliminar_trabajo_confirmacion(self):
        '''ventana para confirmar la eliminación de los trabajos'''      
        # Creo ventana
        self.delete_work_window = Toplevel()
        self.delete_work_window.title = 'Eliminar trabajo'
        
        # Label
        label = Label(self.delete_work_window, text = '¿Está seguro que desea eliminar el trabajo?')
        label.grid(row = 1, column = 0)

        # Botón de Confirmar
        ttk.Button(self.delete_work_window, text = 'Sí, eliminar', command = lambda: self.eliminar_trabajo()).grid(row = 2, column = 0)
        # Botón Cancelar
        ttk.Button(self.delete_work_window, text = 'NO, cancelar', command = lambda: self.delete_work_window.destroy()).grid(row = 3, column = 0)

    def eliminar_trabajo(self):
        '''Eliminar un trabajo de la BD'''

        # Obtengo los datos actuales del objeto en cuestión
        description = self.tree3.item(self.tree3.selection())['values'][4]
        entry_date = self.tree3.item(self.tree3.selection())['values'][1]
        id_cliente = self.tree3.item(self.tree3.selection())['values'][0]
        proposal_delivery_date = self.tree3.item(self.tree3.selection())['values'][2]
        real_delivery_date = self.tree3.item(self.tree3.selection())['values'][3]
        withdrawn = self.tree3.item(self.tree3.selection())['values'][5]
        id_trabajo = self.tree3.item(self.tree3.selection())['text']

        # Paso parametros al obj Trabajo
        parameters = Trabajo(id_cliente,entry_date,proposal_delivery_date,real_delivery_date,description,withdrawn, id_trabajo)
        a = self.rt.delete(parameters)
        
        # Códigos de éxito o error y retorno la lista de trabajos actualizados
        if a:
            self.message['text'] = 'El trabajo {0} sido eliminado correctamente'.format(id_trabajo)
        else:
            self.message['text'] = 'El trabajo no ha sido eliminado'
        self.get_works()

    def informe(self):

        # Creo ventana
        self.informe_trabajos_window = Toplevel()
        self.informe_trabajos_window.title = 'Informe'

        # Obtengo la fecha de hoy
        hoy = date.today()
        hoyhoy = hoy.strftime('%Y-%m-%d')

        # Traigo todos los parámetros para comparar la fecha y la entrega
        trabajos_deben = []
        clientes_deben = []
        trabajos_no_deben = []
        clientes_no_deben = []
        fecha_propuesta = []

        trabajos_realmente_deben = []

        for Parent in self.tree3.get_children():
            entregado = self.tree3.item(Parent)["values"][5]
            id_cliente = self.tree3.item(Parent)['text']
            fecha_entrega_propuesta = self.tree3.item(Parent)['values'][3]
            if entregado == 0:
                trabajos_deben.append(entregado)
                clientes_deben.append(id_cliente)
                fecha_propuesta.append(fecha_entrega_propuesta)
            else:
                trabajos_no_deben.append(entregado)
                clientes_no_deben.append(id_cliente)
        
        #print (fecha_propuesta)
        cant_trabajos = len(trabajos_deben)

        for i in fecha_propuesta:
            if i <= hoyhoy:
                trabajos_realmente_deben.append (i)

        print ("Al dia de hoy",hoyhoy,"faltan entregar",cant_trabajos, "trabajos")
        # Label
        label = Label(self.informe_trabajos_window, text = 'Informes')
        label.grid(row = 1, column = 0)

        label2 = Label(self.informe_trabajos_window, text = "El informe sale por consola")
        label2.grid(row = 1, column = 0)

        # Botón Cierre
        ttk.Button(self.informe_trabajos_window, text = 'Cerrar', command = lambda: self.informe_trabajos_window.destroy()).grid(row = 2, column = 0)    

if __name__ == '__main__':
    window = Tk()
    application = Product(window)
    window.mainloop()