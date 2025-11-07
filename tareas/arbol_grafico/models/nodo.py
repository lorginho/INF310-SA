"""
models/nodo.py
Implementación de la clase Nodo para árboles binarios
Autor: Lorgio Añez J.
Fecha: 2025-08-28
Descripción: Clase que representa un nodo en un árbol binario 
con métodos getter y setter
"""


class Nodo:
    """Representa un nodo en un árbol binario."""

    def __init__(self, dato):
        self.__dato = dato
        self.__izquierdo = None
        self.__derecho = None

    def get_dato(self):
        """Devuelve el valor almacenado en el nodo."""
        return self.__dato

    def set_dato(self, dato):
        """Actualiza el valor del nodo."""
        self.__dato = dato

    def get_izquierdo(self):
        """Devuelve el hijo izquierdo."""
        return self.__izquierdo

    def set_izquierdo(self, izquierdo):
        """Establece el hijo izquierdo."""
        self.__izquierdo = izquierdo

    def get_derecho(self):
        """Devuelve el hijo derecho."""
        return self.__derecho

    def set_derecho(self, derecho):
        """Establece el hijo derecho."""
        self.__derecho = derecho

    def __str__(self):
        """Representación en string del nodo."""
        return f"Nodo({self.__dato})"

    def es_hoja(self):
        """Verifica si el nodo es una hoja (sin hijos)."""
        return self.__izquierdo is None and self.__derecho is None
