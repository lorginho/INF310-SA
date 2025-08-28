"""
models/nodo.py
Implementación de la clase Nodo para árboles binarios
Autor: Lorgio Añez J.
Fecha: 2025-08-28
Descripción: Clase que representa un nodo en un árbol binario con métodos getter y setter
"""


class Nodo:
    """Clase que representa un nodo en un árbol binario."""

    def __init__(self, dato):
        """
        Inicializa un nuevo nodo.

        Args:
            dato: Valor a almacenar en el nodo.
        """
        self.dato = dato
        self.izquierdo = None
        self.derecho = None

    def get_dato(self):
        """
        Obtiene el valor almacenado en el nodo.

        Returns:
            Valor almacenado en el nodo.
        """
        return self.dato

    def set_dato(self, dato):
        """
        Establece el valor del nodo.

        Args:
            dato: Nuevo valor para el nodo.
        """
        self.dato = dato

    def get_izquierdo(self):
        """
        Obtiene el nodo hijo izquierdo.

        Returns:
            Nodo hijo izquierdo o None si no existe.
        """
        return self.izquierdo

    def set_izquierdo(self, izquierdo):
        """
        Establece el nodo hijo izquierdo.

        Args:
            izquierdo: Nuevo nodo hijo izquierdo.
        """
        self.izquierdo = izquierdo

    def get_derecho(self):
        """
        Obtiene el nodo hijo derecho.

        Returns:
            Nodo hijo derecho o None si no existe.
        """
        return self.derecho

    def set_derecho(self, derecho):
        """
        Establece el nodo hijo derecho.

        Args:
            derecho: Nuevo nodo hijo derecho.
        """
        self.derecho = derecho
