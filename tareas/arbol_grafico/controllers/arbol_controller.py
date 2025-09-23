"""
controllers/arbol_controller.py
Controlador para operaciones del árbol binario (MVC)
Autor: Lorgio Añez J.
Fecha: 2025-09-23
Descripción: Controlador que gestiona las operaciones entre la vista y el modelo del árbol binario
"""

from flask import Blueprint, request, jsonify
from models.arbol_binario import ArbolBinario

# Crear instancia global del árbol (para simplicidad)
arbol = ArbolBinario()

arbol_bp = Blueprint('arbol', __name__)


@arbol_bp.route('/insertar', methods=['POST'])
def insertar():
    data = request.get_json()
    valores = data.get('valores', [])

    resultados = []
    for valor in valores:
        try:
            valor_int = int(valor)
            exito = arbol.insertar_nodo(valor_int)
            resultados.append({
                'valor': valor_int,
                'exito': exito,
                'mensaje': 'Insertado correctamente' if exito else 'Valor duplicado'
            })
        except ValueError:
            resultados.append({
                'valor': valor,
                'exito': False,
                'mensaje': 'Valor no válido'
            })

    # Temporalmente no devolver estadísticas
    return jsonify({
        'resultados': resultados
        # 'estadisticas': obtener_estadisticas()
    })


@arbol_bp.route('/eliminar', methods=['POST'])
def eliminar():
    data = request.get_json()
    valor = data.get('valor')

    try:
        valor_int = int(valor)
        exito = arbol.eliminar_nodo(valor_int)
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
    global arbol
    arbol = ArbolBinario()
    return jsonify({
        'mensaje': 'Árbol limpiado',
        'estadisticas': obtener_estadisticas()
    })


@arbol_bp.route('/estadisticas', methods=['GET'])
def estadisticas():
    return jsonify(obtener_estadisticas())


def obtener_estadisticas():
    return {
        'altura': arbol.altura(),
        'total_nodos': arbol.contar_nodos(),
        'nodos_hoja': arbol.contar_hojas(),
        'vacio': arbol.es_vacio()
    }


def recorrido_inorden(nodo):
    if nodo is None:
        return []
    return recorrido_inorden(nodo.get_izquierdo()) + [nodo.get_dato()] + recorrido_inorden(nodo.get_derecho())


def recorrido_preorden(nodo):
    if nodo is None:
        return []
    return [nodo.get_dato()] + recorrido_preorden(nodo.get_izquierdo()) + recorrido_preorden(nodo.get_derecho())


def recorrido_postorden(nodo):
    if nodo is None:
        return []
    return recorrido_postorden(nodo.get_izquierdo()) + recorrido_postorden(nodo.get_derecho()) + [nodo.get_dato()]


@arbol_bp.route('/estructura', methods=['GET'])
def obtener_estructura():
    """
    Devuelve la estructura completa del árbol para visualización.
    """
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
    """Elimina una rama completa del árbol."""
    data = request.get_json()
    valor = data.get('valor')

    try:
        valor_int = int(valor)

        print(f"🔍 Intentando eliminar rama del nodo: {valor_int}")

        # Verificar si el nodo existe
        nodo_existe = arbol.buscar_x(valor_int) is not None
        print(f"🔍 Nodo existe: {nodo_existe}")

        if not nodo_existe:
            return jsonify({
                'exito': False,
                'mensaje': f'Nodo {valor_int} no encontrado'
            })

        # Primero obtenemos información de la rama antes de eliminarla
        rama_info = arbol.obtener_rama(valor_int)
        cantidad_nodos = arbol.contar_nodos_rama(valor_int)

        print(f"🔍 Rama a eliminar: {rama_info}")
        print(f"🔍 Cantidad de nodos en la rama: {cantidad_nodos}")

        # Eliminar la rama
        exito = arbol.eliminar_rama(valor_int)

        print(f"🔍 Eliminación exitosa: {exito}")

        # Verificar si el nodo aún existe después de la eliminación
        nodo_despues = arbol.buscar_x(valor_int) is not None
        print(f"🔍 Nodo existe después de eliminar: {nodo_despues}")

        return jsonify({
            'exito': exito,
            'mensaje': f'Rama eliminada: {cantidad_nodos} nodos removidos' if exito else 'No se pudo eliminar la rama',
            'rama_eliminada': rama_info if exito else [],
            'cantidad_nodos': cantidad_nodos if exito else 0,
            'estadisticas': obtener_estadisticas()
        })

    except ValueError:
        return jsonify({
            'exito': False,
            'mensaje': 'Valor no válido'
        })
    except Exception as e:
        print(f"❌ Error al eliminar rama: {e}")
        return jsonify({
            'exito': False,
            'mensaje': f'Error interno: {str(e)}'
        })


@arbol_bp.route('/info-rama/<int:valor>', methods=['GET'])
def info_rama(valor):
    """Obtiene información sobre una rama específica."""
    try:
        rama = arbol.obtener_rama(valor)
        if rama is None:
            return jsonify({'error': 'Nodo no encontrado'}), 404

        return jsonify({
            'valor_raiz': valor,
            'rama': rama,
            'cantidad_nodos': len(rama),
            # Reutilizamos método interno
            'altura_rama': arbol._altura(arbol.buscar_x(valor))
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
