README.md

- Implementación Visual de un ADT Grafo (grafo_rutas) a traves de una aplicacion Flask de Mapa de Rutas
- Autor: `Lorgio Añez J.`
- Fecha: 2025-10-23
- Descripción:
- Materia: Estructura de Datos II, INF310

![alt text](sistema_rutas.png)

✅ RESUMEN DE LO IMPLEMENTADO:
🏗️ ARQUITECTURA MVC:
✅ app.py - Controlador principal (rutas Flask)

✅ controllers/mapa_controller.py - Lógica de aplicación

✅ models/grafo_rutas.py - Datos + Algoritmos (Dijkstra)

✅ views/mapa_view.py - Formateo de respuestas

✅ templates/mapa.html - Vista principal

✅ static/rutas.js - Frontend interactivo

✅ static/estilo.css - Estilos profesionales

🛠️ FUNCIONALIDADES COMPLETAS:
✅ Visualizar mapa con ciudades y rutas

✅ Calcular rutas óptimas (Dijkstra con animación)

✅ Agregar/Eliminar ciudades

✅ Agregar/Eliminar rutas

✅ Interfaz responsive (3 columnas)

✅ Validaciones y manejo de errores

🎨 INTERFAZ DE USUARIO:
✅ Sidebar izquierdo - Controles y formularios

✅ Centro - Mapa SVG interactivo

✅ Sidebar derecho - Listas de ciudades/rutas + resultados

✅ Botones eliminar en listas

✅ Estados en tiempo real

🗺️ Sistema de Rutas de Bolivia - Documentación Técnica
📋 Tabla de Contenidos
Descripción del Proyecto

Características Principales

Arquitectura del Sistema

Instalación y Configuración

Estructura de Archivos

API Endpoints

Algoritmos Implementados

Guía de Uso

Tecnologías Utilizadas

Desarrollo y Contribución

🎯 Descripción del Proyecto
Sistema de Rutas de Bolivia es una aplicación web interactiva desarrollada en Flask que permite visualizar, gestionar y calcular rutas óptimas entre ciudades bolivianas utilizando algoritmos de grafos. El sistema implementa una arquitectura MVC (Modelo-Vista-Controlador) profesional y ofrece una interfaz de usuario intuitiva con visualización SVG en tiempo real.

🎯 Objetivos del Proyecto
Proporcionar una herramienta educativa para el estudio de algoritmos de grafos

Demostrar la implementación del patrón MVC en Python/Flask

Ofrecer una interfaz visual interactiva para la gestión de rutas

Implementar algoritmos clásicos de búsqueda de caminos (Dijkstra)

✨ Características Principales
🗺️ Visualización
Mapa SVG interactivo de 1600x1200 píxeles

Ciudades representadas como nodos circulares con colores de la bandera boliviana

Rutas visualizadas como líneas con distancias en kilómetros

Diseño responsive con paneles laterales ajustables

Bordes distintivos y fondos personalizados

🔧 Funcionalidades de Gestión
✅ Agregar ciudades: Por formulario o click directo en el mapa

✅ Eliminar ciudades: Con confirmación y eliminación en cascada de rutas

✅ Agregar rutas: Entre ciudades existentes con pesos personalizables

✅ Eliminar rutas: Desde la lista interactiva

✅ Cálculo de rutas óptimas: Algoritmo Dijkstra con animación visual

🎨 Experiencia de Usuario
Interfaz intuitiva con tres paneles organizados

Animaciones en tiempo real del algoritmo Dijkstra

Validaciones robustas en frontend y backend

Mensajes de estado informativos

Listas ordenadas alfabéticamente

🏗️ Arquitectura del Sistema
📐 Patrón MVC Implementado
text
sistema_rutas/
├── 🎮 Controlador (controllers/)
│ └── mapa_controller.py
├── 📊 Modelo (models/)
│ └── grafo_rutas.py
├── 🎨 Vista (views/)
│ └── mapa_view.py
├── 🌐 Frontend (templates/, static/)
│ ├── mapa.html
│ ├── rutas.js
│ └── estilo.css
└── 🚀 Punto de Entrada
└── app.py
🔄 Flujo de Datos
text
Usuario → app.py (Rutas) → MapaController → GrafoRutas (Modelo)
↓
MapaView (Vista) → Respuesta JSON/HTML
🛠️ Instalación y Configuración
Prerrequisitos
Python 3.8+

