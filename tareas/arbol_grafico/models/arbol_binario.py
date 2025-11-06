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

    # <-- FUNCIÓN AÑADIDA: LIMPIAR ARBOL
    def limpiar_arbol(self):
        """
        Establece la raíz a None, eliminando todo el árbol.
        """
        self.raiz = None
    # FUNCIÓN AÑADIDA: LIMPIAR ARBOL -->

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

    # <-- FUNCIÓN AÑADIDA: IN_ORDEN QUE DEVUELVE LISTA (para balanceo)
    def _in_orden_list(self, nodo):
        """
        Método auxiliar para recorrido in-orden que devuelve una lista de valores.
        """
        if nodo is None:
            return []

        # Inorden: Izquierda -> Raíz -> Derecha
        return (self._in_orden_list(nodo.get_izquierdo()) +
                [nodo.get_dato()] +
                self._in_orden_list(nodo.get_derecho()))

    # FUNCIÓN AÑADIDA: IN_ORDEN QUE DEVUELVE LISTA (para balanceo) -->

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

    # <-- FUNCIÓN AÑADIDA: VERIFICAR BALANCEO
    def esta_balanceado(self):
        """
        Verifica si el árbol completo es balanceado (propiedad AVL: factor de equilibrio <= 1 en todos los nodos).
        """

        # Función recursiva auxiliar anidada: retorna (es_balanceado, altura_del_subarbol)
        def verificar(nodo):
            if nodo is None:
                return True, 0

            # Verificar y obtener altura de los hijos
            izq_balanceado, h_izq = verificar(nodo.get_izquierdo())
            der_balanceado, h_der = verificar(nodo.get_derecho())

            # Calcular el Factor de Equilibrio (FE)
            fe = h_izq - h_der

            # Un nodo está balanceado si:
            # 1. Sus hijos están balanceados.
            # 2. Su propio FE está entre -1 y 1.
            nodo_balanceado = izq_balanceado and der_balanceado and abs(
                fe) <= 1

            # Retornar estado y altura del subárbol actual
            return nodo_balanceado, 1 + max(h_izq, h_der)

        balanceado, _ = verificar(self.raiz)
        return balanceado
    # FUNCIÓN AÑADIDA: VERIFICAR BALANCEO -->

    # <-- FUNCIÓN AÑADIDA: FORZAR BALANCEO
    def forzar_balanceo(self):
        """
        Reconstruye el árbol a partir del recorrido inorden para crear un ABB perfectamente balanceado 
        (altura mínima).
        """
        if self.raiz is None:
            return True

        # 1. Obtener los elementos ordenados (recorrido inorden)
        # Importar la función del controlador para obtener los valores
        from controllers.arbol_controller import recorrido_inorden
        elementos = recorrido_inorden(self.raiz)

        # 2. Función auxiliar para construir el ABB balanceado
        def construir_balanceado(lista):
            if not lista:
                return None

            medio = len(lista) // 2

            # El elemento central será la raíz del sub-árbol
            nueva_raiz = Nodo(lista[medio])

            # Construir sub-árboles recursivamente
            nueva_raiz.set_izquierdo(construir_balanceado(lista[:medio]))
            nueva_raiz.set_derecho(construir_balanceado(lista[medio+1:]))

            return nueva_raiz

        # Limpiar el árbol antes de reconstruir
        self.limpiar_arbol()

        # Asignar la nueva raíz balanceada
        self.raiz = construir_balanceado(elementos)

        return True
    # FUNCIÓN AÑADIDA: FORZAR BALANCEO -->

    def es_simetrico(self):
        """
        Verifica si el árbol es simétrico (espejo) en estructura.

        Returns:
            True si el árbol es simétrico, False en caso contrario.
        """
        if self.raiz is None:
            return True
        return self._es_espejo(self.raiz.get_izquierdo(), self.raiz.get_derecho())

    def _es_espejo(self, nodo1, nodo2):
        """
        Método auxiliar recursivo para verificar simetría.

        Args:
            nodo1: Nodo del subárbol izquierdo
            nodo2: Nodo del subárbol derecho

        Returns:
            True si los subárboles son espejo, False en caso contrario.
        """
        # Ambos nodos son None - simétricos
        if nodo1 is None and nodo2 is None:
            return True

        # Solo uno es None - no simétricos
        if nodo1 is None or nodo2 is None:
            return False

        # Verificar recursivamente:
        # - Izquierdo de nodo1 vs Derecho de nodo2
        # - Derecho de nodo1 vs Izquierdo de nodo2
        return (self._es_espejo(nodo1.get_izquierdo(), nodo2.get_derecho()) and
                self._es_espejo(nodo1.get_derecho(), nodo2.get_izquierdo()))

    def obtener_niveles_simetria(self):
        """
        Analiza la simetría de cada nivel del árbol.

        Returns:
            Lista de diccionarios con información de cada nivel
            Ejemplo: [{'nivel': 0, 'simetrico': True, 'nodos': [5]}, ...]
        """
        if self.raiz is None:
            return []

        niveles = []
        cola = [self.raiz]
        nivel_actual = 0

        while cola:
            # Obtener nodos del nivel actual
            nodos_nivel = []
            siguiente_cola = []

            for nodo in cola:
                if nodo is None:
                    nodos_nivel.append(None)
                    siguiente_cola.extend([None, None])
                else:
                    nodos_nivel.append(nodo.get_dato())
                    siguiente_cola.append(nodo.get_izquierdo())
                    siguiente_cola.append(nodo.get_derecho())

            # Verificar simetría del nivel
            es_simetrico = self._nivel_es_simetrico(nodos_nivel)
            niveles.append({
                'nivel': nivel_actual,
                'simetrico': es_simetrico,
                'nodos': nodos_nivel
            })

            # Si todos son None, terminamos
            if all(nodo is None for nodo in siguiente_cola):
                break

            cola = siguiente_cola
            nivel_actual += 1

        return niveles

    def _nivel_es_simetrico(self, nodos_nivel):
        """
        Verifica si un nivel es simétrico comparando posiciones espejo.
        """
        n = len(nodos_nivel)
        for i in range(n // 2):
            # Comparar posición i con posición n-1-i
            # Ambos deben ser None o ambos no-None
            if (nodos_nivel[i] is None) != (nodos_nivel[n-1-i] is None):
                return False
        return True
