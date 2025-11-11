"""
ARCHIVO: routes/api.py
AUTOR: Lorgio Añez J.
FECHA: 2025-10-23
DESCRIPCIÓN: Define endpoints REST API para comunicación frontend-backend.
             Maneja requests de mapa, rutas y ciudades.
"""

from flask import Blueprint, jsonify, request
from controllers.mapa_controller import MapaController
from models.grafo_rutas import GrafoRutas

# Crear blueprint
api_bp = Blueprint('api', __name__)

# Inicializar controlador (UNA SOLA INSTANCIA)
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
    try:
        datos = request.get_json()
        origen = datos.get('origen')
        destino = datos.get('destino')
        criterio = datos.get('criterio', 'distancia')

        if not origen or not destino:
            return jsonify({'error': 'Origen y destino requeridos'}), 400

        # ✅ OPCIÓN 1: Usar obtener_grafo() (más directo)
        grafo = controlador.obtener_grafo()
        resultado = grafo.dijkstra(origen, destino, criterio)

        return jsonify({
            'camino': resultado['camino'],
            'distancia': resultado['distancia'],
            'pasos': resultado['pasos'],
            'criterio': criterio
        })

    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        print(f"❌ Error en /api/ruta: {e}")
        return jsonify({'error': 'Error interno del servidor'}), 500


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
def agregar_ruta_nueva():
    """Agrega una nueva ruta entre ciudades existentes"""
    try:
        data = request.get_json()
        print(f"🔍 DEBUG - Tipo de datos recibidos: {type(data)}")
        print(f"🔍 DEBUG - Datos crudos: {data}")

        if not data:
            return jsonify({'status': 'error', 'message': 'No se recibieron datos JSON'})

        ciudad1 = data.get('ciudad1', '').strip()
        ciudad2 = data.get('ciudad2', '').strip()
        distancia = data.get('distancia')
        tiempo = data.get('tiempo')

        print(f"🔍 DEBUG - ciudad1: '{ciudad1}'")
        print(f"🔍 DEBUG - ciudad2: '{ciudad2}'")
        print(f"🔍 DEBUG - distancia: {distancia}")
        print(f"🔍 DEBUG - tiempo: {tiempo}")

        if not ciudad1 or not ciudad2 or distancia is None or tiempo is None:
            return jsonify({'status': 'error', 'message': 'ciudad1, ciudad2, distancia y tiempo son requeridos'})

        try:
            resultado = controlador.agregar_ruta({
                'ciudad1': ciudad1,
                'ciudad2': ciudad2,
                'distancia': distancia,
                'tiempo': tiempo
            })
            return jsonify(resultado)
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)})

    except Exception as e:
        print(f"❌ Error en agregar_ruta_nueva: {e}")
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
