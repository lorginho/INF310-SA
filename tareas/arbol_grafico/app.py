"""
app.py
Punto de entrada principal de la aplicación Flask - Árbol Binario
Autor: Lorgio Añez J.
Fecha: 2025-09-23

Descripción: Configura y arranca la aplicación web Flask, conectando
controladores, rutas y la interfaz de usuario para interactuar con
el árbol binario de búsqueda.
"""

from flask import Flask, render_template
from controllers.arbol_controller import arbol_bp

# ===== CONFIGURACIÓN DE LA APLICACIÓN FLASK =====

# Crear instancia de la aplicación Flask
app = Flask(__name__)

# Clave secreta para sesiones y seguridad (en producción usar variable de entorno)
app.secret_key = 'arbol_binario_secret_key'

# ===== REGISTRO DE BLUEPRINTS (CONTROLADORES) =====

# Registrar el blueprint del controlador del árbol binario
# Esto conecta todas las rutas definidas en arbol_controller.py
app.register_blueprint(arbol_bp)

# ===== RUTAS PRINCIPALES =====


@app.route('/')
def index():
    """
    Ruta raíz: Sirve la página principal de la aplicación.

    Returns:
        Template HTML: Página index.html con la interfaz de usuario
    """
    return render_template('index.html')

# ===== INICIALIZACIÓN DE LA APLICACIÓN =====


if __name__ == '__main__':
    """
    Punto de entrada cuando se ejecuta el archivo directamente.
    Inicia el servidor web de desarrollo de Flask.

    Configuración:
        debug=True: Habilita modo depuración (desactivar en producción)
                   - Recarga automática al detectar cambios
                   - Mensajes de error detallados
    """
    app.run(debug=True)
