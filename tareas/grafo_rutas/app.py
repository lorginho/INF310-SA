from flask import Flask, render_template, jsonify, request
import heapq

app = Flask(__name__)

# DATOS ACTUALIZADOS - con más conexiones
DATOS_MAPA = {
    'ciudades': {
        'La Paz': [200, 150],
        'Cochabamba': [300, 250],
        'Santa Cruz': [450, 200],
        'Sucre': [350, 350],
        'Oruro': [250, 200],
        'Potosí': [320, 400],
        'Tarija': [400, 450],
        'Trinidad': [500, 100],
        'Cobija': [150, 50]
    },
    'conexiones': [
        # Rutas originales
        ['La Paz', 'Cochabamba'],
        ['La Paz', 'Oruro'],
        ['Cochabamba', 'Santa Cruz'],
        ['Cochabamba', 'Sucre'],
        ['Santa Cruz', 'Trinidad'],
        ['Sucre', 'Potosí'],
        ['Potosí', 'Tarija'],
        ['Oruro', 'Sucre'],
        ['La Paz', 'Cobija'],
        # NUEVAS RUTAS AGREGADAS
        ['Santa Cruz', 'Sucre'],  # Conexión directa Santa Cruz - Sucre
        ['Oruro', 'Potosí'],      # Conexión directa Oruro - Potosí
        ['Cochabamba', 'Potosí']  # Conexión directa Cochabamba - Potosí
    ],
    'pesos': {
        # Pesos originales
        'La Paz-Cochabamba': 380,
        'Cochabamba-La Paz': 380,
        'La Paz-Oruro': 200,
        'Oruro-La Paz': 200,
        'Cochabamba-Santa Cruz': 450,
        'Santa Cruz-Cochabamba': 450,
        'Cochabamba-Sucre': 280,
        'Sucre-Cochabamba': 280,
        'Santa Cruz-Trinidad': 320,
        'Trinidad-Santa Cruz': 320,
        'Sucre-Potosí': 150,
        'Potosí-Sucre': 150,
        'Potosí-Tarija': 320,
        'Tarija-Potosí': 320,
        'Oruro-Sucre': 350,
        'Sucre-Oruro': 350,
        'La Paz-Cobija': 650,
        'Cobija-La Paz': 650,
        # NUEVOS PESOS AGREGADOS
        'Santa Cruz-Sucre': 410,
        'Sucre-Santa Cruz': 410,
        'Oruro-Potosí': 220,
        'Potosí-Oruro': 220,
        'Cochabamba-Potosí': 180,
        'Potosí-Cochabamba': 180
    }
}


def calcular_ruta_dijkstra(origen, destino):
    """
    Algoritmo Dijkstra para encontrar la ruta más corta
    """
    print(f"🔄 Calculando ruta: {origen} -> {destino}")

    # Verificar que las ciudades existen
    if origen not in DATOS_MAPA['ciudades'] or destino not in DATOS_MAPA['ciudades']:
        return {'status': 'error', 'message': 'Una o ambas ciudades no existen'}

    if origen == destino:
        return {
            'status': 'success',
            'camino': [origen],
            'distancia': 0,
            'pasos': [('visitando', origen, 0)]
        }

    # Inicializar estructuras
    distancias = {ciudad: float('inf') for ciudad in DATOS_MAPA['ciudades']}
    distancias[origen] = 0
    previos = {}
    pasos = []

    # Cola de prioridad
    cola = [(0, origen)]

    while cola:
        distancia_actual, ciudad_actual = heapq.heappop(cola)
        pasos.append(('visitando', ciudad_actual, distancia_actual))

        # Si llegamos al destino, terminar
        if ciudad_actual == destino:
            break

        # Si encontramos una distancia mejor, continuar
        if distancia_actual > distancias[ciudad_actual]:
            continue

        # Explorar vecinos
        for conexion in DATOS_MAPA['conexiones']:
            if conexion[0] == ciudad_actual:
                vecino = conexion[1]

                # Obtener peso de la conexión
                clave = f"{ciudad_actual}-{vecino}"
                peso = DATOS_MAPA['pesos'].get(clave, float('inf'))

                nueva_distancia = distancia_actual + peso

                if nueva_distancia < distancias[vecino]:
                    distancias[vecino] = nueva_distancia
                    previos[vecino] = ciudad_actual
                    heapq.heappush(cola, (nueva_distancia, vecino))
                    pasos.append(('actualizando', vecino, nueva_distancia))

    # Reconstruir camino si se llegó al destino
    if destino not in previos and origen != destino:
        return {'status': 'error', 'message': f'No hay camino de {origen} a {destino}'}

    # Reconstruir camino
    camino = []
    actual = destino
    while actual in previos:
        camino.append(actual)
        actual = previos[actual]
    camino.append(origen)
    camino.reverse()

    print(
        f"✅ Ruta encontrada: {' -> '.join(camino)} (Distancia: {distancias[destino]} km)")

    return {
        'status': 'success',
        'camino': camino,
        'distancia': distancias[destino],
        'pasos': pasos
    }


@app.route('/')
def index():
    return render_template('mapa.html')


@app.route('/api/mapa')
def obtener_mapa():
    print("✅ Enviando datos del mapa con", len(
        DATOS_MAPA['ciudades']), "ciudades")
    return jsonify(DATOS_MAPA)


@app.route('/api/ruta', methods=['POST'])
def calcular_ruta():
    data = request.json
    origen = data.get('origen', '').strip()
    destino = data.get('destino', '').strip()

    if not origen or not destino:
        return jsonify({'status': 'error', 'message': 'Origen y destino son requeridos'})

    resultado = calcular_ruta_dijkstra(origen, destino)
    return jsonify(resultado)


if __name__ == '__main__':
    print("🚀 Servidor Flask iniciado - Con Dijkstra Real")
    print("📍 9 ciudades de Bolivia cargadas")
    print("🛣️ 12 rutas disponibles:")
    rutas_unicas = set()
    for conexion in DATOS_MAPA['conexiones']:
        ruta = f"{conexion[0]} ↔ {conexion[1]}"
        if ruta not in rutas_unicas:
            clave = f"{conexion[0]}-{conexion[1]}"
            peso = DATOS_MAPA['pesos'][clave]
            print(f"   • {ruta}: {peso} km")
            rutas_unicas.add(ruta)
    print("🌐 Accede en: http://localhost:5000")
    app.run(debug=True, port=5000)
