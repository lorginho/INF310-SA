"""
controllers/arbol_controller.py
Controlador Flask para operaciones del Árbol Binario de Búsqueda
"""

from flask import Blueprint, request, jsonify
from models.arbol_binario import ArbolBinario

# ===== INICIALIZACIÓN =====

arbol = ArbolBinario()
arbol_bp = Blueprint('arbol', __name__)

# Cache simple para estadísticas (mejora eficiencia)
_estadisticas_cache = None


def invalidar_cache():
    """Invalidar cache cuando el árbol cambie"""
    global _estadisticas_cache
    _estadisticas_cache = None


def obtener_estadisticas():
    """Obtener estadísticas con cache (evita cálculos repetidos)"""
    global _estadisticas_cache
    if _estadisticas_cache is None:
        _estadisticas_cache = {
            'altura': arbol.altura(),
            'total_nodos': arbol.contar_nodos(),
            'nodos_hoja': arbol.contar_hojas(),
            'vacio': arbol.es_vacio()
        }
    return _estadisticas_cache

# ===== FUNCIONES AUXILIARES OPTIMIZADAS =====


def recorrido_inorden(nodo):
    """Recorrido in-order optimizado (menos creación de listas)"""
    resultado = []

    def _inorden(n):
        if n is not None:
            _inorden(n.get_izquierdo())
            resultado.append(n.get_dato())
            _inorden(n.get_derecho())
    _inorden(nodo)
    return resultado


def recorrido_preorden(nodo):
    """Recorrido pre-order optimizado"""
    resultado = []

    def _preorden(n):
        if n is not None:
            resultado.append(n.get_dato())
            _preorden(n.get_izquierdo())
            _preorden(n.get_derecho())
    _preorden(nodo)
    return resultado


def recorrido_postorden(nodo):
    """Recorrido post-order optimizado"""
    resultado = []

    def _postorden(n):
        if n is not None:
            _postorden(n.get_izquierdo())
            _postorden(n.get_derecho())
            resultado.append(n.get_dato())
    _postorden(nodo)
    return resultado

# ===== ENDPOINTS OPTIMIZADOS =====


@arbol_bp.route('/insertar', methods=['POST'])
def insertar():
    """Insertar valores con validación temprana y cache"""
    data = request.get_json()
    valores = data.get('valores', [])

    # Validación temprana - filtrar solo valores válidos
    valores_validos = []
    for valor in valores:
        try:
            valores_validos.append(int(valor))
        except ValueError:
            continue  # Saltar valores inválidos sin procesar excepciones

    resultados = []
    for valor_int in valores_validos:
        exito = arbol.insertar_nodo(valor_int)
        resultados.append({
            'valor': valor_int,
            'exito': exito,
            'mensaje': 'Insertado correctamente' if exito else 'Valor duplicado'
        })

    invalidar_cache()  # El árbol cambió, invalidar cache
    return jsonify({'resultados': resultados})


@arbol_bp.route('/eliminar', methods=['POST'])
def eliminar():
    """Eliminar nodo sin búsqueda redundante"""
    data = request.get_json()
    valor = data.get('valor')

    try:
        valor_int = int(valor)
        # El modelo ya hace la búsqueda internamente, no duplicar
        exito = arbol.eliminar_nodo(valor_int)

        invalidar_cache()
        return jsonify({
            'exito': exito,
            'mensaje': 'Nodo eliminado' if exito else 'Nodo no encontrado',
            'estadisticas': obtener_estadisticas()
        })
    except ValueError:
        return jsonify({
            'exito': False,
            'mensaje': 'Valor no válido'
        })


@arbol_bp.route('/buscar', methods=['POST'])
def buscar():
    """Buscar valor en el árbol"""
    data = request.get_json()
    valor = data.get('valor')

    try:
        valor_int = int(valor)
        nodo = arbol.buscar_x(valor_int)
        return jsonify({
            'encontrado': nodo is not None,
            'valor': valor_int,
            'mensaje': 'Nodo encontrado' if nodo else 'Nodo no encontrado'
        })
    except ValueError:
        return jsonify({
            'encontrado': False,
            'mensaje': 'Valor no válido'
        })


@arbol_bp.route('/recorrido/<tipo>', methods=['GET'])
def recorrido(tipo):
    """Recorridos optimizados"""
    if tipo == 'inorden':
        resultado = recorrido_inorden(arbol.raiz)
    elif tipo == 'preorden':
        resultado = recorrido_preorden(arbol.raiz)
    elif tipo == 'postorden':
        resultado = recorrido_postorden(arbol.raiz)
    elif tipo == 'amplitud':
        resultado = arbol.amplitud()
    else:
        return jsonify({'error': 'Tipo de recorrido no válido'})

    return jsonify({
        'tipo': tipo,
        'recorrido': resultado
    })


