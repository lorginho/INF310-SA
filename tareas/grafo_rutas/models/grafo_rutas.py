"""
models/grafo_rutas.py
Autor: Lorgio Añez J.
Fecha: 2025-10-23
Descripción: Clase que representa un Grafo de Rutas para conectar ciudades
de Bolivia, creando ciudades y rutas entre ellas, calculando distancias y
rutas optimas, etc
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
            peso = datos['pesos'].get(clave)
            if peso:
                self.agregar_ruta(ciudad1, ciudad2, peso)

    @classmethod
    def crear_grafo_bolivia(cls):
        """Factory method para crear grafo con datos de Bolivia"""

        datos_bolivia = {

            'ciudades': {
                'La Paz': [200, 360],        # ✅ COORDENADAS ESCALADAS
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
                'La Paz-Cochabamba': 375,
                'Cochabamba-La Paz': 375,
                'La Paz-Oruro': 240,
                'Oruro-La Paz': 240,
                'Cochabamba-Santa Cruz': 480,
                'Santa Cruz-Cochabamba': 480,
                'Cochabamba-Sucre': 340,
                'Sucre-Cochabamba': 340,
                'Santa Cruz-Trinidad': 420,
                'Trinidad-Santa Cruz': 420,
                'Sucre-Potosí': 150,
                'Potosí-Sucre': 150,
                'Sucre-Tarija': 320,
                'Tarija-Sucre': 320,
                'Oruro-Sucre': 350,
                'Sucre-Oruro': 350,
                'La Paz-Cobija': 650,
                'Cobija-La Paz': 650,
                'Santa Cruz-Sucre': 410,
                'Sucre-Santa Cruz': 410,
                'Oruro-Potosí': 220,
                'Potosí-Oruro': 220,
                'Cochabamba-Oruro': 180,
                'Oruro-Cochabamba': 180
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

        if peso <= 0:
            raise ValueError("El peso debe ser mayor a 0")

        self.conexiones[(ciudad1, ciudad2)] = peso
        self.conexiones[(ciudad2, ciudad1)] = peso
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

    def dijkstra(self, origen, destino):
        """Algoritmo Dijkstra para encontrar ruta óptima"""
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
            for (c1, c2), peso in self.conexiones.items():
                if c1 == ciudad_actual:
                    vecino = c2
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
        """Retorna el estado completo del modelo para la vista """
        # ✅ CORRECCIÓN: Convertir tuplas a formatos serializables para JSON
        conexiones_formateadas = []
        pesos_formateados = {}

        for (ciudad1, ciudad2), peso in self.conexiones.items():
            # Formato para conexiones: lista de listas [["La Paz", "Cochabamba"], ...]
            conexiones_formateadas.append([ciudad1, ciudad2])
            # Formato para pesos: diccionario con claves string {"La Paz-Cochabamba": 380, ...}
            clave = f"{ciudad1}-{ciudad2}"
            pesos_formateados[clave] = peso

        return {
            'ciudades': self.ciudades.copy(),
            'conexiones': conexiones_formateadas,  # ✅ Lista de listas
            'pesos': pesos_formateados             # ✅ Diccionario con claves string
        }
