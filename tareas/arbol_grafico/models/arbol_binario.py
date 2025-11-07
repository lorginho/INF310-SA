"""
models/arbol_binario.py
Implementación del ADT Árbol Binario de Búsqueda
Autor: Lorgio Añez J.
Fecha: 2025-08-28
Descripción: Clase que representa un árbol binario con métodos para insertar, buscar y recorrer nodos
"""

from collections import deque  # Para colas eficientes en recorrido por amplitud
from models.nodo import Nodo


class ArbolBinario:
    """Representa un árbol binario de búsqueda."""

    def __init__(self):
        # Inicializa un árbol vacío (raíz = None)
        self.raiz = None

    # ===== OPERACIONES BÁSICAS DEL ÁRBOL =====

    def get_raiz(self):
        return self.raiz

    def set_raiz(self, raiz):
        self.raiz = raiz

    def es_vacio(self):
        """Verifica si el árbol no tiene nodos."""
        return self.raiz is None

    def limpiar_arbol(self):
        """Elimina todos los nodos del árbol."""
        self.raiz = None

    # ===== INSERCIÓN DE NODOS =====

    def insertar_nodo(self, x):
        """
        Inserta un nuevo valor en el árbol manteniendo la propiedad de ABB.
        No permite valores duplicados.
        """
        # Verificar si el valor ya existe (no se permiten duplicados)
        if self.buscar_x(x) is not None:
            return False

        # Caso especial: árbol vacío
        if self.raiz is None:
            self.raiz = Nodo(x)
            return True

        # Insertar recursivamente en la posición correcta
        self._insertar(self.raiz, x)
        return True

    def _insertar(self, nodo, x):
        """
        Método auxiliar recursivo para insertar.
        Busca la posición correcta comparando con el nodo actual.
        """
        if x < nodo.get_dato():
            # Insertar en subárbol izquierdo
            if nodo.get_izquierdo() is None:
                nodo.set_izquierdo(Nodo(x))
            else:
                self._insertar(nodo.get_izquierdo(), x)
        else:
            # Insertar en subárbol derecho
            if nodo.get_derecho() is None:
                nodo.set_derecho(Nodo(x))
            else:
                self._insertar(nodo.get_derecho(), x)

    # ===== BÚSQUEDA DE NODOS =====

    def buscar_x(self, x):
        """Busca un valor en el árbol y retorna el nodo que lo contiene."""
        return self._buscar(self.raiz, x)

    def _buscar(self, nodo, x):
        """
        Búsqueda recursiva en el árbol.
        Aprovecha la propiedad de ABB para hacer búsqueda eficiente.
        """
        if nodo is None:
            return None  # No encontrado
        if x == nodo.get_dato():
            return nodo  # Encontrado
        if x < nodo.get_dato():
            # Buscar en subárbol izquierdo
            return self._buscar(nodo.get_izquierdo(), x)
        # Buscar en subárbol derecho
        return self._buscar(nodo.get_derecho(), x)

    # ===== RECORRIDOS DEL ÁRBOL =====

    def in_orden(self, nodo):
        """
        Recorrido in-orden: izquierdo -> raíz -> derecho.
        Produce los valores ordenados de menor a mayor.
        """
        if nodo is not None:
            self.in_orden(nodo.get_izquierdo())
            print(nodo.get_dato(), end=" ")
            self.in_orden(nodo.get_derecho())

    def _in_orden_list(self, nodo):
        """
        Versión del in-orden que retorna una lista ordenada.
        Útil para operaciones como el balanceo del árbol.
        """
        if nodo is None:
            return []
        return (self._in_orden_list(nodo.get_izquierdo()) +
                [nodo.get_dato()] +
                self._in_orden_list(nodo.get_derecho()))

    def pre_orden(self, nodo):
        """
        Recorrido pre-orden: raíz -> izquierdo -> derecho.
        Útil para copiar la estructura del árbol.
        """
        if nodo is not None:
            print(nodo.get_dato(), end=" ")
            self.pre_orden(nodo.get_izquierdo())
            self.pre_orden(nodo.get_derecho())

    def post_orden(self, nodo):
        """
        Recorrido post-orden: izquierdo -> derecho -> raíz.
        Útil para eliminar árboles.
        """
        if nodo is not None:
            self.post_orden(nodo.get_izquierdo())
            self.post_orden(nodo.get_derecho())
            print(nodo.get_dato(), end=" ")

    def amplitud(self):
        """
        Recorrido por niveles (amplitud).
        Usa una cola para procesar nodos nivel por nivel.
        """
        if self.raiz is None:
            return []

        resultado = []
        cola = deque([self.raiz])  # Cola eficiente para BFS

        while cola:
            nodo_actual = cola.popleft()  # Obtener el primer nodo de la cola
            resultado.append(nodo_actual.get_dato())

            # Agregar hijos a la cola para procesar después
            if nodo_actual.get_izquierdo():
                cola.append(nodo_actual.get_izquierdo())
            if nodo_actual.get_derecho():
                cola.append(nodo_actual.get_derecho())

        return resultado

    # ===== ELIMINACIÓN DE NODOS =====

    def eliminar_nodo(self, x):
        """Elimina un nodo con el valor x manteniendo la propiedad de ABB."""
        if self.buscar_x(x) is None:
            return False  # El valor no existe

        self.raiz = self._eliminar(self.raiz, x)
        return True

    def _eliminar(self, nodo, x):
        """
        Eliminación recursiva con tres casos:
        1. Nodo hoja: simplemente se elimina
        2. Nodo con un hijo: el hijo reemplaza al nodo
        3. Nodo con dos hijos: se busca el sucesor inorden
        """
        if nodo is None:
            return nodo

        # Buscar el nodo a eliminar
        if x < nodo.get_dato():
            nodo.set_izquierdo(self._eliminar(nodo.get_izquierdo(), x))
        elif x > nodo.get_dato():
            nodo.set_derecho(self._eliminar(nodo.get_derecho(), x))
        else:
            # Nodo encontrado - aplicar estrategia según cantidad de hijos

            # Caso 1: Nodo con un hijo o sin hijos
            if nodo.get_izquierdo() is None:
                return nodo.get_derecho()  # El derecho reemplaza al nodo
            elif nodo.get_derecho() is None:
                return nodo.get_izquierdo()  # El izquierdo reemplaza al nodo

            # Caso 2: Nodo con dos hijos
            # Buscar el sucesor inorden (mínimo del subárbol derecho)
            temp = self._min_valor_nodo(nodo.get_derecho())
            # Copiar el valor del sucesor
            nodo.set_dato(temp.get_dato())
            # Eliminar el sucesor original
            nodo.set_derecho(self._eliminar(
                nodo.get_derecho(), temp.get_dato()))

        return nodo

    def _min_valor_nodo(self, nodo):
        """Encuentra el nodo con el valor mínimo en un subárbol."""
        actual = nodo
        while actual.get_izquierdo() is not None:
            actual = actual.get_izquierdo()
        return actual

    # ===== INFORMACIÓN DEL ÁRBOL =====

    def altura(self):
        """Calcula la altura máxima del árbol."""
        return self._altura(self.raiz)

    def _altura(self, nodo):
        """Calcula recursivamente la altura de un subárbol."""
        if nodo is None:
            return 0
        return 1 + max(self._altura(nodo.get_izquierdo()),
                       self._altura(nodo.get_derecho()))

    def contar_nodos(self):
        """Cuenta el total de nodos en el árbol."""
        return self._contar_nodos(self.raiz)

    def _contar_nodos(self, nodo):
        """Cuenta recursivamente los nodos en un subárbol."""
        if nodo is None:
            return 0
        return (1 + self._contar_nodos(nodo.get_izquierdo()) +
                self._contar_nodos(nodo.get_derecho()))

    def contar_hojas(self):
        """Cuenta los nodos hoja (sin hijos) en el árbol."""
        return self._contar_hojas(self.raiz)

    def _contar_hojas(self, nodo):
        """Cuenta recursivamente las hojas en un subárbol."""
        if nodo is None:
            return 0
        if nodo.es_hoja():  # Usa el método del nodo para verificar si es hoja
            return 1
        return (self._contar_hojas(nodo.get_izquierdo()) +
                self._contar_hojas(nodo.get_derecho()))

    # ===== OPERACIONES CON RAMAS =====

    def eliminar_rama(self, x):
        """
        Elimina toda una rama del árbol a partir del nodo con valor x.
        Útil para podar subárboles completos.
        """
        if self.raiz is None:
            return False

        # Caso especial: eliminar toda el árbol
        if self.raiz.get_dato() == x:
            self.raiz = None
            return True

        # Buscar el padre del nodo a eliminar
        padre = self._buscar_padre(self.raiz, x)
        if padre is None:
            return False  # Nodo no encontrado

        # Eliminar la referencia del padre al nodo
        if (padre.get_izquierdo() and
                padre.get_izquierdo().get_dato() == x):
            padre.set_izquierdo(None)
            return True
        elif (padre.get_derecho() and
              padre.get_derecho().get_dato() == x):
            padre.set_derecho(None)
            return True

        return False

    def _buscar_padre(self, nodo, x):
        """
        Busca el nodo padre del nodo que contiene el valor x.
        Retorna None si no encuentra el nodo o si es la raíz.
        """
        if nodo is None:
            return None

        # Verificar si alguno de los hijos tiene el valor buscado
        if ((nodo.get_izquierdo() and nodo.get_izquierdo().get_dato() == x) or
                (nodo.get_derecho() and nodo.get_derecho().get_dato() == x)):
            return nodo  # Este es el padre

        # Buscar recursivamente en los subárboles
        if x < nodo.get_dato():
            return self._buscar_padre(nodo.get_izquierdo(), x)
        return self._buscar_padre(nodo.get_derecho(), x)

    def obtener_rama(self, x):
        """Obtiene todos los valores de la rama que comienza en x (pre-orden)."""
        nodo = self.buscar_x(x)
        return self._obtener_rama_preorden(nodo) if nodo else None

    def _obtener_rama_preorden(self, nodo):
        """Recoge todos los valores de una rama en recorrido pre-orden."""
        if nodo is None:
            return []

        resultado = [nodo.get_dato()]
        if nodo.get_izquierdo():
            resultado.extend(self._obtener_rama_preorden(nodo.get_izquierdo()))
        if nodo.get_derecho():
            resultado.extend(self._obtener_rama_preorden(nodo.get_derecho()))

        return resultado

    def contar_nodos_rama(self, x):
        """Cuenta cuántos nodos hay en la rama que comienza en x."""
        nodo = self.buscar_x(x)
        return self._contar_nodos(nodo) if nodo else 0

    # ===== BALANCEO DEL ÁRBOL =====

    def esta_balanceado(self):
        """
        Verifica si el árbol está balanceado (propiedad AVL).
        Un árbol está balanceado si para cada nodo, la diferencia de alturas
        entre sus subárboles izquierdo y derecho es como máximo 1.
        """
        def verificar(nodo):
            if nodo is None:
                return True, 0  # Árbol vacío está balanceado y altura 0

            # Verificar recursivamente los subárboles
            izq_balanceado, h_izq = verificar(nodo.get_izquierdo())
            der_balanceado, h_der = verificar(nodo.get_derecho())

            # Calcular factor de equilibrio
            fe = h_izq - h_der
            # El nodo está balanceado si sus hijos lo están y |FE| <= 1
            nodo_balanceado = (izq_balanceado and der_balanceado
                               and abs(fe) <= 1)

            return nodo_balanceado, 1 + max(h_izq, h_der)

        balanceado, _ = verificar(self.raiz)
        return balanceado

    def forzar_balanceo(self):
        """
        Reconstruye el árbol como un árbol perfectamente balanceado.
        Convierte el árbol en un ABB balanceado de altura mínima.
        """
        if self.raiz is None:
            return True

        # 1. Obtener todos los valores ordenados
        elementos = self._in_orden_list(self.raiz)

        # 2. Construir árbol balanceado recursivamente
        def construir_balanceado(lista):
            if not lista:
                return None

            # El elemento del medio será la raíz (estrategia divide y vencerás)
            medio = len(lista) // 2
            nueva_raiz = Nodo(lista[medio])
            # Construir subárbol izquierdo con la mitad izquierda
            nueva_raiz.set_izquierdo(construir_balanceado(lista[:medio]))
            # Construir subárbol derecho con la mitad derecha
            nueva_raiz.set_derecho(construir_balanceado(lista[medio+1:]))

            return nueva_raiz

        # 3. Reemplazar el árbol actual por el balanceado
        self.raiz = construir_balanceado(elementos)
        return True

    # ===== SIMETRÍA DEL ÁRBOL =====

    def es_simetrico(self):
        """
        Verifica si el árbol es simétrico (espejo) en estructura.
        Un árbol es simétrico si el subárbol izquierdo es espejo del derecho.
        """
        if self.raiz is None:
            return True
        return self._es_espejo(self.raiz.get_izquierdo(),
                               self.raiz.get_derecho())

    def _es_espejo(self, nodo1, nodo2):
        """
        Verifica recursivamente si dos subárboles son espejo.
        Compara: izquierdo de nodo1 con derecho de nodo2, y viceversa.
        """
        if nodo1 is None and nodo2 is None:
            return True  # Ambos vacíos → simétricos
        if nodo1 is None or nodo2 is None:
            return False  # Solo uno vacío → no simétricos

        # Verificar recursivamente la simetría espejo
        return (self._es_espejo(nodo1.get_izquierdo(), nodo2.get_derecho()) and
                self._es_espejo(nodo1.get_derecho(), nodo2.get_izquierdo()))

    def obtener_niveles_simetria(self):
        """
        Analiza la simetría nivel por nivel.
        Útil para identificar en qué nivel específico falla la simetría.
        """
        if self.raiz is None:
            return []

        niveles = []
        cola = deque([self.raiz])
        nivel_actual = 0

        while cola:
            nodos_nivel = []
            siguiente_cola = deque()

            # Procesar todos los nodos del nivel actual
            for nodo in cola:
                if nodo is None:
                    nodos_nivel.append(None)
                    # Para mantener la estructura, agregamos hijos None
                    siguiente_cola.extend([None, None])
                else:
                    nodos_nivel.append(nodo.get_dato())
                    # Agregar hijos al siguiente nivel (aunque sean None)
                    siguiente_cola.append(nodo.get_izquierdo())
                    siguiente_cola.append(nodo.get_derecho())

            # Verificar simetría del nivel actual
            es_simetrico = self._nivel_es_simetrico(nodos_nivel)
            niveles.append({
                'nivel': nivel_actual,
                'simetrico': es_simetrico,
                'nodos': nodos_nivel
            })

            # Si todos los nodos del siguiente nivel son None, terminamos
            if all(nodo is None for nodo in siguiente_cola):
                break

            cola = siguiente_cola
            nivel_actual += 1

        return niveles

    def _nivel_es_simetrico(self, nodos_nivel):
        """
        Verifica si un array de nodos es simétrico.
        Compara posiciones espejo: primera con última, segunda con penúltima, etc.
        """
        n = len(nodos_nivel)
        for i in range(n // 2):
            # Dos posiciones son simétricas si ambas son None o ambas no-None
            if (nodos_nivel[i] is None) != (nodos_nivel[n-1-i] is None):
                return False
        return True
