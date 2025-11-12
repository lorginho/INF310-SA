"""
ARCHIVO: app.py
AUTOR: Lorgio Añez J.
FECHA: 2025-10-23
DESCRIPCIÓN: Punto de entrada principal de la aplicación Flask.

CONCEPTOS CLAVE:
- Blueprint: Componente modular de rutas (api_bp desde routes/api.py)
- Endpoints REST: URLs que responden a métodos HTTP (GET, POST, DELETE)
- Los endpoints REST API son URLs específicas que aceptan 
  operaciones HTTP (GET, POST, DELETE) para realizar acciones en el sistema, 
  como obtener datos o modificar el grafo.
- url_prefix='/api': Todas las rutas del blueprint empiezan con /api

DEPENDENCIAS: Flask, routes.api
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
    print("📍 Usable en red local: http://192.168.100.37:5000")
    print("🌐 Accede en: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
