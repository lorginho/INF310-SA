"""
models/arbol_binario.py
Implementación del ADT Árbol Binario de Búsqueda
Autor: Lorgio Añez J.
Fecha: 2025-08-28
Descripción: Clase que representa un árbol binario con métodos para insertar, buscar y recorrer nodos
"""


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

    def eliminar_nodo(self, x):
        """
        Elimina un nodo con el valor x del árbol.

        Args:
            x: Valor a eliminar

        Returns:
            True si se eliminó, False si no se encontró
        """
        if self.buscar_x(x) is None:
            return False

        self.raiz = self._eliminar(self.raiz, x)
        return True

    def _eliminar(self, nodo, x):
        """
        Método auxiliar recursivo para eliminar un nodo.
        """
        if nodo is None:
            return nodo

        if x < nodo.get_dato():
            nodo.set_izquierdo(self._eliminar(nodo.get_izquierdo(), x))
        elif x > nodo.get_dato():
            nodo.set_derecho(self._eliminar(nodo.get_derecho(), x))
        else:
            # Nodo con un solo hijo o sin hijos
            if nodo.get_izquierdo() is None:
                return nodo.get_derecho()
            elif nodo.get_derecho() is None:
                return nodo.get_izquierdo()

            # Nodo con dos hijos: obtener el sucesor inorden (mínimo en subárbol derecho)
            temp = self._min_valor_nodo(nodo.get_derecho())
            nodo.set_dato(temp.get_dato())
            nodo.set_derecho(self._eliminar(
                nodo.get_derecho(), temp.get_dato()))

        return nodo

    def _min_valor_nodo(self, nodo):
        """
        Encuentra el nodo con el valor mínimo en un subárbol.
        """
        actual = nodo
        while actual.get_izquierdo() is not None:
            actual = actual.get_izquierdo()
        return actual

    def altura(self):
        """
        Calcula la altura del árbol.

        Returns:
            Altura del árbol (0 si está vacío)
        """
        return self._altura(self.raiz)

    def _altura(self, nodo):
        if nodo is None:
            return 0
        return 1 + max(self._altura(nodo.get_izquierdo()), self._altura(nodo.get_derecho()))

    def contar_nodos(self):
        """
        Cuenta el total de nodos en el árbol.
        """
        return self._contar_nodos(self.raiz)

    def _contar_nodos(self, nodo):
        if nodo is None:
            return 0
        return 1 + self._contar_nodos(nodo.get_izquierdo()) + self._contar_nodos(nodo.get_derecho())

    def contar_hojas(self):
        """
        Cuenta los nodos hoja en el árbol.
        """
        return self._contar_hojas(self.raiz)

    def _contar_hojas(self, nodo):
        if nodo is None:
            return 0
        if self.es_hoja(nodo):
            return 1
        return self._contar_hojas(nodo.get_izquierdo()) + self._contar_hojas(nodo.get_derecho())

    def eliminar_rama(self, x):
        """
        Elimina toda la rama que comienza en el nodo con valor x.

        Args:
            x: Valor del nodo raíz de la rama a eliminar

        Returns:
            True si se encontró y eliminó la rama, False si no se encontró el nodo
        """
        if self.raiz is None:
            return False

        # Caso especial: si la raíz es el nodo a eliminar
        if self.raiz.get_dato() == x:
            self.raiz = None
            return True

        # Buscar el nodo padre que contiene al nodo que será eliminado
        padre = self._buscar_padre(self.raiz, x)
        if padre is None:
            return False

        # Eliminar la referencia al nodo desde su padre
        if padre.get_izquierdo() and padre.get_izquierdo().get_dato() == x:
            padre.set_izquierdo(None)
            return True
        elif padre.get_derecho() and padre.get_derecho().get_dato() == x:
            padre.set_derecho(None)
            return True

        return False

    def _buscar_padre(self, nodo, x):
        """
        Busca el padre del nodo con valor x.

        Returns:
            El nodo padre que contiene al nodo con valor x, o None si no se encuentra.
        """
        if nodo is None:
            return None

        # Verificar si el nodo actual es el padre del nodo buscado
        if (nodo.get_izquierdo() and nodo.get_izquierdo().get_dato() == x) or \
                (nodo.get_derecho() and nodo.get_derecho().get_dato() == x):
            return nodo

        # Buscar recursivamente en los subárboles
        if x < nodo.get_dato():
            return self._buscar_padre(nodo.get_izquierdo(), x)
        else:
            return self._buscar_padre(nodo.get_derecho(), x)

    def obtener_rama(self, x):
        """
        Obtiene todos los valores de la rama que comienza en el nodo con valor x.

        Returns:
            Lista con los valores de la rama en recorrido preorden, o None si no se encuentra
        """
        nodo = self.buscar_x(x)
        if nodo is None:
            return None

        return self._obtener_rama_preorden(nodo)

    def _obtener_rama_preorden(self, nodo):
        """Obtiene los valores de una rama en recorrido preorden."""
        if nodo is None:
            return []

        resultado = [nodo.get_dato()]
        # Agregar subárbol izquierdo
        if nodo.get_izquierdo():
            resultado.extend(self._obtener_rama_preorden(nodo.get_izquierdo()))
        # Agregar subárbol derecho
        if nodo.get_derecho():
            resultado.extend(self._obtener_rama_preorden(nodo.get_derecho()))

        return resultado

    def contar_nodos_rama(self, x):
        """
        Cuenta la cantidad de nodos en la rama que comienza en el nodo con valor x.
        """
        nodo = self.buscar_x(x)
        if nodo is None:
            return 0

        return self._contar_nodos(nodo)  # Reutilizamos el método existente
