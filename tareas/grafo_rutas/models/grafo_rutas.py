import heapq


class GrafoRutas:
    def __init__(self):
        self.ciudades = {}
        self.conexiones = {}

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
        """Retorna el estado completo del modelo para la vista"""
        return {
            'ciudades': self.ciudades.copy(),
            'conexiones': list(self.conexiones.keys()),
            'pesos': self.conexiones.copy()
        }
