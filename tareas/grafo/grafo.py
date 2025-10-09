"""
grafo.py
Autor: Lorgio Añez J.
Fecha: 2025-09-23

## Descripción

La clase `Grafo` implementa una estructura de datos de grafo 
con representación dual: **lista de adyacencia** y **matriz de adyacencia**.
Soporta tanto grafos **dirigidos** como **no dirigidos** 
y proporciona operaciones completas para la manipulación y consulta de grafos.

## Características Principales

- ✅ **Doble representación**: Lista y matriz de adyacencia
- ✅ **Soporte para grafos dirigidos y no dirigidos**
- ✅ **Operaciones CRUD completas** para vértices y aristas
- ✅ **Métodos getter y setter** en español
- ✅ **Validación de operaciones**
- ✅ **Métodos de visualización** integrados
- ✅ **Manejo de bucles** en grafos dirigidos

## Estructura de Datos

### Atributos de la Clase

| Atributo            | Tipo   | Descripción                         |
| ------------------- | ------ | ----------------------------------- |
| `vertices`          | `list` | Lista de nombres de vértices        |
| `dirigido`          | `bool` | Indica si el grafo es dirigido      |
| `lista_adyacencia`  | `dict` | Diccionario de listas de adyacencia |
| `matriz_adyacencia` | `list` | Matriz bidimensional de adyacencia  |

"""


class Grafo:
    def __init__(self, vertices=None, dirigido=False):
        """
        Inicializa el grafo
        Args:
            vertices: Lista de vértices (opcional)
            dirigido: Booleano que indica si el grafo es dirigido (default: False)
        """
        self.vertices = vertices if vertices else []
        self.dirigido = dirigido
        self.lista_adyacencia = {}
        self.matriz_adyacencia = []

        # Inicializar estructuras si se proporcionan vértices
        if self.vertices:
            self._inicializar_estructuras()

    def _inicializar_estructuras(self):
        """Inicializa la lista y matriz de adyacencia"""
        # Inicializar lista de adyacencia
        self.lista_adyacencia = {vertice: [] for vertice in self.vertices}

        # Inicializar matriz de adyacencia
        n = len(self.vertices)
        self.matriz_adyacencia = [[0] * n for _ in range(n)]

    # GETTERS
    def obtener_vertices(self):
        """Retorna la lista de vértices"""
        return self.vertices.copy()

    def es_dirigido(self):
        """Retorna si el grafo es dirigido"""
        return self.dirigido

    def obtener_lista_adyacencia(self):
        """Retorna una copia de la lista de adyacencia"""
        return {vertice: vecinos.copy() for vertice, vecinos in self.lista_adyacencia.items()}

    def obtener_matriz_adyacencia(self):
        """Retorna una copia de la matriz de adyacencia"""
        return [fila.copy() for fila in self.matriz_adyacencia]

    def obtener_indice_vertice(self, vertice):
        """Retorna el índice de un vértice en la matriz"""
        if vertice in self.vertices:
            return self.vertices.index(vertice)
        return -1

    def obtener_vecinos(self, vertice):
        """Retorna los vecinos de un vértice"""
        if vertice in self.lista_adyacencia:
            return self.lista_adyacencia[vertice].copy()
        return []

    def existe_arista(self, vertice1, vertice2):
        """Verifica si existe una arista entre dos vértices"""
        if vertice1 not in self.vertices or vertice2 not in self.vertices:
            return False

        idx1 = self.obtener_indice_vertice(vertice1)
        idx2 = self.obtener_indice_vertice(vertice2)

        return self.matriz_adyacencia[idx1][idx2] == 1

    def obtener_grado(self, vertice):
        """Retorna el grado de un vértice (número de aristas incidentes)"""
        if vertice not in self.lista_adyacencia:
            return 0
        return len(self.lista_adyacencia[vertice])

    # SETTERS
    def agregar_vertice(self, vertice):
        """Añade un nuevo vértice al grafo"""
        if vertice in self.vertices:
            return False

        self.vertices.append(vertice)

        # Actualizar lista de adyacencia
        self.lista_adyacencia[vertice] = []

        # Actualizar matriz de adyacencia
        n = len(self.vertices)

        # Añadir nueva columna a todas las filas existentes
        for fila in self.matriz_adyacencia:
            fila.append(0)

        # Añadir nueva fila
        self.matriz_adyacencia.append([0] * n)

        return True

    def eliminar_vertice(self, vertice):
        """Elimina un vértice del grafo"""
        if vertice not in self.vertices:
            return False

        idx = self.obtener_indice_vertice(vertice)

        # Remover de la lista de vértices
        self.vertices.remove(vertice)

        # Remover de la lista de adyacencia
        del self.lista_adyacencia[vertice]

        # Remover de todas las listas de adyacencia
        for v in self.lista_adyacencia:
            if vertice in self.lista_adyacencia[v]:
                self.lista_adyacencia[v].remove(vertice)

        # Remover de la matriz de adyacencia
        # Eliminar fila
        del self.matriz_adyacencia[idx]

        # Eliminar columna de cada fila
        for fila in self.matriz_adyacencia:
            del fila[idx]

        return True

    def agregar_arista(self, vertice1, vertice2, peso=1):
        """Añade una arista entre dos vértices"""
        if vertice1 not in self.vertices or vertice2 not in self.vertices:
            return False

        idx1 = self.obtener_indice_vertice(vertice1)
        idx2 = self.obtener_indice_vertice(vertice2)

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

    def eliminar_arista(self, vertice1, vertice2):
        """Elimina una arista entre dos vértices"""
        if vertice1 not in self.vertices or vertice2 not in self.vertices:
            return False

        idx1 = self.obtener_indice_vertice(vertice1)
        idx2 = self.obtener_indice_vertice(vertice2)

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

    # MÉTODOS DE VISUALIZACIÓN
    def imprimir_lista_adyacencia(self):
        """Imprime la lista de adyacencia"""
        print("Lista de Adyacencia:")
        for vertice in sorted(self.lista_adyacencia.keys()):
            vecinos = sorted(self.lista_adyacencia[vertice])
            print(f"{vertice}: {vecinos}")

    def imprimir_matriz_adyacencia(self):
        """Imprime la matriz de adyacencia"""
        print("Matriz de Adyacencia:")
        print("   ", end="")
        for vertice in self.vertices:
            print(f"{vertice:>3}", end="")
        print()

        for i, vertice in enumerate(self.vertices):
            print(f"{vertice}: ", end="")
            for j in range(len(self.vertices)):
                print(f"{self.matriz_adyacencia[i][j]:>3}", end="")
            print()

    def __str__(self):
        """Representación string del grafo"""
        return f"Grafo con {len(self.vertices)} vértices: {self.vertices}"


