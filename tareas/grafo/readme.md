# Documentación de la Clase `Grafo`

## Descripción

La clase `Grafo` implementa una estructura de datos de grafo con representación dual: **lista de adyacencia** y **matriz de adyacencia**. Soporta tanto grafos **dirigidos** como **no dirigidos** y proporciona operaciones completas para la manipulación y consulta de grafos.

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

### Ejemplo de Estructuras

**Lista de Adyacencia:**

```python
{
    'A': ['B', 'C'],
    'B': ['A', 'D'],
    'C': ['A'],
    'D': ['B']
}
```

**Matriz de Adyacencia:**

```python
[
    [0, 1, 1, 0],  # A
    [1, 0, 0, 1],  # B
    [1, 0, 0, 0],  # C
    [0, 1, 0, 0]   # D
]
```

## Constructor

```python
def __init__(self, vertices=None, dirigido=False)
```

**Parámetros:**

- `vertices` (opcional): Lista inicial de vértices
- `dirigido` (default: False): Booleano que indica si el grafo es dirigido

**Ejemplo:**

```python
# Grafo no dirigido
grafo1 = Grafo(['A', 'B', 'C'], dirigido=False)

# Grafo dirigido vacío
grafo2 = Grafo(dirigido=True)
```

## Métodos Públicos

### Métodos Getter

#### `obtener_vertices()`

Retorna una copia de la lista de vértices.

**Retorna:** `list` - Lista de vértices

#### `es_dirigido()`

Verifica si el grafo es dirigido.

**Retorna:** `bool` - True si es dirigido, False en caso contrario

#### `obtener_lista_adyacencia()`

Retorna una copia profunda de la lista de adyacencia.

**Retorna:** `dict` - Diccionario con la lista de adyacencia

#### `obtener_matriz_adyacencia()`

Retorna una copia profunda de la matriz de adyacencia.

**Retorna:** `list` - Matriz de adyacencia 2D

#### `obtener_indice_vertice(vertice)`

Obtiene el índice de un vértice en la matriz.

**Parámetros:**

- `vertice`: Nombre del vértice a buscar

**Retorna:** `int` - Índice del vértice o -1 si no existe

#### `obtener_vecinos(vertice)`

Retorna los vértices adyacentes a un vértice dado.

**Parámetros:**

- `vertice`: Vértice del cual obtener los vecinos

**Retorna:** `list` - Lista de vértices vecinos

#### `existe_arista(vertice1, vertice2)`

Verifica si existe una arista entre dos vértices.

**Parámetros:**

- `vertice1`: Primer vértice
- `vertice2`: Segundo vértice

**Retorna:** `bool` - True si existe la arista

#### `obtener_grado(vertice)`

Calcula el grado (número de aristas incidentes) de un vértice.

**Parámetros:**

- `vertice`: Vértice del cual calcular el grado

**Retorna:** `int` - Grado del vértice

### Métodos Setter

#### `agregar_vertice(vertice)`

Añade un nuevo vértice al grafo.

**Parámetros:**

- `vertice`: Nombre del nuevo vértice

**Retorna:** `bool` - True si se agregó exitosamente

#### `eliminar_vertice(vertice)`

Elimina un vértice y todas sus aristas incidentes.

**Parámetros:**

- `vertice`: Vértice a eliminar

**Retorna:** `bool` - True si se eliminó exitosamente

#### `agregar_arista(vertice1, vertice2, peso=1)`

Crea una arista entre dos vértices.

**Parámetros:**

- `vertice1`: Primer vértice
- `vertice2`: Segundo vértice
- `peso` (opcional): Peso de la arista (default: 1)

**Retorna:** `bool` - True si se creó exitosamente

#### `eliminar_arista(vertice1, vertice2)`

Elimina una arista entre dos vértices.

**Parámetros:**

- `vertice1`: Primer vértice
- `vertice2`: Segundo vértice

**Retorna:** `bool` - True si se eliminó exitosamente

### Métodos de Visualización

#### `imprimir_lista_adyacencia()`

Imprime la lista de adyacencia en formato legible.

**Salida:**

