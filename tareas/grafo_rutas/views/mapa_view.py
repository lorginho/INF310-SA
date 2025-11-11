"""
ARCHIVO: views/mapa_view.py
AUTOR: Lorgio Añez J.
FECHA: 2025-10-23
DESCRIPCIÓN: Formatea datos para frontend y valida entradas.
             Serializa respuestas JSON y maneja validaciones.
DEPENDENCIAS: Ninguna
"""


class MapaView:
    @staticmethod
    def formatear_datos_mapa(datos_modelo):
        """Formatea los datos del modelo para la vista web"""
        return {
            'ciudades': datos_modelo['ciudades'],
            'conexiones': datos_modelo['conexiones'],
            'pesos': datos_modelo['pesos']
        }

    @staticmethod
    def formatear_respuesta_ruta(resultado_dijkstra):
        """Formatea la respuesta del algoritmo para el frontend"""
        return {
            'status': 'success',
            'camino': resultado_dijkstra['camino'],
            'distancia': resultado_dijkstra['distancia'],
            'pasos': resultado_dijkstra['pasos']
        }

    @staticmethod
    def formatear_error(mensaje):
        """Formatea mensajes de error"""
        return {
            'status': 'error',
            'message': mensaje
        }

    @staticmethod
    def formatear_exito(mensaje=None):
        """Formatea respuestas de éxito"""
        respuesta = {'status': 'ok'}
        if mensaje:
            respuesta['message'] = mensaje
        return respuesta

    @staticmethod
    def validar_datos_ciudad(datos):
        """Valida los datos para agregar una ciudad"""
        if not datos.get('nombre') or not datos.get('x') or not datos.get('y'):
            return False, "Faltan datos: nombre, x, y son requeridos"

        try:
            x = float(datos['x'])
            y = float(datos['y'])
            if x < 0 or y < 0:
                return False, "Las coordenadas deben ser positivas"
        except ValueError:
            return False, "Las coordenadas deben ser números"

        return True, None

    @staticmethod
    def validar_datos_ruta(datos):
        """Valida datos para agregar ruta"""
        if not datos.get('ciudad1') or not datos.get('ciudad2'):
            return False, "Ambas ciudades son requeridas"

        if not datos.get('distancia') or not datos.get('tiempo'):
            return False, "Distancia y tiempo son requeridos"

        try:
            distancia = float(datos['distancia'])
            tiempo = float(datos['tiempo'])
            if distancia <= 0 or tiempo <= 0:
                return False, "Distancia y tiempo deben ser mayores a 0"
        except ValueError:
            return False, "Distancia y tiempo deben ser números válidos"

        return True, None

    @staticmethod
    def validar_datos_ruta_calculo(datos):
        """Valida los datos para calcular una ruta"""
        if not datos.get('origen') or not datos.get('destino'):
            return False, "Origen y destino son requeridos"
        return True, None
