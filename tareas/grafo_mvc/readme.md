# Sistema de Grafos con Arquitectura MVC

## Descripción

Un sistema completo para la gestión y visualización de grafos implementado en Python con arquitectura MVC (Modelo-Vista-Controlador) y programación orientada a objetos.

## Características Principales

- ✅ **Arquitectura MVC** - Separación clara de responsabilidades
- ✅ **Grafos Dirigidos y No Dirigidos** - Soporte completo para ambos tipos
- ✅ **Doble Representación** - Matriz y lista de adyacencia
- ✅ **Población Aleatoria** - Generación automática de grafos
- ✅ **Operaciones CRUD** - Crear, leer, actualizar y eliminar vértices y aristas
- ✅ **Manejo de Bucles** - Soporte para self-loops en grafos dirigidos
- ✅ **Validación de Datos** - Verificación de operaciones válidas

## Estructura del Proyecto

```
grafo_mvc/
├── models/
│   └── graph_model.py          # Modelo de datos del grafo
├── views/
│   └── graph_view.py           # Interfaz de usuario
├── controllers/
│   └── graph_controller.py     # Lógica de aplicación
├── main.py                     # Punto de entrada
└── README.md                   # Esta documentación
```

## Instalación y Ejecución

### Requisitos

- Python 3.6 o superior
- No se requieren dependencias externas

### Ejecución

```bash
python main.py
```

## Funcionalidades

### Operaciones Básicas

1. **Agregar Vértice** - Añadir nuevos vértices al grafo
2. **Eliminar Vértice** - Remover vértices y sus conexiones
3. **Agregar Arista** - Conectar vértices entre sí
4. **Eliminar Arista** - Remover conexiones entre vértices
5. **Mostrar Lista de Adyacencia** - Representación en lista
6. **Mostrar Matriz de Adyacencia** - Representación matricial
7. **Mostrar Información del Grafo** - Estadísticas completas

### Funcionalidades Avanzadas

8. **Cambiar Tipo de Grafo** - Intercambiar entre dirigido/no dirigido
9. **Limpiar Grafo** - Reiniciar el grafo actual
10. **Poblar Grafo Aleatoriamente** - Generación automática
11. **Salir** - Terminar la aplicación

## Ejemplos de Uso

### Crear un Grafo Manualmente

```
=== SISTEMA GRAFOS MVC (Grafo no dirigido) ===
Seleccione opción (1-11): 1
Ingrese vértice a agregar: A
ÉXITO: Vértice 'A' agregado exitosamente

Seleccione opción (1-11): 3
Ingrese primer vértice: A
Ingrese segundo vértice: B
ÉXITO: Arista no dirigida (A - B) agregada exitosamente
```

### Poblar Grafo Aleatoriamente

```
Seleccione opción (1-11): 10
=== POBLAR GRAFO ALEATORIAMENTE ===
Número de vértices (3-15): 5
Número de aristas (0-20): 8
Vértices creados: 5
Aristas creadas: 0
...
ÉXITO: Grafo poblado con 5 vértices y 8 aristas
```

### Grafo Dirigido con Bucles

```
=== SISTEMA GRAFOS MVC (Grafo dirigido) ===
Seleccione opción (1-11): 3
Ingrese primer vértice: A
Ingrese segundo vértice: A
ÉXITO: Bucle dirigido (A ↺) agregado exitosamente
```

## Representaciones del Grafo

### Lista de Adyacencia

```
--- LISTA DE ADYACENCIA ---
A: ['B', 'C']
B: ['A', 'D']
C: ['A']
D: ['B']
```

### Matriz de Adyacencia

```
--- MATRIZ DE ADYACENCIA ---
     A  B  C  D
A:   0  1  1  0
B:   1  0  0  1
C:   1  0  0  0
D:   0  1  0  0
```

## Características Técnicas

### Modelo (GraphModel)

- Almacenamiento dual: lista y matriz de adyacencia
- Validación de operaciones
- Cálculo de grados y conexiones
- Soporte para grafos dirigidos y bucles

### Vista (GraphView)

- Formateo de salidas
- Entrada y validación de datos
- Mensajes de feedback

### Controlador (GraphController)

- Coordinación entre modelo y vista
- Lógica de aplicación
- Manejo de excepciones
- Generación aleatoria

## Algoritmos de Generación Aleatoria

### Población Básica

- Genera vértices con nombres únicos (A-Z o V1,V2,...)
- Crea aristas aleatorias evitando duplicados
- Respeta las propiedades del tipo de grafo
- Límites seguros para evitar sobrecarga

## Manejo de Errores

- Validación de vértices existentes
- Prevención de bucles en grafos no dirigidos
- Límites en generación aleatoria
- Mensajes de error descriptivos

## Extensibilidad

El sistema está diseñado para ser extendido fácilmente:

- **Nuevos Algoritmos**: BFS, DFS, Dijkstra, etc.
- **Persistencia**: Guardar/cargar grafos desde archivos
- **Visualización**: Gráficos interactivos
- **Métricas Avanzadas**: Centralidad, conectividad, etc.

---

**¡Listo para usar!** Ejecuta `python main.py` para comenzar.