```
Lista de Adyacencia:
A: ['B', 'C']
B: ['A', 'D']
C: ['A']
D: ['B']
```

#### `imprimir_matriz_adyacencia()`

Imprime la matriz de adyacencia en formato tabular.

**Salida:**

```
Matriz de Adyacencia:
     A  B  C  D
A:   0  1  1  0
B:   1  0  0  1
C:   1  0  0  0
D:   0  1  0  0
```

## Métodos Protegidos

### `_inicializar_estructuras()`

Inicializa las estructuras de datos internas cuando se proporcionan vértices en el constructor.

## Ejemplos de Uso

### Ejemplo 1: Grafo No Dirigido

```python
# Crear grafo no dirigido
grafo = Grafo(['A', 'B', 'C'], dirigido=False)

# Agregar aristas
grafo.agregar_arista('A', 'B')
grafo.agregar_arista('B', 'C')

# Consultar información
print(f"Vértices: {grafo.obtener_vertices()}")
print(f"Vecinos de B: {grafo.obtener_vecinos('B')}")
print(f"Existe A-C: {grafo.existe_arista('A', 'C')}")

# Visualizar
grafo.imprimir_lista_adyacencia()
grafo.imprimir_matriz_adyacencia()
```

### Ejemplo 2: Grafo Dirigido con Bucles

```python
# Crear grafo dirigido
grafo_dirigido = Grafo(['X', 'Y', 'Z'], dirigido=True)

# Agregar aristas dirigidas
grafo_dirigido.agregar_arista('X', 'Y')
grafo_dirigido.agregar_arista('Y', 'Z')
grafo_dirigido.agregar_arista('Z', 'Z')  # Bucle

# Verificar direccionalidad
print(f"Es dirigido: {grafo_dirigido.es_dirigido()}")
```

### Ejemplo 3: Operaciones Dinámicas

```python
# Crear grafo vacío
grafo = Grafo()

# Agregar vértices dinámicamente
grafo.agregar_vertice('A')
grafo.agregar_vertice('B')
grafo.agregar_vertice('C')

# Modificar estructura
grafo.agregar_arista('A', 'B')
grafo.agregar_arista('B', 'C')
grafo.eliminar_vertice('B')
```

## Consideraciones de Diseño

### Representación Dual

La clase mantiene ambas representaciones simultáneamente para:

- **Lista de adyacencia**: Eficiente para grafos dispersos y consulta de vecinos
- **Matriz de adyacencia**: Rápida para verificación de aristas y algoritmos matriciales

### Inmutabilidad

Los métodos getter retornan **copias** de las estructuras internas para prevenir modificaciones accidentales.

### Validación

Todas las operaciones validan la existencia de vértices antes de ejecutarse.

## Complejidades de Tiempo

| Operación            | Lista Adyacencia | Matriz Adyacencia |
| -------------------- | ---------------- | ----------------- |
| `agregar_vertice()`  | O(1)             | O(n²)             |
| `eliminar_vertice()` | O(V + E)         | O(n²)             |
| `agregar_arista()`   | O(1)             | O(1)              |
| `eliminar_arista()`  | O(k)             | O(1)              |
| `existe_arista()`    | O(k)             | O(1)              |
| `obtener_vecinos()`  | O(1)             | O(n)              |

Donde:

- **V**: Número de vértices
- **E**: Número de aristas
- **k**: Grado del vértice
- **n**: Número total de vértices

## Uso Avanzado

La clase es adecuada para:

- **Algoritmos de grafos** (BFS, DFS, Dijkstra, etc.)
- **Análisis de redes** sociales y de conectividad
- **Sistemas de recomendación**
- **Simulaciones y modelado**

## Notas Importantes

- Los bucles (self-loops) están permitidos solo en grafos dirigidos
- En grafos no dirigidos, las aristas son bidireccionales automáticamente
- Los nombres de vértices deben ser únicos
- La clase no soporta aristas múltiples entre el mismo par de vértices

Esta documentación cubre todos los aspectos esenciales de la clase `Grafo` para su uso efectivo en aplicaciones que requieran manipulación y análisis de estructuras de grafos.
