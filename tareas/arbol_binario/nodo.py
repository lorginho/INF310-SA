
'''
title: class Nodo
autor: lorgio añez jimenez
created:2025-08-23
version: 0.1
'''


class Nodo:
    '''
    Clase Nodo
    Constructor que inicializa la clase Nodo
    self.__elemento  significa q es un atributo privado
    def __getelemento  igul en fucniones si se pone con guion bajo se hace metodo privado
    '''

    def __init__(self):
        self.__valor = None
        self.__izq = None
        self.__der = None
    '''@property'''

    def get_elemento(self):
        p = self.valor
        return (p)

    def get_hijo_izq(self):
        p = self._izq
        return (p)

    def get_hijo_der(self):
        p = self._der
        return (p)

    '''@setelemento.setter'''

    def set_elemento(self, x):
        self.valor = x

    def set_hijo_izq(self, x):
        self._izq = x

    def set_hijo_der(self, x):
        self._der = x
