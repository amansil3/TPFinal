from tkinter import ttk
from tkinter import *
from repositorioClientes import RepositorioClientes

import sqlite3

class Product:

    nombre_bd = 'base_datos.sqlite'

    def __init__(self, window):
        self.wind = window
        self.wind.title('Listado de Clientes')

        #Frame
        frame = LabelFrame(self.wind, text = 'Registrar un nuevo cliente')
        frame.grid(row = 0, column = 0, columnspan = 3, pady = 20)

        # Input Nombre
        Label(frame, text = 'Nombre: ').grid(row = 1, column = 0)
        Entry(frame)
        self.name = Entry(frame)
        self.name.focus()
        self.name.grid(row = 1, column = 1)

        # Input Apellido
        Label(frame, text = 'Apellido: ').grid(row = 2, column = 0)
        Entry(frame)
        self.surname = Entry(frame)
        self.surname.grid(row = 2, column = 1)

        # Input Telefono
        Label(frame, text = 'Telefono: ').grid(row = 3, column = 0)
        Entry(frame)
        self.surname = Entry(frame)
        self.surname.grid(row = 3, column = 1)

        # Input Telefono
        Label(frame, text = 'Mail: ').grid(row = 4, column = 0)
        Entry(frame)
        self.surname = Entry(frame)
        self.surname.grid(row = 4, column = 1)

        # Button Guardar
        ttk.Button(frame, text = "Guardar Cliente", command = self.add_clients).grid(row = 5, columnspan = 2, sticky = W + E)

        # Tabla
        self.tree = ttk.Treeview(height = 10, columns = 2)
        self.tree.grid(row = 6, column = 0, columnspan = 2)
        self.tree.heading('#0', text = 'Nombre', anchor = CENTER)
        self.tree.heading('#1', text = 'Apellido', anchor = CENTER)

        self.get_clients()

    def run_query (self, query, parameters = ()):
        with sqlite3.connect(self.nombre_bd) as Conectar:
            cursor = Conectar.cursor()
            resultado = cursor.execute(query, parameters)
            Conectar.commit()
        return resultado

    def get_clients(self):
        
        # Limpio la tabla antes de arrancar la query
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        
        # Query
        query = 'SELECT * FROM repositorioClientes'
        db_rows = self.run_query(query)
        for row in db_rows:
            self.tree.insert('', 0, values = row[1], text = row[2])
    
    def validations(self):
        return  len(self.name.get()) !=0 and len(self.surname.get()) !=0

    def add_clients(self):
        if self.validations():
            query = 'INSERT INTO cliente VALUES (null, ?, ?)'
            parameters = (self.name.get(), self.surname.get())
            self.run_query(query, parameters)
            print('Datos Guardados')
        else:
            print('El nombre y el apellido son requeridos')
        self.get_clients()

if __name__ == '__main__':
    window = Tk()
    application = Product(window)
    window.mainloop()