# Ejemplo de uso y pruebas
if __name__ == "__main__":
    # Crear un grafo no dirigido
    print("=== GRAFO NO DIRIGIDO ===")
    vertices = ['A', 'B', 'C', 'D']
    grafo = Grafo(vertices, dirigido=False)

    # Añadir aristas
    grafo.agregar_arista('A', 'B')
    grafo.agregar_arista('A', 'C')
    grafo.agregar_arista('B', 'C')
    grafo.agregar_arista('C', 'D')

    # Mostrar representaciones
    grafo.imprimir_lista_adyacencia()
    print()
    grafo.imprimir_matriz_adyacencia()
    print()

    # Probar getters
    print("Getters:")
    print(f"Vértices: {grafo.obtener_vertices()}")
    print(f"Es dirigido: {grafo.es_dirigido()}")
    print(f"Vecinos de 'A': {grafo.obtener_vecinos('A')}")
    print(f"Existe arista A-B: {grafo.existe_arista('A', 'B')}")
    print(f"Existe arista A-D: {grafo.existe_arista('A', 'D')}")
    print(f"Grado de 'C': {grafo.obtener_grado('C')}")
    print()

    # Probar setters
    print("Añadiendo vértice 'E' y arista C-E:")
    grafo.agregar_vertice('E')
    grafo.agregar_arista('C', 'E')
    grafo.imprimir_lista_adyacencia()
    print()

    print("Eliminando arista A-C:")
    grafo.eliminar_arista('A', 'C')
    grafo.imprimir_lista_adyacencia()
    print()

    # Crear un grafo dirigido
    print("\n=== GRAFO DIRIGIDO ===")
    grafo_dirigido = Grafo(['X', 'Y', 'Z'], dirigido=True)
    grafo_dirigido.agregar_arista('X', 'Y')
    grafo_dirigido.agregar_arista('Y', 'Z')
    grafo_dirigido.agregar_arista('Z', 'X')

    grafo_dirigido.imprimir_lista_adyacencia()
    print()
    grafo_dirigido.imprimir_matriz_adyacencia()
