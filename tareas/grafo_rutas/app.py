from flask import Flask, render_template, jsonify, request
from controllers.mapa_controller import MapaController  # ✅ Usar el Controlador

app = Flask(__name__)

# ✅ MVC COMPLETO: app.py solo conoce al Controlador
controlador = MapaController()


@app.route('/')
def index():
    return render_template('mapa.html')


@app.route('/api/mapa')
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


@app.route('/api/ruta', methods=['POST'])
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


@app.route('/api/ciudad', methods=['POST'])
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


@app.route('/api/ciudad', methods=['DELETE'])
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


@app.route('/api/ruta/nueva', methods=['POST'])
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


if __name__ == '__main__':
    print("🚀 Servidor Flask - Arquitectura MVC COMPLETA")
    print("📍 Usando MapaController → GrafoRutas → MapaView")
    print("🌐 Accede en: http://localhost:5000")
    app.run(debug=True, port=5000)