pip (gestor de paquetes de Python)

Navegador web moderno

📥 Instalación Paso a Paso
Clonar o descargar el proyecto

bash
git clone <url-del-repositorio>
cd sistema_rutas
Crear entorno virtual (recomendado)

bash
python -m venv venv
source venv/bin/activate # Linux/Mac
venv\Scripts\activate # Windows
Instalar dependencias

bash
pip install flask
Ejecutar la aplicación

bash
python app.py
Acceder a la aplicación

text
🌐 Abrir navegador en: http://localhost:5000
⚙️ Configuración
El sistema no requiere configuración adicional. Los datos iniciales de Bolivia están precargados en el modelo.

📁 Estructura de Archivos
Backend (Python)
text
sistema_rutas/
├── app.py # Servidor Flask principal
├── controllers/
│ └── mapa_controller.py # Orquestador MVC
├── models/
│ └── grafo_rutas.py # Modelo de datos + algoritmos
├── views/
│ └── mapa_view.py # Formateo de respuestas
└── requirements.txt # Dependencias (si existe)
Frontend (HTML/CSS/JavaScript)
text
sistema_rutas/
├── templates/
│ └── mapa.html # Template principal
└── static/
├── estilo.css # Estilos y diseño
└── rutas.js # Lógica frontend interactiva
🔌 API Endpoints
🗺️ Gestión del Mapa
Método Endpoint Descripción Parámetros
GET /api/mapa Obtener estado completo del mapa -
POST /api/ciudad Agregar nueva ciudad nombre, x, y
DELETE /api/ciudad Eliminar ciudad nombre
POST /api/ruta/nueva Agregar nueva ruta ciudad1, ciudad2, peso
DELETE /api/ruta Eliminar ruta ciudad1, ciudad2
🧮 Cálculo de Rutas
Método Endpoint Descripción Parámetros
POST /api/ruta Calcular ruta óptima origen, destino
🧠 Algoritmos Implementados
Dijkstra - Búsqueda de Ruta Óptima
python
def dijkstra(self, origen, destino):
"""
Implementación del algoritmo Dijkstra para encontrar
el camino más corto entre dos ciudades.

    Complejidad: O((V + E) log V)
    Donde:
      V = número de vértices (ciudades)
      E = número de aristas (rutas)
    """

Características del Algoritmo:
✅ Optimizado con heapq para cola de prioridad

✅ Trazabilidad completa de pasos para animación

✅ Manejo de casos bordes (sin camino, mismo origen-destino)

✅ Reconstrucción eficiente del camino óptimo

Estructuras de Datos Utilizadas:
Grafo no dirigido con pesos en aristas

Diccionarios para acceso O(1) a ciudades y rutas

Heap para gestión eficiente de prioridades

📖 Guía de Uso
🖱️ Interacción Básica

1. Visualización del Mapa
   El mapa muestra 9 ciudades principales de Bolivia

Cada ciudad tiene coordenadas predefinidas

Las rutas existentes se muestran con distancias en km

2. Agregar Ciudades
   Método 1: Formulario

Completa nombre, coordenada X e Y en el panel izquierdo

Haz clic en "Agregar Ciudad"

Método 2: Click en Mapa 🆕

Haz click en cualquier lugar del mapa SVG

Ingresa el nombre de la ciudad en el prompt

La ciudad se agregará automáticamente

3. Gestionar Rutas
   Agregar Ruta:

Selecciona ciudades origen y destino

Ingresa la distancia en kilómetros

Haz clic en "Agregar Ruta"

Eliminar Ruta:

Localiza la ruta en el panel derecho "Rutas"

Haz clic en el botón 🗑️ junto a la ruta

