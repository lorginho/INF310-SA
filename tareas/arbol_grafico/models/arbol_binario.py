"""
models/arbol_binario.py
Implementación del ADT Árbol Binario de Búsqueda
Autor: Lorgio Añez J.
Fecha: 2025-08-28
Descripción: Clase que representa un árbol binario con métodos para insertar, buscar y recorrer nodos
Ñ"""


from models.nodo import Nodo


class ArbolBinario:
    """Clase que representa un árbol binario de búsqueda."""

    def __init__(self):
        """Inicializa un árbol binario vacío."""
        self.raiz = None

    def get_raiz(self):
        """
        Obtiene la raíz del árbol.

        Returns:
            Nodo raíz del árbol o None si está vacío.
        """
        return self.raiz

    def set_raiz(self, raiz):
        """
        Establece la raíz del árbol.

        Args:
            raiz: Nuevo nodo raíz.
        """
        self.raiz = raiz

    def insertar_nodo(self, x):
        """
        Inserta un nuevo nodo con el valor x en el árbol si no existe.

        Args:
            x: Valor a insertar en el árbol.

        Returns:
            True si se insertó, False si ya existía.
        """
        if self.buscar_x(x) is not None:
            return False  # El valor ya existe, no se inserta

        if self.raiz is None:
            self.raiz = Nodo(x)
            return True
        else:
            self._insertar(self.raiz, x)
            return True

    def _insertar(self, nodo, x):
        """
        Método auxiliar recursivo para insertar un nodo.

        Args:
            nodo: Nodo actual en la recursión.
            x: Valor a insertar.
        """
        if x < nodo.get_dato():
            if nodo.get_izquierdo() is None:
                nodo.set_izquierdo(Nodo(x))
            else:
                self._insertar(nodo.get_izquierdo(), x)
        else:
            if nodo.get_derecho() is None:
                nodo.set_derecho(Nodo(x))
            else:
                self._insertar(nodo.get_derecho(), x)

    def es_vacio(self):
        """
        Verifica si el árbol está vacío.

        Returns:
            True si el árbol está vacío, False en caso contrario.
        """
        return self.raiz is None

    def es_hoja(self, nodo):
        """
        Verifica si un nodo es una hoja.

        Args:
            nodo: Nodo a verificar.

        Returns:
            True si el nodo es una hoja, False en caso contrario.
        """
        if nodo is None:
            return False
        return nodo.get_izquierdo() is None and nodo.get_derecho() is None

    def buscar_x(self, x):
        """
        Busca un valor en el árbol.

        Args:
            x: Valor a buscar.

        Returns:
            Nodo que contiene el valor o None si no se encuentra.
        """
        return self._buscar(self.raiz, x)

    def _buscar(self, nodo, x):
        """
        Método auxiliar recursivo para buscar un valor.

        Args:
            nodo: Nodo actual en la recursión.
            x: Valor a buscar.

        Returns:
            Nodo que contiene el valor o None si no se encuentra.
        """
        if nodo is None:
            return None
        if x == nodo.get_dato():
            return nodo
        if x < nodo.get_dato():
            return self._buscar(nodo.get_izquierdo(), x)
        return self._buscar(nodo.get_derecho(), x)

    def in_orden(self, nodo):
        """
        Recorrido in-order del árbol (izquierdo, raíz, derecho).
        Produce una lista ordenada de los nodos.

        Args:
            nodo: Nodo actual en la recursión.
        """
        if nodo is not None:
            self.in_orden(nodo.get_izquierdo())
            print(nodo.get_dato(), end=" ")
            self.in_orden(nodo.get_derecho())

    def post_orden(self, nodo):
        """
        Recorrido post-order del árbol (izquierdo, derecho, raíz).

        Args:
            nodo: Nodo actual en la recursión.
        """
        if nodo is not None:
            self.post_orden(nodo.get_izquierdo())
            self.post_orden(nodo.get_derecho())
            print(nodo.get_dato(), end=" ")

    def pre_orden(self, nodo):
        """
        Recorrido pre-order del árbol (raíz, izquierdo, derecho).

        Args:
            nodo: Nodo actual en la recursión.
        """
        if nodo is not None:
            print(nodo.get_dato(), end=" ")
            self.pre_orden(nodo.get_izquierdo())
            self.pre_orden(nodo.get_derecho())

    def amplitud(self):
        """
        Recorrido por amplitud (nivel por nivel) del árbol.

        Returns:
            Lista con los valores del árbol en orden por niveles.
        """
        if self.raiz is None:
            return []

        resultado = []
        # Usamos una cola (simulada con lista) para el recorrido
        cola = [self.raiz]

        while cola:
            # Extraemos el primer elemento de la cola
            nodo_actual = cola.pop(0)
            resultado.append(nodo_actual.get_dato())

            # Agregamos los hijos a la cola si existen
            if nodo_actual.get_izquierdo() is not None:
                cola.append(nodo_actual.get_izquierdo())
            if nodo_actual.get_derecho() is not None:
                cola.append(nodo_actual.get_derecho())

        return resultado
