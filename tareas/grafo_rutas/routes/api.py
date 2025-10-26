from flask import Blueprint, jsonify, request
from controllers.mapa_controller import MapaController

# Crear blueprint
api_bp = Blueprint('api', __name__)

# Inicializar controlador
controlador = MapaController()


@api_bp.route('/mapa')
def obtener_mapa():
    """Obtiene datos a través del Controlador"""
    try:
        datos_mapa = controlador.obtener_mapa()
        print(
            f"🔍 DEBUG - /api/mapa enviando: {len(datos_mapa['ciudades'])} ciudades")
        return jsonify(datos_mapa)
    except Exception as e:
        print(f"❌ Error en /api/mapa: {e}")
        return jsonify({'status': 'error', 'message': str(e)})


@api_bp.route('/ruta', methods=['POST'])
def calcular_ruta():
    """Calcula ruta a través del Controlador"""
    data = request.json
    origen = data.get('origen', '').strip()
    destino = data.get('destino', '').strip()

    if not origen or not destino:
        return jsonify({'status': 'error', 'message': 'Origen y destino son requeridos'})

    try:
        resultado = controlador.calcular_ruta(origen, destino)
        return jsonify(resultado)
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})


@api_bp.route('/ciudad', methods=['POST'])
def agregar_ciudad():
    """Agrega una nueva ciudad a través del Controlador"""
    data = request.json
    nombre = data.get('nombre', '').strip()
    x = data.get('x', '')
    y = data.get('y', '')

    if not nombre or not x or not y:
        return jsonify({'status': 'error', 'message': 'Nombre, x e y son requeridos'})

    try:
        resultado = controlador.agregar_ciudad({
            'nombre': nombre,
            'x': x,
            'y': y
        })
        return jsonify(resultado)
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})


@api_bp.route('/ciudad', methods=['DELETE'])
def eliminar_ciudad():
    """Elimina una ciudad a través del Controlador"""
    data = request.json
    nombre = data.get('nombre', '').strip()

    if not nombre:
        return jsonify({'status': 'error', 'message': 'Nombre es requerido'})

    try:
        resultado = controlador.eliminar_ciudad(nombre)
        return jsonify(resultado)
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})


@api_bp.route('/ruta/nueva', methods=['POST'])
def agregar_ruta():
    """Agrega una nueva ruta entre ciudades existentes"""
    data = request.json
    ciudad1 = data.get('ciudad1', '').strip()
    ciudad2 = data.get('ciudad2', '').strip()
    peso = data.get('peso', '')

    if not ciudad1 or not ciudad2 or not peso:
        return jsonify({'status': 'error', 'message': 'ciudad1, ciudad2 y peso son requeridos'})

    try:
        resultado = controlador.agregar_ruta({
            'ciudad1': ciudad1,
            'ciudad2': ciudad2,
            'peso': peso
        })
        return jsonify(resultado)
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})


@api_bp.route('/ruta', methods=['DELETE'])
def eliminar_ruta():
    """Elimina una ruta entre ciudades"""
    data = request.json
    ciudad1 = data.get('ciudad1', '').strip()
    ciudad2 = data.get('ciudad2', '').strip()

    if not ciudad1 or not ciudad2:
        return jsonify({'status': 'error', 'message': 'ciudad1 y ciudad2 son requeridos'})

    try:
        resultado = controlador.eliminar_ruta(ciudad1, ciudad2)
        return jsonify(resultado)
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})