Confirma la eliminación

4. Calcular Ruta Óptima
   Selecciona ciudades origen y destino

Haz clic en "Calcular Ruta"

Observa la animación del algoritmo Dijkstra

La ruta óptima se resaltará en verde

🎨 Personalización Visual
Colores y Temas
Ciudades: Rojo (#d52b1e) con borde amarillo (#fdda00)

Nombres: Verde (#007a33) - colores bandera boliviana

Rutas normales: Marrón (#8B4513)

Rutas óptimas: Verde (#28a745) con animación

Fondo: Gris claro (#f8f9fa)

Tamaños y Espaciado
Mapa principal: 1600x1200 píxeles

Paneles laterales: 380px (izq) y 400px (der)

Texto ciudades: 24px para máxima legibilidad

Radio círculos: 16px para mejor visibilidad

🛠️ Tecnologías Utilizadas
Backend
Tecnología Versión Propósito
Python 3.8+ Lenguaje principal
Flask 2.0+ Framework web
Heapq Built-in Cola de prioridad para Dijkstra
Frontend
Tecnología Propósito
HTML5 Estructura semántica
CSS3 Estilos y diseño responsive
JavaScript ES6+ Interactividad y llamadas API
SVG Gráficos vectoriales para el mapa
Arquitectura
Patrón/Concepto Implementación
MVC Separación clara de responsabilidades
REST API Endpoints JSON para frontend
Factory Pattern GrafoRutas.crear_grafo_bolivia()
Singleton Controlador principal en app.py
🔧 Desarrollo y Contribución
🏗️ Estructura para Nuevas Funcionalidades
Agregar Nuevo Algoritmo
Modelo (grafo_rutas.py):

python
def bfs(self, origen, destino): # Implementar BFS
pass
Controlador (mapa_controller.py):

python
def calcular_ruta_bfs(self, origen, destino):
try:
resultado = self.modelo.bfs(origen, destino)
return self.vista.formatear_respuesta_ruta(resultado)
except Exception as e:
return self.vista.formatear_error(str(e))
Vista (mapa_view.py): Ya preparada para formatear respuestas

Ruta (app.py):

python
@app.route('/api/ruta/bfs', methods=['POST'])
def calcular_ruta_bfs(): # Llamar al controlador
🐛 Debugging y Logs
El sistema incluye logs detallados:

python
print(f"🔍 DEBUG - Ciudades en modelo: {len(self.modelo.ciudades)}")
print(f"✅ Ruta encontrada: {' -> '.join(camino)}")
📊 Métricas de Calidad
Cobertura de código: Estructura modular facilita testing

Performance: Dijkstra optimizado con heapq

Mantenibilidad: Separación clara MVC

Usabilidad: Interfaz intuitiva con feedback inmediato

🚀 Roadmap y Mejoras Futuras
🔮 Próximas Características
Múltiples criterios de optimización (tiempo, costo, distancia)

Algoritmos adicionales (A\*, Bellman-Ford, Floyd-Warshall)

Persistencia de datos (JSON, SQLite)

Exportación de mapas (PNG, PDF)

Modo offline con Service Workers

🎨 Mejoras de UX
Drag & drop para reposicionar ciudades

Zoom y pan en el mapa SVG

Tooltips informativos

Temas dark/light mode

📞 Soporte y Contacto
🐛 Reportar Issues
Al encontrar un error, incluir:

Pasos para reproducir

Comportamiento esperado vs actual

Capturas de pantalla (si aplica)

Logs de la consola del navegador

💡 Sugerencias de Mejora
Las contribuciones son bienvenidas en:

Nuevos algoritmos de grafos

Mejoras de interfaz de usuario

Optimizaciones de performance

Documentación adicional

📄 Licencia
Este proyecto fue desarrollado con fines educativos y demostrativos. Libre uso y modificación con atribución al autor.

¡Disfruta explorando el sistema de rutas de Bolivia! 🗺️🇧🇴

_Documentación generada automáticamente - Sistema de Rutas de Bolivia v1.0_
