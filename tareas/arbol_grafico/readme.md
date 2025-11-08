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
- **🔄 Recorridos Animados**: Inorden, Preorden, Postorden, Por Niveles con visualización secuencial

### 📊 Análisis Avanzado

- **🔄 Verificación de Simetría** - Estructural y por niveles
- **⚖️ Balanceo AVL** - Verificación y balanceo automático
- **📈 Estadísticas** en tiempo real (altura, nodos, hojas)

### 🎨 Visualización

- **🎨 SVG Dinámico** con colores por estado
- **📱 Interfaz Responsiva** con tres paneles
- **✨ Recorridos Animados** - Nodos se iluminan en orden de visita
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
| `🌳 MOSTRAR ÁRBOL`  | Restablece vista a colores normales |

### 🔄 Recorridos Animados

| Tipo           | Comportamiento                                              |
| -------------- | ----------------------------------------------------------- |
| `🔄 INORDEN`   | Muestra lista + anima nodos en orden izquierdo-raíz-derecho |
| `🔄 PREORDEN`  | Muestra lista + anima nodos en orden raíz-izquierdo-derecho |
| `🔄 POSTORDEN` | Muestra lista + anima nodos en orden izquierdo-derecho-raíz |
| `🔄 AMPLITUD`  | Muestra lista + anima nodos por niveles                     |

### ⚡ Utilidades Avanzadas

| Función                   | Descripción                            |
| ------------------------- | -------------------------------------- |
| `⚖️ VERIFICAR BALANCE`    | Chequea balance AVL                    |
| `⚖️ BALANCEAR ÁRBOL`      | Reconstruye a altura mínima            |
| `🔄 VERIFICAR SIMETRÍA`   | Análisis estructural completo          |
| `📊 SIMETRÍA POR NIVELES` | Análisis nivel por nivel con coloreado |
| `🎲 ÁRBOL ALEATORIO`      | Genera árbol con valores random        |
| `🗑️ LIMPIAR ÁRBOL`        | Reinicia completamente                 |
| `🚪 SALIR`                | Cierra la aplicación                   |

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

## 🎯 Casos de Uso Destacados

### 🔄 Recorridos Animados

- **Un solo click** muestra lista ordenada + animación visual
- **Nodos visitados** se mantienen en verde permanente
- **Nodo actual** se resalta en naranja durante cada paso
- **Máximo valor educativo** para entender algoritmos

### 🎨 Análisis de Simetría

- **Coloreado inteligente** por niveles (🟢 VERDE = simétrico, 🔴 ROJO = asimétrico)
- **Reporte detallado** nivel por nivel en panel de resultados
- **Visualización inmediata** de estructura del árbol

### ⚡ Optimizaciones de Rendimiento

- **Algoritmo O(1)** para coloreado usando Map()
- **Búsqueda eficiente** con mapa de niveles
- **Manejo de estado** optimizado y centralizado

## 🚀 Instalación y Desarrollo

```bash
git clone [url-repositorio]
cd arbol_grafico
python app.py
# http://localhost:5000
```
