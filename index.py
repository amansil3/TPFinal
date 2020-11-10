from tkinter import ttk
from tkinter import *

import sqlite3

class Product:

    def __init__(self, window):
        self.wind = window
        self.wind.title('Product Application')

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
        self.price = Entry(frame)
        self.price.grid(row = 2, column = 1)

        # Button Guardar
        ttk.Button(frame, text = "Guardar Cliente").grid(row = 3, columnspan = 2, sticky = W + E)

        # Tabla
        self.tree = ttk.Treeview(height = 10, columns = 2)
        self.tree.grid(row = 4, column = 0, columnspan = 2)

if __name__ == '__main__':
    window = Tk()
    application = Product(window)
    window.mainloop()