"""
ARCHIVO: models/grafo_rutas.py
AUTOR: Lorgio Añez J.
FECHA: 2025-10-23
DESCRIPCIÓN: Implementación del grafo de rutas y algoritmo Dijkstra.
             Representa ciudades, conexiones y calcula caminos óptimos.
DEPENDENCIAS: heapq, Módulo de Python que implementa colas de prioridad 
              usando min-heap para eficiencia.
"""

import heapq


class GrafoRutas:
    def __init__(self, datos_iniciales=None):
        self.ciudades = {}
        self.conexiones = {}
        if datos_iniciales:
            self.cargar_datos(datos_iniciales)

    def cargar_datos(self, datos):
        """Carga datos iniciales en el modelo"""
        # Limpiar datos existentes
        self.ciudades = {}
        self.conexiones = {}

        # Cargar ciudades
        for ciudad, coordenadas in datos.get('ciudades', {}).items():
            self.agregar_ciudad(ciudad, coordenadas[0], coordenadas[1])

        # Cargar rutas
        for conexion in datos.get('conexiones', []):
            ciudad1, ciudad2 = conexion
            clave = f"{ciudad1}-{ciudad2}"
            pesos = datos['pesos'].get(clave)
            if pesos:
                self.agregar_ruta(ciudad1, ciudad2, pesos)

    @classmethod
    def crear_grafo_bolivia(cls):
        """Factory method para crear grafo con datos de Bolivia"""
        datos_bolivia = {
            'ciudades': {
                'La Paz': [200, 360],
                'Cochabamba': [400, 500],
                'Santa Cruz': [700, 600],
                'Sucre': [500, 700],
                'Oruro': [200, 600],
                'Potosí': [300, 800],
                'Tarija': [600, 900],
                'Trinidad': [600, 200],
                'Cobija': [300, 100]
            },
            'conexiones': [
                ['La Paz', 'Cochabamba'],
                ['La Paz', 'Oruro'],
                ['Cochabamba', 'Santa Cruz'],
                ['Cochabamba', 'Sucre'],
                ['Santa Cruz', 'Trinidad'],
                ['Sucre', 'Potosí'],
                ['Sucre', 'Tarija'],
                ['La Paz', 'Cobija'],
                ['Santa Cruz', 'Sucre'],
                ['Oruro', 'Potosí'],
                ['Cochabamba', 'Oruro']
            ],
            'pesos': {
                'La Paz-Cochabamba': {'distancia': 375, 'tiempo': 6.3},
                'Cochabamba-La Paz': {'distancia': 375, 'tiempo': 6.3},
                'La Paz-Oruro': {'distancia': 240, 'tiempo': 4.0},
                'Oruro-La Paz': {'distancia': 240, 'tiempo': 4.0},
                'Cochabamba-Santa Cruz': {'distancia': 480, 'tiempo': 8.0},
                'Santa Cruz-Cochabamba': {'distancia': 480, 'tiempo': 8.0},
                'Cochabamba-Sucre': {'distancia': 340, 'tiempo': 5.7},
                'Sucre-Cochabamba': {'distancia': 340, 'tiempo': 5.7},
                'Santa Cruz-Trinidad': {'distancia': 420, 'tiempo': 7.0},
                'Trinidad-Santa Cruz': {'distancia': 420, 'tiempo': 7.0},
                'Sucre-Potosí': {'distancia': 150, 'tiempo': 2.5},
                'Potosí-Sucre': {'distancia': 150, 'tiempo': 2.5},
                'Sucre-Tarija': {'distancia': 320, 'tiempo': 5.3},
                'Tarija-Sucre': {'distancia': 320, 'tiempo': 5.3},
                'Oruro-Sucre': {'distancia': 350, 'tiempo': 5.8},
                'Sucre-Oruro': {'distancia': 350, 'tiempo': 5.8},
                'La Paz-Cobija': {'distancia': 650, 'tiempo': 10.8},
                'Cobija-La Paz': {'distancia': 650, 'tiempo': 10.8},
                'Santa Cruz-Sucre': {'distancia': 410, 'tiempo': 6.8},
                'Sucre-Santa Cruz': {'distancia': 410, 'tiempo': 6.8},
                'Oruro-Potosí': {'distancia': 220, 'tiempo': 3.7},
                'Potosí-Oruro': {'distancia': 220, 'tiempo': 3.7},
                'Cochabamba-Oruro': {'distancia': 180, 'tiempo': 3.0},
                'Oruro-Cochabamba': {'distancia': 180, 'tiempo': 3.0}
            }
        }

        grafo = cls()
        grafo.cargar_datos(datos_bolivia)
        return grafo

    def agregar_ciudad(self, nombre, x, y):
        """Agrega una ciudad al grafo"""
        if nombre in self.ciudades:
            raise ValueError(f"La ciudad {nombre} ya existe")
        self.ciudades[nombre] = (x, y)
        return True

    def eliminar_ciudad(self, nombre):
        """Elimina una ciudad y sus conexiones"""
        if nombre not in self.ciudades:
            raise ValueError(f"La ciudad {nombre} no existe")

        # Eliminar ciudad
        del self.ciudades[nombre]

        # Eliminar conexiones relacionadas
        conexiones_a_eliminar = [
            (c1, c2) for c1, c2 in self.conexiones.keys()
            if c1 == nombre or c2 == nombre
        ]

        for conexion in conexiones_a_eliminar:
            del self.conexiones[conexion]

        return True

    def agregar_ruta(self, ciudad1, ciudad2, peso):
        """Agrega una ruta entre dos ciudades"""
        if ciudad1 not in self.ciudades or ciudad2 not in self.ciudades:
            raise ValueError("Una o ambas ciudades no existen")

        # ✅ SI RECIBE UN NÚMERO, CALCULAR TIEMPO AUTOMÁTICAMENTE
        if isinstance(peso, (int, float)):
            # Calcular tiempo estimado basado en distancia (60 km/h promedio)
            tiempo_estimado = round(peso / 60, 1)
            pesos = {
                'distancia': peso,
                'tiempo': tiempo_estimado
            }
        else:
            pesos = peso

        self.conexiones[(ciudad1, ciudad2)] = pesos
        self.conexiones[(ciudad2, ciudad1)] = pesos
        return True

    def eliminar_ruta(self, ciudad1, ciudad2):
        """Elimina una ruta entre dos ciudades"""
        if (ciudad1, ciudad2) not in self.conexiones:
            raise ValueError("La ruta no existe")

        del self.conexiones[(ciudad1, ciudad2)]
        del self.conexiones[(ciudad2, ciudad1)]
        return True

    def obtener_ciudades(self):
        """Retorna todas las ciudades"""
        return self.ciudades.copy()

    def obtener_conexiones(self):
        """Retorna todas las conexiones"""
        return self.conexiones.copy()

    def dijkstra(self, origen, destino, criterio='distancia'):
        if origen not in self.ciudades or destino not in self.ciudades:
            raise ValueError("Origen o destino no existen")

        # Inicialización
        distancias = {ciudad: float('inf') for ciudad in self.ciudades}
        distancias[origen] = 0
        previos = {}
        pasos = []

        cola = [(0, origen)]

        while cola:
            dist_actual, ciudad_actual = heapq.heappop(cola)
            pasos.append(('visitando', ciudad_actual, dist_actual))

            if ciudad_actual == destino:
                break

            if dist_actual > distancias[ciudad_actual]:
                continue

            # Explorar vecinos
            for (c1, c2), pesos_ruta in self.conexiones.items():
                if c1 == ciudad_actual:
                    vecino = c2
                    peso = pesos_ruta.get(criterio, pesos_ruta['distancia'])
                    nueva_dist = dist_actual + peso

                    if nueva_dist < distancias[vecino]:
                        distancias[vecino] = nueva_dist
                        previos[vecino] = ciudad_actual
                        heapq.heappush(cola, (nueva_dist, vecino))
                        pasos.append(('actualizando', vecino, nueva_dist))

        # Verificar si hay camino
        if destino not in previos and origen != destino:
            raise ValueError(f"No hay camino de {origen} a {destino}")

        # Reconstruir camino
        camino = self._reconstruir_camino(previos, origen, destino)

        return {
            'camino': camino,
            'distancia': distancias[destino],
            'pasos': pasos
        }

    def _reconstruir_camino(self, previos, origen, destino):
        """Reconstruye el camino desde el destino al origen"""
        camino = []
        actual = destino

        while actual in previos:
            camino.append(actual)
            actual = previos[actual]

        camino.append(origen)
        camino.reverse()
        return camino

    def obtener_estado(self):
        """Retorna el estado completo del modelo para la vista"""
        conexiones_formateadas = []
        pesos_formateados = {}

        for (ciudad1, ciudad2), pesos in self.conexiones.items():
            conexiones_formateadas.append([ciudad1, ciudad2])
            clave = f"{ciudad1}-{ciudad2}"
            # ✅ MANTENER OBJETO COMPLETO CON DISTANCIA Y TIEMPO
            pesos_formateados[clave] = pesos

        return {
            'ciudades': self.ciudades.copy(),
            'conexiones': conexiones_formateadas,
            'pesos': pesos_formateados  # ← AHORA ENVÍA OBJETOS COMPLETOS
        }
