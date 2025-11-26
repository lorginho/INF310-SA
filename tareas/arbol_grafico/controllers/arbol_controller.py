"""
controllers/arbol_controller.py
Controlador para operaciones del Árbol Binario de Búsqueda (Lógica de Aplicación)
"""

from models.arbol_binario import ArbolBinario

class ArbolController:
    def __init__(self):
        self.arbol = ArbolBinario()
        self._estadisticas_cache = None

    def invalidar_cache(self):
        self._estadisticas_cache = None

    def obtener_estadisticas(self):
        if self._estadisticas_cache is None:
            self._estadisticas_cache = {
                'altura': self.arbol.altura(),
                'total_nodos': self.arbol.contar_nodos(),
                'nodos_hoja': self.arbol.contar_hojas(),
                'vacio': self.arbol.es_vacio()
            }
        return self._estadisticas_cache

    def insertar(self, valores):
        # Validación temprana - filtrar solo valores válidos
        valores_validos = []
        for valor in valores:
            try:
                valores_validos.append(int(valor))
            except ValueError:
                continue

        resultados = []
        for valor_int in valores_validos:
            exito = self.arbol.insertar_nodo(valor_int)
            resultados.append({
                'valor': valor_int,
                'exito': exito,
                'mensaje': 'Insertado correctamente' if exito else 'Valor duplicado'
            })

        self.invalidar_cache()
        return {'resultados': resultados}

    def eliminar(self, valor):
        try:
            valor_int = int(valor)
            exito = self.arbol.eliminar_nodo(valor_int)
            self.invalidar_cache()
            return {
                'exito': exito,
                'mensaje': 'Nodo eliminado' if exito else 'Nodo no encontrado',
                'estadisticas': self.obtener_estadisticas()
            }
        except ValueError:
            return {
                'exito': False,
                'mensaje': 'Valor no válido'
            }

    def buscar(self, valor):
        try:
            valor_int = int(valor)
            nodo = self.arbol.buscar_x(valor_int)
            return {
                'encontrado': nodo is not None,
                'valor': valor_int,
                'mensaje': 'Nodo encontrado' if nodo else 'Nodo no encontrado'
            }
        except ValueError:
            return {
                'encontrado': False,
                'mensaje': 'Valor no válido'
            }

    def recorrido(self, tipo):
        if tipo == 'inorden':
            resultado = self._recorrido_inorden(self.arbol.raiz)
        elif tipo == 'preorden':
            resultado = self._recorrido_preorden(self.arbol.raiz)
        elif tipo == 'postorden':
            resultado = self._recorrido_postorden(self.arbol.raiz)
        elif tipo == 'amplitud':
            resultado = self.arbol.amplitud()
        else:
            return {'error': 'Tipo de recorrido no válido'}

        return {
            'tipo': tipo,
            'recorrido': resultado
        }

    def _recorrido_inorden(self, nodo):
        resultado = []
        def _inorden(n):
            if n is not None:
                _inorden(n.get_izquierdo())
                resultado.append(n.get_dato())
                _inorden(n.get_derecho())
        _inorden(nodo)
        return resultado

    def _recorrido_preorden(self, nodo):
        resultado = []
        def _preorden(n):
            if n is not None:
                resultado.append(n.get_dato())
                _preorden(n.get_izquierdo())
                _preorden(n.get_derecho())
        _preorden(nodo)
        return resultado

    def _recorrido_postorden(self, nodo):
        resultado = []
        def _postorden(n):
            if n is not None:
                _postorden(n.get_izquierdo())
                _postorden(n.get_derecho())
                resultado.append(n.get_dato())
        _postorden(nodo)
        return resultado

    def limpiar(self):
        self.arbol = ArbolBinario()
        self.invalidar_cache()
        return {
            'mensaje': 'Árbol limpiado',
            'estadisticas': self.obtener_estadisticas()
        }

    def obtener_estructura(self):
        def serializar_nodo(nodo):
            if nodo is None:
                return None
            return {
                'dato': nodo.get_dato(),
                'izquierdo': serializar_nodo(nodo.get_izquierdo()),
                'derecho': serializar_nodo(nodo.get_derecho())
            }

        estructura = serializar_nodo(self.arbol.raiz)
        return {'raiz': estructura}

    def eliminar_rama(self, valor):
        try:
            valor_int = int(valor)
            rama_eliminada = self.arbol.obtener_rama(valor_int)
            if rama_eliminada is None:
                return {
                    'exito': False,
                    'mensaje': f'Nodo {valor_int} no encontrado'
                }

            exito = self.arbol.eliminar_rama(valor_int)
            self.invalidar_cache()

            return {
                'exito': exito,
                'mensaje': 'Rama eliminada correctamente' if exito else 'No se pudo eliminar la rama',
                'rama_eliminada': rama_eliminada,
                'cantidad_nodos': len(rama_eliminada),
                'estadisticas': self.obtener_estadisticas()
            }

        except ValueError:
            return {
                'exito': False,
                'mensaje': 'Valor no válido'
            }
        except Exception as e:
            return {
                'exito': False,
                'mensaje': f'Error interno: {str(e)}'
            }

    def verificar_balanceo(self):
        try:
            balanceado = self.arbol.esta_balanceado()
            return {
                'balanceado': balanceado,
                'mensaje': 'El árbol está balanceado' if balanceado else 'El árbol está desbalanceado.'
            }
        except Exception as e:
            return {'error': f'Error al verificar balanceo: {str(e)}'}

    def balancear(self):
        try:
            self.arbol.forzar_balanceo()
            self.invalidar_cache()
            return {
                'exito': True,
                'mensaje': 'Árbol balanceado exitosamente.'
            }
        except Exception as e:
            return {'error': f'Error al balancear el árbol: {str(e)}'}

    def verificar_simetria(self):
        try:
            es_simetrico = self.arbol.es_simetrico()
            return {
                'es_simetrico': es_simetrico,
                'mensaje': 'El árbol es simétrico' if es_simetrico else 'El árbol no es simétrico'
            }
        except Exception as e:
            return {'error': f'Error al verificar simetría: {str(e)}'}

    def simetria_niveles(self):
        try:
            niveles_simetria = self.arbol.obtener_niveles_simetria()
            return {
                'niveles_simetria': niveles_simetria,
                'total_niveles': len(niveles_simetria)
            }
        except Exception as e:
            return {'error': f'Error al analizar simetría por niveles: {str(e)}'}

    def recorrido_animado(self, tipo):
        try:
            if tipo == 'inorden':
                resultado = self._recorrido_inorden(self.arbol.raiz)
            elif tipo == 'preorden':
                resultado = self._recorrido_preorden(self.arbol.raiz)
            elif tipo == 'postorden':
                resultado = self._recorrido_postorden(self.arbol.raiz)
            elif tipo == 'amplitud':
                resultado = self.arbol.amplitud()
            else:
                return {'error': 'Tipo de recorrido no válido'}

            return {
                'tipo': tipo,
                'recorrido': resultado,
                'mensaje': f'Recorrido {tipo} listo para animación'
            }
        except Exception as e:
            return {'error': f'Error en recorrido animado: {str(e)}'}
