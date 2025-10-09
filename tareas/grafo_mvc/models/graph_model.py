"""
models/graph_model.py
Autor: Lorgio Añez J.
Fecha: 2025-10-09

Propósito: Representar la estructura de datos del grafo (Modelo en MVC)
Responsabilidad: Gestionar los datos y operaciones del grafo
Clase Principal: GraphModel

❌ NO sabe sobre la interfaz de usuario
❌ NO maneja entrada/salida directa
✅ SI gestiona la estructura de datos
✅ SI valida operaciones internas

Atributos:

-   vertices: Lista de vértices del grafo
-   dirigido: Booleano que indica si el grafo es dirigido
-   lista_adyacencia: Diccionario con las conexiones entre vértices
-   matriz_adyacencia: Matriz que representa las conexiones

Métodos Principales:

-   agregar_vertice(vertice): Añade un nuevo vértice
-   eliminar_vertice(vertice): Elimina un vértice y sus conexiones
-   agregar_arista(vertice1, vertice2): Crea una conexión entre vértices
-   eliminar_arista(vertice1, vertice2): Elimina una conexión
-   obtener_datos_grafo(): Retorna todos los datos para la vista
-   obtener_vertices(), obtener_lista_adyacencia(), etc.: Getters

"""


class GraphModel:
    def __init__(self, vertices=None, dirigido=False):
        """
        Modelo que representa la estructura de datos del grafo
        """
        self.vertices = vertices if vertices else []  # Lista de vértices
        self.dirigido = dirigido        # Booleano para tipo
        self.lista_adyacencia = {}      # Diccionario de listas
        self.matriz_adyacencia = []     # Lista de listas (matriz)

        if self.vertices:
            self._inicializar_estructuras()

    def _inicializar_estructuras(self):
        """Inicializa las estructuras de adyacencia"""
        self.lista_adyacencia = {vertice: [] for vertice in self.vertices}
        n = len(self.vertices)
        self.matriz_adyacencia = [[0] * n for _ in range(n)]

    # Operaciones de datos
    def agregar_vertice(self, vertice):
        if vertice in self.vertices:
            return False

        self.vertices.append(vertice)
        self.lista_adyacencia[vertice] = []

        # Actualizar matriz
        n = len(self.vertices)
        for fila in self.matriz_adyacencia:
            fila.append(0)
        self.matriz_adyacencia.append([0] * n)
        return True

    def eliminar_vertice(self, vertice):
        if vertice not in self.vertices:
            return False

        idx = self.vertices.index(vertice)
        self.vertices.remove(vertice)
        del self.lista_adyacencia[vertice]

        # Eliminar de otras listas de adyacencia
        for v in self.lista_adyacencia:
            if vertice in self.lista_adyacencia[v]:
                self.lista_adyacencia[v].remove(vertice)

        # Actualizar matriz
        del self.matriz_adyacencia[idx]
        for fila in self.matriz_adyacencia:
            del fila[idx]

        return True

    def agregar_arista2(self, vertice1, vertice2, peso=1):
        if vertice1 not in self.vertices or vertice2 not in self.vertices:
            return False

        idx1 = self.vertices.index(vertice1)
        idx2 = self.vertices.index(vertice2)

        # Actualizar lista de adyacencia
        if vertice2 not in self.lista_adyacencia[vertice1]:
            self.lista_adyacencia[vertice1].append(vertice2)

        if not self.dirigido and vertice1 not in self.lista_adyacencia[vertice2]:
            self.lista_adyacencia[vertice2].append(vertice1)

        # Actualizar matriz de adyacencia
        self.matriz_adyacencia[idx1][idx2] = peso
        if not self.dirigido:
            self.matriz_adyacencia[idx2][idx1] = peso

        return True

    def agregar_arista(self, vertice1, vertice2, peso=1):
        if vertice1 not in self.vertices or vertice2 not in self.vertices:
            return False

        idx1 = self.vertices.index(vertice1)
        idx2 = self.vertices.index(vertice2)

        # Actualizar lista de adyacencia
        if vertice2 not in self.lista_adyacencia[vertice1]:
            self.lista_adyacencia[vertice1].append(vertice2)

        # En grafos no dirigidos, agregar la arista recíproca (excepto para bucles)
        if not self.dirigido and vertice1 != vertice2 and vertice1 not in self.lista_adyacencia[vertice2]:
            self.lista_adyacencia[vertice2].append(vertice1)

        # Actualizar matriz de adyacencia
        self.matriz_adyacencia[idx1][idx2] = peso
        if not self.dirigido and vertice1 != vertice2:
            self.matriz_adyacencia[idx2][idx1] = peso

        return True

    def eliminar_arista(self, vertice1, vertice2):
        if vertice1 not in self.vertices or vertice2 not in self.vertices:
            return False

        idx1 = self.vertices.index(vertice1)
        idx2 = self.vertices.index(vertice2)

        # Actualizar lista de adyacencia
        if vertice2 in self.lista_adyacencia[vertice1]:
            self.lista_adyacencia[vertice1].remove(vertice2)

        if not self.dirigido and vertice1 in self.lista_adyacencia[vertice2]:
            self.lista_adyacencia[vertice2].remove(vertice1)

        # Actualizar matriz de adyacencia
        self.matriz_adyacencia[idx1][idx2] = 0
        if not self.dirigido:
            self.matriz_adyacencia[idx2][idx1] = 0

        return True

    # Métodos de consulta
    def obtener_vertices(self):
        return self.vertices.copy()

    def obtener_lista_adyacencia(self):
        return {v: n.copy() for v, n in self.lista_adyacencia.items()}

    def obtener_matriz_adyacencia(self):
        return [fila.copy() for fila in self.matriz_adyacencia]

    def obtener_vecinos(self, vertice):
        return self.lista_adyacencia.get(vertice, []).copy()

    def existe_arista(self, vertice1, vertice2):
        if vertice1 not in self.vertices or vertice2 not in self.vertices:
            return False
        idx1 = self.vertices.index(vertice1)
        idx2 = self.vertices.index(vertice2)
        return self.matriz_adyacencia[idx1][idx2] == 1

    def obtener_grado(self, vertice):
        return len(self.lista_adyacencia.get(vertice, []))

    def es_dirigido(self):
        return self.dirigido

    def obtener_datos_grafo(self):
        """Retorna todos los datos del grafo para las vistas"""
        return {
            'vertices': self.obtener_vertices(),
            'lista_adyacencia': self.obtener_lista_adyacencia(),
            'matriz_adyacencia': self.obtener_matriz_adyacencia(),
            'dirigido': self.dirigido
        }
