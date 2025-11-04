"""
archivo: app.py
Punto de entrada principal del proyecto Flask
Autor: Lorgio Añez J.
Fecha: 2025-09-23

Descripción: app.py arranca la aplicación web, conecta los controladores
y sirve la interfaz de usuario, permitiendo que el proyecto funcione 
como una aplicación web interactiva.


A Detalle: 

Crear la aplicación Flask y configurarla.
Registrar el blueprint del controlador (arbol_bp),que contiene las rutas
para operar sobre el árbol binario.
Definir la ruta raíz / que muestra la página principal (index.html).
Iniciar el servidor web cuando se ejecuta el archivo directamente.

app.py
Punto de entrada principal del proyecto Flask
"""

from flask import Flask, render_template
from controllers.arbol_controller import arbol_bp

app = Flask(__name__)
app.secret_key = 'arbol_binario_secret_key'

app.register_blueprint(arbol_bp)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
