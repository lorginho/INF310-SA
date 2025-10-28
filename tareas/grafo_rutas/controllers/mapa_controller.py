"""
ARCHIVO: controllers/mapa_controller.py
AUTOR: Lorgio Añez J.
FECHA: 2025-10-23
DESCRIPCIÓN: Controlador principal que coordina operaciones entre modelo y vista.
             Gestiona ciudades, rutas y cálculo de caminos mínimos.
DEPENDENCIAS: models.grafo_rutas, views.mapa_view
"""


from models.grafo_rutas import GrafoRutas
from views.mapa_view import MapaView


class MapaController:
    def __init__(self, modelo=None, vista=None):
        # ✅ MVC CORRECTO: Controlador no sabe de datos específicos
        self.modelo = modelo or GrafoRutas.crear_grafo_bolivia()  # Factory method
        self.vista = vista or MapaView()

        # DEBUG DETALLADO
        print(f"🔍 DEBUG - Ciudades en modelo: {len(self.modelo.ciudades)}")
        print(f"🔍 DEBUG - Conexiones en modelo: {len(self.modelo.conexiones)}")
        print(
            f"🔍 DEBUG - Ciudades específicas: {list(self.modelo.ciudades.keys())}")

        print("✅ Controlador MVC inicializado correctamente")

    def obtener_mapa(self):
        """Obtiene los datos del mapa formateados para la vista"""
        datos_modelo = self.modelo.obtener_estado()
        return self.vista.formatear_datos_mapa(datos_modelo)

    def calcular_ruta(self, origen, destino):
        """Calcula la ruta óptima entre dos ciudades"""
        try:
            valido, error = self.vista.validar_datos_ruta_calculo({
                'origen': origen,
                'destino': destino
            })

            if not valido:
                return self.vista.formatear_error(error)

            resultado = self.modelo.dijkstra(origen, destino)
            return self.vista.formatear_respuesta_ruta(resultado)

        except Exception as e:
            return self.vista.formatear_error(str(e))

    def agregar_ciudad(self, datos):
        """Agrega una nueva ciudad"""
        try:
            valido, error = self.vista.validar_datos_ciudad(datos)
            if not valido:
                return self.vista.formatear_error(error)

            self.modelo.agregar_ciudad(
                datos['nombre'], float(datos['x']), float(datos['y']))
            return self.vista.formatear_exito("Ciudad agregada correctamente")

        except Exception as e:
            return self.vista.formatear_error(str(e))

    def agregar_ruta(self, datos):
        """Agregar una nueva ruta"""
        try:
            valido, error = self.vista.validar_datos_ruta(datos)
            if not valido:
                return self.vista.formatear_error(error)

            self.modelo.agregar_ruta(
                datos['ciudad1'],
                datos['ciudad2'],
                float(datos['peso'])
            )
            return self.vista.formatear_exito("Ruta agregada correctamente")

        except Exception as e:
            return self.vista.formatear_error(str(e))

    def eliminar_ciudad(self, nombre):
        """Elimina una ciudad existente"""
        try:
            self.modelo.eliminar_ciudad(nombre)
            return self.vista.formatear_exito("Ciudad eliminada correctamente")
        except Exception as e:
            return self.vista.formatear_error(str(e))

    def eliminar_ruta(self, ciudad1, ciudad2):
        """Elimina una ruta existente"""
        try:
            self.modelo.eliminar_ruta(ciudad1, ciudad2)
            return self.vista.formatear_exito("Ruta eliminada correctamente")
        except Exception as e:
            return self.vista.formatear_error(str(e))
