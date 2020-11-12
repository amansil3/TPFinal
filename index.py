#! /usr/bin/python3
from tkinter import ttk, Label, LabelFrame, Entry, StringVar, Tk, CENTER, W, E, END, Toplevel
from clienteCorporativo import ClienteCorporativo
from clienteParticular import ClienteParticular
from repositorioClientes import RepositorioClientes


import sqlite3

class Product:

    nombre_bd = 'base_datos.sqlite'

    def __init__(self, window):
        self.wind = window
        self.wind.title('Listado de Clientes')
        self.rc = RepositorioClientes()
        self.lista_clientes = self.rc.get_all_particulares()

        #Frame
        frame = LabelFrame(self.wind, text = 'Registrar un nuevo cliente')
        frame.grid(row = 0, column = 0, columnspan = 3, pady = 20)

        # Botonera
        ttk.Button(frame, text = "Agregar cliente particular", command = self.add_clientspart_window).grid(row = 5, columnspan = 2, sticky = W + E)
        ttk.Button(frame, text = "Agregar cliente corporativo", command = self.add_clientscorp_window).grid(row = 6, columnspan = 2, sticky = W + E)
        ttk.Button(frame, text = "Editar cliente", command = self.edit_clients_window).grid(row = 7, columnspan = 2, sticky = W + E)

        # Mensajes de salida
        self.message = Label(text = '', fg = 'red')
        self.message.grid(row = 8, column = 0, columnspan = 2, sticky = W + E)

        # Tabla
        self.tree = ttk.Treeview(height = 10, columns = ("#1","#2","#3"))
        self.tree.grid(row = 9, column = 0, columnspan = 5)

        self.tree.heading('#0', text = 'Nombre', anchor = CENTER)
        self.tree.heading('#1', text = 'Apellido', anchor = CENTER)
        self.tree.heading('#2', text = 'Teléfono', anchor = CENTER)
        self.tree.heading('#3', text = 'Mail', anchor = CENTER)

        #SubTabla
        self.tree2 = ttk.Treeview(height = 10, columns = ("#1","#2","#3","#4"))
        self.tree2.grid(row = 11, column = 0, columnspan = 5)

        self.tree2.heading('#0', text = 'Nombre de la Empresa', anchor = CENTER)
        self.tree2.heading('#1', text = 'Nombre de Contacto', anchor = CENTER)
        self.tree2.heading('#2', text = 'Teléfono', anchor = CENTER)
        self.tree2.heading('#3', text = 'Teléfono de contacto', anchor = CENTER)
        self.tree2.heading('#4', text = 'Mail', anchor = CENTER)

        self.get_clients()

    def run_query (self, query, parameters = ()):
        with sqlite3.connect(self.nombre_bd) as Conectar:
            cursor = Conectar.cursor()
            resultado = cursor.execute(query, parameters)
            Conectar.commit()
        return resultado
     
    def get_clients(self, lista = None):
        # Limpio la tabla antes de arrancar la query
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        
        # Muestro clientes
        query = 'SELECT * FROM cliente JOIN cliente_particular ON cliente.id=cliente_particular.id_cliente ORDER BY id ASC'
        query1 = 'SELECT * FROM cliente JOIN cliente_corporativo ON cliente.id=cliente_corporativo.id_cliente ORDER BY id ASC'
        db_rows = self.run_query(query)
        db_rows1 = self.run_query(query1)        
        for row in db_rows:
            self.tree.insert('', 0, text = (row[4]), values = (row[5], row[1],row [2]))
        for fila in db_rows1:
            self.tree2.insert('', 0, text = (fila[4]), values = (fila[5], fila[1], fila[6],fila[2]))
    
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

    def edit_clients_window(self):
        '''Editar un cliente'''
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
        self.edit_window = Toplevel()
        self.edit_window.title = 'Editar cliente'

        # Nombre Anterior
        Label(self.edit_window, text = 'Nombre anterior: ').grid(row = 0, column = 1)
        Entry(self.edit_window, textvariable = StringVar(self.edit_window, value = old_name), state = 'readonly').grid(row = 0, column = 2)

        # Nombre Actual
        Label(self.edit_window, text = 'Nombre actual: ').grid(row = 1, column = 1)
        Entry(self.edit_window).grid(row = 1, column = 2)

        # Apellido Anterior
        Label(self.edit_window, text = 'Apellido Anterior: ').grid(row = 2, column = 1)
        Entry(self.edit_window, textvariable = StringVar(self.edit_window, value = old_surname), state = 'readonly').grid(row = 2, column = 2)

        # Nuevo Apellido
        Label(self.edit_window, text = 'Apellido Actual: ').grid(row = 3, column = 1)
        Entry(self.edit_window).grid(row = 3, column = 2)

        # Telefono Anterior
        Label(self.edit_window, text = 'Telefono Anterior: ').grid(row = 4, column = 1)
        Entry(self.edit_window, textvariable = StringVar(self.edit_window, value = old_phone), state = 'readonly').grid(row = 4, column = 2)

        # Nuevo Telefono
        Label(self.edit_window, text = 'Telefono Actual: ').grid(row = 5, column = 1)
        Entry(self.edit_window).grid(row = 5, column = 2)

        # Telefono Anterior
        Label(self.edit_window, text = 'Mail Anterior: ').grid(row = 6, column = 1)
        Entry(self.edit_window, textvariable = StringVar(self.edit_window, value = old_mail), state = 'readonly').grid(row = 6, column = 2)

        # Nuevo Telefono
        Label(self.edit_window, text = 'Mail Actual: ').grid(row = 7, column = 1)
        Entry(self.edit_window).grid(row = 7, column = 2)

        # Botón de guardar cambios
        ttk.Button(self.edit_window, text = 'Actualizar', command = lambda: self.edit_clients).grid(row = 8, columnspan = 3, sticky = W + E)

    def edit_clients(self):
        parameters = ClienteParticular(self.name.get(), self.surname.get(), self.phone.get(), self.mail.get())
        parameters.id_cliente = self.rc.store(parameters)
        self.lista_clientes.append(parameters)
        self.message['text'] = 'El cliente personal {0} {1} ha sido añadido correctamente'.format(self.name.get(), self.surname.get())
        self.name.delete(0, END)
        self.surname.delete(0, END)
        self.phone.delete(0, END)
        self.mail.delete(0, END)
        self.get_clients()

if __name__ == '__main__':
    window = Tk()
    application = Product(window)
    window.mainloop()