from models.grafo_rutas import GrafoRutas
from views.mapa_view import MapaView


class MapaController:
    def __init__(self):
        self.modelo = GrafoRutas()
        self.vista = MapaView()
        self._inicializar_datos()
        print("✅ Controlador inicializado con", len(
            self.modelo.ciudades), "ciudades")  # DEBUG

    def _inicializar_datos(self):
        """Inicializa con datos de Bolivia - VERSIÓN CORREGIDA"""
        ciudades_bolivia = [
            ('La Paz', 200, 150),
            ('Cochabamba', 300, 250),
            ('Santa Cruz', 450, 200),
            ('Sucre', 350, 350),
            ('Oruro', 250, 200),
            ('Potosí', 320, 400),
            ('Tarija', 400, 450),
            ('Trinidad', 500, 100),
            ('Cobija', 150, 50)
        ]

        rutas_bolivia = [
            ('La Paz', 'Cochabamba', 380),
            ('La Paz', 'Oruro', 200),
            ('Cochabamba', 'Santa Cruz', 450),
            ('Cochabamba', 'Sucre', 280),
            ('Santa Cruz', 'Trinidad', 320),
            ('Sucre', 'Potosí', 150),
            ('Potosí', 'Tarija', 320),
            ('Oruro', 'Sucre', 350),
            ('La Paz', 'Cobija', 650)
        ]

        print("🔄 Inicializando ciudades...")  # DEBUG
        for ciudad, x, y in ciudades_bolivia:
            try:
                self.modelo.agregar_ciudad(ciudad, x, y)
                print(f"  ✅ Ciudad agregada: {ciudad}")
            except Exception as e:
                print(f"  ❌ Error agregando {ciudad}: {e}")

        print("🔄 Inicializando rutas...")  # DEBUG
        for ciudad1, ciudad2, peso in rutas_bolivia:
            try:
                self.modelo.agregar_ruta(ciudad1, ciudad2, peso)
                print(f"  ✅ Ruta agregada: {ciudad1} - {ciudad2}")
            except Exception as e:
                print(f"  ❌ Error en ruta {ciudad1}-{ciudad2}: {e}")

        print(
            f"🎉 Inicialización completada: {len(self.modelo.ciudades)} ciudades, {len(self.modelo.conexiones)//2} rutas")

    def obtener_mapa(self):
        """Obtiene los datos del mapa formateados para la vista"""
        datos_modelo = self.modelo.obtener_estado()
        # DEBUG
        print(f"📊 Obteniendo mapa: {len(datos_modelo['ciudades'])} ciudades")
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
        """Agrega una nueva ruta"""
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
