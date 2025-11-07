# 🌳 Visualizador Interactivo de Árbol Binario

**Autor:** Lorgio Añez J.  
**Fecha:** 2025-09-23  
**Materia:** Estructura de Datos II, INF310

## 🚀 Demo en Vivo

[**🌐 Visitar la Aplicación Web**](https://lorginho.pythonanywhere.com/)

## 📋 Descripción

Aplicación web interactiva que representa visualmente un **Árbol Binario de Búsqueda** con arquitectura MVC. Permite operaciones completas sobre el árbol con visualización gráfica en tiempo real usando SVG.

## 📸 Galería de Interfaces

![Árbol Binario Normal](image.png)
![Análisis de Simetría](arbol_no_simetrico.png)

## ✨ Características Principales

### 🔧 Operaciones Básicas

- **🌱 Inserción** individual y por series
- **🗑️ Eliminación** de nodos y ramas completas
- **🔍 Búsqueda** con resaltado visual
- **🔄 Recorridos**: Inorden, Preorden, Postorden, Por Niveles

### 📊 Análisis Avanzado

- **🔄 Verificación de Simetría** - Estructural y por niveles
- **⚖️ Balanceo AVL** - Verificación y balanceo automático
- **📈 Estadísticas** en tiempo real (altura, nodos, hojas)

### 🎨 Visualización

- **🎨 SVG Dinámico** con colores por estado
- **📱 Interfaz Responsiva** con tres paneles
- **✨ Animaciones Suaves** para todas las operaciones
- **🎯 Coloreado por niveles** para análisis de simetría

## 🛠️ Stack Tecnológico

| Capa              | Tecnología                      |
| ----------------- | ------------------------------- |
| **Backend**       | Flask (Python)                  |
| **Frontend**      | HTML5, CSS3, JavaScript Vanilla |
| **Visualización** | SVG Nativo                      |
| **Arquitectura**  | MVC (Modelo-Vista-Controlador)  |
| **API**           | REST JSON                       |

## 🎮 Panel de Control Completo

### 📥 Operaciones de Entrada

| Botón               | Función                             |
| ------------------- | ----------------------------------- |
| `🌱 INSERTAR NODO`  | Agrega nodo individual              |
| `📦 INSERTAR SERIE` | Múltiples nodos (ej: "5 3 7 2 4")   |
| `🗑️ ELIMINAR NODO`  | Elimina nodo específico             |
| `🌿 ELIMINAR RAMA`  | Elimina nodo y toda su descendencia |
| `🔍 BUSCAR NODO`    | Encuentra y resalta nodo            |

### 🔄 Recorridos Disponibles

| Tipo           | Orden                                 |
| -------------- | ------------------------------------- |
| `🔄 INORDEN`   | Izquierdo - Raíz - Derecho (ordenado) |
| `🔄 PREORDEN`  | Raíz - Izquierdo - Derecho            |
| `🔄 POSTORDEN` | Izquierdo - Derecho - Raíz            |
| `🔄 AMPLITUD`  | Por niveles (BFS)                     |

### ⚡ Utilidades Avanzadas

| Función                   | Descripción                     |
| ------------------------- | ------------------------------- |
| `⚖️ VERIFICAR BALANCE`    | Chequea balance AVL             |
| `⚖️ BALANCEAR ÁRBOL`      | Reconstruye a altura mínima     |
| `🔄 VERIFICAR SIMETRÍA`   | Análisis estructural completo   |
| `📊 SIMETRÍA POR NIVELES` | Análisis nivel por nivel        |
| `🎲 ÁRBOL ALEATORIO`      | Genera árbol con valores random |
| `🗑️ LIMPIAR ÁRBOL`        | Reinicia completamente          |
| `🚪 SALIR`                | Cierra la aplicación            |

## 🏗️ Arquitectura del Sistema

### 📁 Estructura de Proyecto

arbol_grafico/
├── 🐍 app.py
├── 🎮 controllers/arbol_controller.py
├── 🧠 models/arbol_binario.py
├── 🧠 models/nodo.py
├── 👁️ templates/index.html
└── 🎨 static/
├── css/style.css
└── js/script.js

### 🔄 Flujo de Datos MVC

1. **👤 Usuario** → Interactúa con la vista
2. **🎮 JavaScript** → Captura eventos y llama API
3. **🐍 Controlador Flask** → Procesa endpoints REST
4. **🧠 Modelo Árbol** → Ejecuta operaciones
5. **📡 Respuesta JSON** → Datos actualizados
6. **🎨 SVG Dinámico** → Actualiza visualización

## 💻 Métodos Implementados

### ⚡ Operaciones Principales

`insertar_nodo(x)` | `eliminar_nodo(x)` | `buscar_x(x)` | `eliminar_rama(x)`

### 📊 Análisis y Recorridos

`in_orden()` | `pre_orden()` | `post_orden()` | `amplitud()` | `altura()` | `contar_nodos()` | `contar_hojas()`

### 🔬 Funcionalidades Avanzadas

`esta_balanceado()` | `forzar_balanceo()` | `es_simetrico()` | `obtener_niveles_simetria()`

## 🎯 Casos de Uso Detallados

### 📥 Proceso de Inserción

1. **👤 Usuario** ingresa valor
2. **🎮 Frontend** envía `POST /insertar`
3. **🐍 Backend** valida e inserta
4. **🧠 Modelo** coloca nodo BST
5. **📡 Respuesta** confirma
6. **🎨 SVG** redibuja

### 🔍 Proceso de Búsqueda

1. **👤 Usuario** ingresa valor
2. **🎮 Frontend** envía `POST /buscar`
3. **🧠 Modelo** búsqueda recursiva
4. **📡 Respuesta** resultado
5. **🎨 SVG** resalta nodo

### ⚖️ Proceso de Balanceo AVL

1. **👤 Usuario** presiona "VERIFICAR BALANCE"
2. **🐍 Backend** calcula factores equilibrio
3. **📡 Respuesta** estado balance
4. **👤 Usuario** opción "BALANCEAR"
5. **🧠 Modelo** reconstruye árbol

### 🔄 Análisis de Simetría por Niveles

1. **👤 Usuario** presiona "VER SIMETRÍA POR NIVELES"
2. **🧠 Modelo** analiza cada nivel
3. **🎨 Frontend** colorea nodos: 🟢 **VERDE** (simétrico), 🔴 **ROJO** (asimétrico)
4. **📊 Panel** reporte detallado

## 🚀 Características Técnicas Destacadas

### ⚡ Optimizaciones

- **Algoritmo O(1)** para coloreado con `Map()`
- **Búsqueda eficiente** con mapa niveles
- **Manejo de estado** optimizado

### 🎨 Visualización

- **SVG Nativo** escalado vectorial
- **Colores semánticos** por estado
- **Responsive design** CSS Grid/Flexbox
- **Transiciones suaves**

### 🔧 Robustez

- **Validación completa** inputs
- **Manejo de errores** frontend/backend
- **Prevención duplicados**
- **API RESTful** estandarizada