@arbol_bp.route('/limpiar', methods=['POST'])
def limpiar():
    """Limpiar árbol y cache"""
    global arbol
    arbol = ArbolBinario()
    invalidar_cache()
    return jsonify({
        'mensaje': 'Árbol limpiado',
        'estadisticas': obtener_estadisticas()
    })


@arbol_bp.route('/estadisticas', methods=['GET'])
def estadisticas():
    """Estadísticas con cache para respuesta instantánea"""
    return jsonify(obtener_estadisticas())


@arbol_bp.route('/estructura', methods=['GET'])
def obtener_estructura():
    """Estructura del árbol para visualización"""
    def serializar_nodo(nodo):
        if nodo is None:
            return None
        return {
            'dato': nodo.get_dato(),
            'izquierdo': serializar_nodo(nodo.get_izquierdo()),
            'derecho': serializar_nodo(nodo.get_derecho())
        }

    estructura = serializar_nodo(arbol.raiz)
    return jsonify({'raiz': estructura})


@arbol_bp.route('/eliminar-rama', methods=['POST'])
def eliminar_rama():
    """Eliminar rama optimizado - evita recorridos duplicados"""
    data = request.get_json()
    valor = data.get('valor')

    try:
        valor_int = int(valor)

        # Obtener la rama antes de eliminar
        rama_eliminada = arbol.obtener_rama(valor_int)
        if rama_eliminada is None:
            return jsonify({
                'exito': False,
                'mensaje': f'Nodo {valor_int} no encontrado'
            })

        # Eliminar la rama
        exito = arbol.eliminar_rama(valor_int)

        invalidar_cache()

        return jsonify({
            'exito': exito,
            'mensaje': 'Rama eliminada correctamente' if exito else 'No se pudo eliminar la rama',
            'rama_eliminada': rama_eliminada,
            'cantidad_nodos': len(rama_eliminada),
            'estadisticas': obtener_estadisticas()
        })

    except ValueError:
        return jsonify({
            'exito': False,
            'mensaje': 'Valor no válido'
        })
    except Exception as e:
        return jsonify({
            'exito': False,
            'mensaje': f'Error interno: {str(e)}'
        })


@arbol_bp.route('/verificar-balanceo', methods=['GET'])
def verificar_balanceo_ruta():
    """Verificar balanceo del árbol"""
    try:
        balanceado = arbol.esta_balanceado()
        return jsonify({
            'balanceado': balanceado,
            'mensaje': 'El árbol está balanceado' if balanceado else 'El árbol está desbalanceado.'
        })
    except Exception as e:
        return jsonify({'error': f'Error al verificar balanceo: {str(e)}'}), 500


@arbol_bp.route('/balancear', methods=['POST'])
def balancear_arbol_ruta():
    """Balancear árbol"""
    try:
        arbol.forzar_balanceo()
        invalidar_cache()
        return jsonify({
            'exito': True,
            'mensaje': 'Árbol balanceado exitosamente.'
        })
    except Exception as e:
        return jsonify({'error': f'Error al balancear el árbol: {str(e)}'}), 500


@arbol_bp.route('/simetrico', methods=['GET'])
def verificar_simetria():
    """Verificar simetría del árbol"""
    try:
        es_simetrico = arbol.es_simetrico()
        return jsonify({
            'es_simetrico': es_simetrico,
            'mensaje': 'El árbol es simétrico' if es_simetrico else 'El árbol no es simétrico'
        })
    except Exception as e:
        return jsonify({
            'error': f'Error al verificar simetría: {str(e)}'
        }), 500


@arbol_bp.route('/simetria-niveles', methods=['GET'])
def obtener_simetria_niveles():
    """Simetría por niveles"""
    try:
        niveles_simetria = arbol.obtener_niveles_simetria()
        return jsonify({
            'niveles_simetria': niveles_simetria,
            'total_niveles': len(niveles_simetria)
        })
    except Exception as e:
        return jsonify({
            'error': f'Error al analizar simetría por niveles: {str(e)}'
        }), 500


@arbol_bp.route('/recorrido-animado/<tipo>', methods=['GET'])
def recorrido_animado(tipo):
    """Devuelve lista de nodos en orden para animación"""
    try:
        if tipo == 'inorden':
            resultado = recorrido_inorden(arbol.raiz)
        elif tipo == 'preorden':
            resultado = recorrido_preorden(arbol.raiz)
        elif tipo == 'postorden':
            resultado = recorrido_postorden(arbol.raiz)
        elif tipo == 'amplitud':
            resultado = arbol.amplitud()
        else:
            return jsonify({'error': 'Tipo de recorrido no válido'})

        return jsonify({
            'tipo': tipo,
            'recorrido': resultado,
            'mensaje': f'Recorrido {tipo} listo para animación'
        })
    except Exception as e:
        return jsonify({'error': f'Error en recorrido animado: {str(e)}'})
