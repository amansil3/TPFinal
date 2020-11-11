#! /usr/bin/env python3
from cliente import Cliente

class ClienteCorporativo(Cliente):
    '''Representa un cliente corporativo'''
    def __init__(self, nombre_empresa, nombre_contacto, telefono_contacto,
            telefono, mail, id_cliente = None):
        self.nombre_empresa = nombre_empresa
        self.nombre_contacto = nombre_contacto
        self.telefono_contacto = telefono_contacto
        super().__init__(telefono, mail, id_cliente)

    def __str__(self):
        '''No objeto a string'''
        cadena = f"{self.id_cliente}: {self.nombre_empresa} (Cliente Corporativo) \n"
        cadena+= f"{self.telefono} - {self.mail}\n"
        cadena+= f"Contacto: {self.nombre_contacto} {self.telefono_contacto}\n"
        return cadena

