README.md
Implementación Grafica del ADT Árbol Binario de Búsqueda
Autor: Lorgio Añez J.
Fecha: 2025-09-22
Descripción: AplicaciOn que representa un árbol binario con métodos para insertar, buscar, eliminar, recorrer nodos, etc. La representacion del Arbol
se realiza graficamente en una aplicacin WEB, con arquitectura MVC.
Materia: Estructura de Datos II, INF310

## Tarea Unidad 1: Crear interfaz grafica

Requisitos de finalización

Apertura: martes, 2 de septiembre de 2025, 07:00
Cierre: jueves, 11 de septiembre de 2025, 07:00
Realizar la implementacion de una inteface graphics para la representacion de un Arbol Binario.

- La representacion grafica se la tiene que realizar en interfaz web, empleando flask, html, css.
  El proyecto ya fue subido a github para que sirva como base.

Nota: Crear un ambiente grafico que permita llamar a metodos de la clase arbol archivo ZIP.

# Resumen de Funcionalidades - Visualizador de Árboles Binarios

## 📊 MÉTODOS DEL ÁRBOL BINARIO

### Inserción

insertar_nodo(x): Agrega un nodo con valor x (evita duplicados)
\_insertar(): Método auxiliar recursivo para inserción

### Eliminación

eliminar_nodo(x): Elimina un nodo específico manteniendo la estructura BST
eliminar_rama(x): Elimina un nodo y toda su descendencia
\_eliminar(): Método auxiliar para eliminación con reemplazo por sucesor

### Búsqueda

buscar_x(x): Encuentra un nodo por su valor
\_buscar(): Búsqueda recursiva auxiliar

### Recorridos

in_orden(): Izquierdo - Raíz - Derecho (ordenado)
pre_orden(): Raíz - Izquierdo - Derecho
post_orden(): Izquierdo - Derecho - Raíz
amplitud(): Por niveles (usando cola)

### Información

altura(): Calcula la altura máxima del árbol
contar_nodos(): Total de nodos en el árbol
contar_hojas(): Nodos sin hijos
es_vacio(): Verifica si el árbol está vacío
es_hoja(): Verifica si un nodo es hoja

## 🎮 INTERFAZ WEB - BOTONES PRINCIPALES

### Panel Izquierdo - Operaciones

🌱 INSERTAR NODO → Agrega nodo individual
📦 INSERTAR SERIE → Agrega múltiples nodos (ej: "5 3 7")
🗑️ ELIMINAR NODO → Elimina nodo específico
🌿 ELIMINAR RAMA → Elimina nodo y toda su descendencia
🔍 BUSCAR NODO → Encuentra y resalta nodo

#### Recorridos

🔄 INORDEN → Muestra valores ordenados
🔄 PREORDEN → Raíz primero  
🔄 POSTORDEN → Raíz al final
🔄 AMPLITUD → Por niveles

#### Utilidades

🗑️ LIMPIAR ÁRBOL → Reinicia el árbol completo
🎲 ÁRBOL ALEATORIO → Genera árbol con valores random
⚖️ VERIFICAR BALANCE → Chequea balance AVL
🚪 SALIR → Cierra la aplicación

## 🔄 FLUJO DE LA APLICACIÓN

- Usuario interactúa con botones/inputs
- JavaScript envía petición al servidor Flask
- Controlador procesa y modifica el árbol
- Modelo actualiza la estructura del árbol
- JavaScript recibe respuesta y actualiza visualización
- SVG se redibuja automáticamente

### 💾 ALMACENAMIENTO

Memoria del servidor: El árbol persiste durante la sesión
Sin base de datos: No hay persistencia entre reinicios
Una instancia global: Todos los usuarios ven el mismo árbol

### 🎨 VISUALIZACIÓN

- SVG dinámico: Se genera automáticamente
- Nodos circulares con valores numéricos
- Líneas conectadas mostrando parentesco
- Colores diferenciados: Normal, encontrado, eliminado
- Animaciones suaves al insertar/eliminar

### ⚡ CARACTERÍSTICAS TÉCNICAS

- Arquitectura MVC (Modelo-Vista-Controlador)
- Backend: Flask (Python)
- Frontend: HTML5, CSS3, JavaScript vanilla
- Comunicación: API REST JSON
- Visualización: SVG nativo
