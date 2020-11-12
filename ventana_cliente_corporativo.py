#! /usr/bin/python3
from tkinter import ttk, Label, LabelFrame, Entry, StringVar, Tk, CENTER, W, E, END, Toplevel
from clienteCorporativo import ClienteCorporativo
from clienteParticular import ClienteParticular
from repositorioClientes import RepositorioClientes

import sqlite3

class VentanaClienteCorporativo:
    
    nombre_bd = 'base_datos.sqlite'

    def __init__(self, window):
        self.wind = window
        self.wind.title('Listado de clientes corporativos')
        self.rc = RepositorioClientes()
        #self.lista_clientes = self.rc.get_all_corporativos()

        #Frame
        frame = LabelFrame(self.wind, text = 'Registrar un nuevo cliente corporativo')
        frame.grid(row = 0, column = 0, columnspan = 3, pady = 20)

        
        #Botonera
        ttk.Button(frame, text = "Nuevo cliente").grid(row = 1, columnspan = 2, sticky = W + E)
        ttk.Button(frame, text = "Editar cliente").grid(row = 2, columnspan = 2, sticky = W + E)
        ttk.Button(frame, text = "Eliminar cliente").grid(row = 3, columnspan = 2, sticky = W + E)
        
        # Mensajes de salida
        self.message = Label(text = '', fg = 'red')
        self.message.grid(row = 4, column = 0, columnspan = 2, sticky = W + E)

        # Tabla
        self.tree = ttk.Treeview(height = 10, columns = ("#1","#2","#3","#4"))
        self.tree.grid(row = 5, column = 0, columnspan = 5)

        self.tree.heading('#0', text = 'Nombre de la Empresa', anchor = CENTER)
        self.tree.heading('#1', text = 'Teléfono', anchor = CENTER)
        self.tree.heading('#2', text = 'Nombre de Contacto', anchor = CENTER)
        self.tree.heading('#3', text = 'Teléfono de contacto', anchor = CENTER)
        self.tree.heading('#4', text = 'Mail', anchor = CENTER)

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
        query = 'SELECT * FROM cliente JOIN cliente_corporativo ON cliente.id=cliente_corporativo.id_cliente ORDER BY id ASC'
        db_rows = self.run_query(query)
        for row in db_rows:
            self.tree.insert('', 0, text = (row[4]), values = (row[1], row[5], row[6], row[2]))

if __name__ == '__main__':
    window = Tk()
    application = VentanaClienteCorporativo(window)
    window.mainloop()