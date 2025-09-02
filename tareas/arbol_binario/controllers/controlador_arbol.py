"""
controllers/controlador_arbol.py
Controlador para operaciones del árbol binario (MVC)
Autor: Lorgio Añez J.
Fecha: 2025-09-01
Descripción: Controlador que gestiona las operaciones entre la vista y el modelo del árbol binario
"""

from models.arbol_binario import ArbolBinario


class ControladorArbol:
    """Controlador para gestionar las operaciones del árbol binario."""

    def __init__(self):
        """Inicializa el controlador con un árbol binario vacío."""
        self.arbol = ArbolBinario()

    def insertar_nodo(self, x):
        """
        Inserta un nuevo nodo en el árbol si no existe.

        Args:
            x: Valor a insertar.

        Returns:
            True si se inserto, False si ya existia.
        """
        return self.arbol.insertar_nodo(x)

    def es_vacio(self):
        """
        Verifica si el árbol está vacío.

        Returns:
            True si el árbol está vacío, False en caso contrario.
        """
        return self.arbol.es_vacio()

    def es_hoja(self, dato):
        """
        Verifica si un nodo con el valor dado es una hoja.

        Args:
            dato: Valor del nodo a verificar.

        Returns:
            True si el nodo es una hoja, False en caso contrario.
        """
        nodo = self.arbol.buscar_x(dato)
        return nodo is not None and self.arbol.es_hoja(nodo)

    def buscar_x(self, x):
        """
        Busca un valor en el árbol.

        Args:
            x: Valor a buscar.

        Returns:
            True si el valor existe en el árbol, False en caso contrario.
        """
        return self.arbol.buscar_x(x) is not None

    def in_orden(self):
        """
        Realiza un recorrido in-order del árbol.
        """
        self.arbol.in_orden(self.arbol.get_raiz())
        print()

    def post_orden(self):
        """
        Realiza un recorrido post-order del árbol.
        """
        self.arbol.post_orden(self.arbol.get_raiz())
        print()

    def pre_orden(self):
        """
        Realiza un recorrido pre-order del árbol.
        """
        self.arbol.pre_orden(self.arbol.get_raiz())
        print()

    def amplitud(self):
        """
        Realiza un recorrido por amplitud del arbol.

        Returns:
            Lista con los valores del arbol en orden por niveles.            
        """
        return self.arbol.amplitud()
