from tkinter import ttk
from tkinter import *
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
        ttk.Button(frame, text = "Agregar cliente corporativo", command = self.add_clientsger_window).grid(row = 6, columnspan = 2, sticky = W + E)
        ttk.Button(frame, text = "Editar cliente", command = self.edit_clients).grid(row = 7, columnspan = 2, sticky = W + E)
        ttk.Button(frame, text = "Ver clientes corporativos", command = self.get_client_corporativo).grid(row = 8, columnspan = 2, sticky = W + E)

        # Mensajes de salida
        self.message = Label(text = '', fg = 'red')
        self.message.grid(row = 9, column = 0, columnspan = 2, sticky = W + E)

        '''
        # Tabla
        self.tree = ttk.Treeview(height = 10, columns = ("#1","#2","#3"))
        self.tree.grid(row = 9, column = 0, columnspan = 5)

        self.tree.heading('#0', text = 'Nombre', anchor = CENTER)
        self.tree.heading('#1', text = 'Apellido', anchor = CENTER)
        self.tree.heading('#2', text = 'Teléfono', anchor = CENTER)
        self.tree.heading('#3', text = 'Mail', anchor = CENTER)

        self.get_clients()
        '''

    def run_query (self, query, parameters = ()):
        with sqlite3.connect(self.nombre_bd) as Conectar:
            cursor = Conectar.cursor()
            resultado = cursor.execute(query, parameters)
            Conectar.commit()
        return resultado

    def get_client_corporativo(self, lista = None):

        self.client_corp_window = Toplevel()
        self.client_corp_window.title = 'Agregar cliente'

        '''
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
            self.tree.insert('', 0, text = (fila[4]), values = (fila[5], fila[1], fila[2]))
        '''
    def get_clients(self, lista = None):
        # Limpio la tabla antes de arrancar la query
        #records = self.tree.get_children()
        #for element in records:
        #    self.tree.delete(element)
        
        # Muestro clientes
        query = 'SELECT * FROM cliente JOIN cliente_particular ON cliente.id=cliente_particular.id_cliente ORDER BY id ASC'
        query1 = 'SELECT * FROM cliente JOIN cliente_corporativo ON cliente.id=cliente_corporativo.id_cliente ORDER BY id ASC'
        db_rows = self.run_query(query)
        db_rows1 = self.run_query(query1)        
        #for row in db_rows:
        #    self.tree.insert('', 0, text = (row[4]), values = (row[5], row[1],row [2]))
        #for fila in db_rows1:
        #    self.tree.insert('', 0, text = (fila[4]), values = (fila[5], fila[1], fila[2]))
    
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

    def add_clientsger_window(self):

        self.add_window_ger = Toplevel()
        self.add_window_ger.title = 'Agregar cliente corporativo'

        # Input Nombre Empresa
        Label(self.add_window_ger, text = 'Nombre Empresa: ').grid(row = 1, column = 0)
        Entry(self.add_window_ger, textvariable = StringVar(self.add_window_ger), state = 'readonly')
        self.company_name = Entry(self.add_window_ger)
        self.company_name.focus()
        self.company_name.grid(row = 1, column = 1)

        # Input Nombre Contacto
        Label(self.add_window_ger, text = 'Nombre Contacto: ').grid(row = 2, column = 0)
        Entry(self.add_window_ger)
        self.contact_name = Entry(self.add_window_ger)
        self.contact_name.grid(row = 2, column = 1)

        # Input Telefono
        Label(self.add_window_ger, text = 'Telefono: ').grid(row = 3, column = 0)
        Entry(self.add_window_ger)
        self.phone = Entry(self.add_window_ger)
        self.phone.grid(row = 3, column = 1)

        # Input Telefono de Contacto
        Label(self.add_window_ger, text = 'Telefono de contacto: ').grid(row = 4, column = 0)
        Entry(self.add_window_ger)
        self.contact_phone = Entry(self.add_window_ger)
        self.contact_phone.grid(row = 4, column = 1)

        # Input Mail
        Label(self.add_window_ger, text = 'Mail: ').grid(row = 5, column = 0)
        Entry(self.add_window_ger)
        self.mail = Entry(self.add_window_ger)
        self.mail.grid(row = 5, column = 1)
        
        # Botonera
        ttk.Button(self.add_window_ger, text = "Guardar", command = self.add_client_corporativo).grid(row = 6, columnspan = 2, sticky = W + E)

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

    def edit_clients(self):
        '''Editar un cliente'''
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['text'][0]
        except IndexError:
            self.message['text'] = 'Por favor, seleccione un registro'
            return
        name = self.tree.item(self.tree.selection())['text']
        oldprice = self.tree.item(self.tree.selection())['values'][0]
        self.edit_window = Toplevel()
        self.edit_window.title = 'Editar cliente'


if __name__ == '__main__':
    window = Tk()
    application = Product(window)
    window.mainloop()