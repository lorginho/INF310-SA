"""
routes/arbol_api.py
Blueprint para las rutas del Árbol Binario
"""

from flask import Blueprint, request, jsonify
from controllers.arbol_controller import ArbolController

# Crear blueprint
arbol_bp = Blueprint('arbol', __name__)

# Inicializar controlador
controlador = ArbolController()

@arbol_bp.route('/insertar', methods=['POST'])
def insertar():
    data = request.get_json()
    valores = data.get('valores', [])
    resultado = controlador.insertar(valores)
    return jsonify(resultado)

@arbol_bp.route('/eliminar', methods=['POST'])
def eliminar():
    data = request.get_json()
    valor = data.get('valor')
    resultado = controlador.eliminar(valor)
    return jsonify(resultado)

@arbol_bp.route('/buscar', methods=['POST'])
def buscar():
    data = request.get_json()
    valor = data.get('valor')
    resultado = controlador.buscar(valor)
    return jsonify(resultado)

@arbol_bp.route('/recorrido/<tipo>', methods=['GET'])
def recorrido(tipo):
    resultado = controlador.recorrido(tipo)
    if 'error' in resultado:
        return jsonify(resultado), 400
    return jsonify(resultado)

@arbol_bp.route('/limpiar', methods=['POST'])
def limpiar():
    resultado = controlador.limpiar()
    return jsonify(resultado)

@arbol_bp.route('/estadisticas', methods=['GET'])
def estadisticas():
    resultado = controlador.obtener_estadisticas()
    return jsonify(resultado)

@arbol_bp.route('/estructura', methods=['GET'])
def obtener_estructura():
    resultado = controlador.obtener_estructura()
    return jsonify(resultado)

@arbol_bp.route('/eliminar-rama', methods=['POST'])
def eliminar_rama():
    data = request.get_json()
    valor = data.get('valor')
    resultado = controlador.eliminar_rama(valor)
    return jsonify(resultado)

@arbol_bp.route('/verificar-balanceo', methods=['GET'])
def verificar_balanceo():
    resultado = controlador.verificar_balanceo()
    if 'error' in resultado:
        return jsonify(resultado), 500
    return jsonify(resultado)

@arbol_bp.route('/balancear', methods=['POST'])
def balancear_arbol():
    resultado = controlador.balancear()
    if 'error' in resultado:
        return jsonify(resultado), 500
    return jsonify(resultado)

@arbol_bp.route('/simetrico', methods=['GET'])
def verificar_simetria():
    resultado = controlador.verificar_simetria()
    if 'error' in resultado:
        return jsonify(resultado), 500
    return jsonify(resultado)

@arbol_bp.route('/simetria-niveles', methods=['GET'])
def obtener_simetria_niveles():
    resultado = controlador.simetria_niveles()
    if 'error' in resultado:
        return jsonify(resultado), 500
    return jsonify(resultado)

@arbol_bp.route('/recorrido-animado/<tipo>', methods=['GET'])
def recorrido_animado(tipo):
    resultado = controlador.recorrido_animado(tipo)
    if 'error' in resultado:
        return jsonify(resultado), 400
    return jsonify(resultado)
