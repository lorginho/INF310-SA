"""
app.py
Punto de entrada principal de la aplicación Flask - Árbol Binario
"""

from flask import Flask, render_template
from routes.arbol_api import arbol_bp

app = Flask(__name__)
app.secret_key = 'arbol_binario_secret_key'

# Registrar el blueprint desde routes
app.register_blueprint(arbol_bp)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    print("🚀 Servidor Flask - Arquitectura con Blueprints")
    print("📍 Usable en red local: http://192.168.100.37:5000")
    print("🌐 Accede en: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
