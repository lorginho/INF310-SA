"""
archivo: app.py
Punto de entrada principal del proyecto Flask
Autor: Lorgio Añez J.
Fecha: 2025-10-23

Descripción: app.py arranca la aplicación web, conecta los controladores
y sirve la interfaz de usuario, permitiendo que el proyecto funcione 
como una aplicación web interactiva.


Resumen breve del funcionamiento de app.py:

Crea la aplicación Flask: app = Flask(name).
Instancia el controlador: controlador = MapaController(). 
app.py delega la lógica al controlador (patrón MVC).
Define la ruta raíz / que muestra la página principal (mapa.html).
Iniciar el servidor web cuando se ejecuta el archivo directamente.

"""

from flask import Flask, render_template
from routes.api import api_bp

app = Flask(__name__)

# Registrar blueprint
app.register_blueprint(api_bp, url_prefix='/api')


@app.route('/')
def index():
    return render_template('mapa.html')


if __name__ == '__main__':
    print("🚀 Servidor Flask - Arquitectura con Blueprints")
    print("📍 Usando MapaController → GrafoRutas → MapaView")
    print("🌐 Accede en: http://localhost:5000")
    app.run(debug=True, port=5000)
