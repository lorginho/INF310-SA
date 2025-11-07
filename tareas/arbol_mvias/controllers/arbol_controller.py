from flask import Blueprint, request, jsonify, render_template
from models.arbol_mvias import ArbolMvias

arbol_bp = Blueprint('arbol', __name__)
arbol = ArbolMvias(m=4)


@arbol_bp.route('/')
def index():
    return render_template('index.html')


@arbol_bp.route('/insertar', methods=['POST'])
def insertar():
    try:
        data = request.get_json()
        valor = int(data.get('valor'))

        # Verificar si el valor ya existe
        if arbol.buscar(valor):
            return jsonify({
                'success': False,
                'error': f'El valor {valor} ya existe en el árbol'
            })

        insertado = arbol.insertar(valor)
        if insertado:
            return jsonify({
                'success': True,
                'arbol': arbol.to_dict(),
                'estadisticas': arbol.obtener_estadisticas()
            })
        else:
            return jsonify({
                'success': False,
                'error': f'No se pudo insertar el valor {valor}'
            })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@arbol_bp.route('/buscar', methods=['POST'])
def buscar():
    try:
        data = request.get_json()
        valor = int(data.get('valor'))
        encontrado = arbol.buscar(valor)
        return jsonify({
            'success': True,
            'encontrado': encontrado,
            'arbol': arbol.to_dict()
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@arbol_bp.route('/recorrido/<tipo>')
def obtener_recorrido(tipo):
    try:
        if tipo == 'inorden':
            resultado = arbol.inorden()
        elif tipo == 'preorden':
            resultado = arbol.preorden()
        elif tipo == 'niveles':
            resultado = arbol.por_niveles()
        else:
            return jsonify({'success': False, 'error': 'Tipo de recorrido no válido'})

        return jsonify({
            'success': True,
            'recorrido': resultado,
            'tipo': tipo
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@arbol_bp.route('/arbol')
def obtener_arbol():
    return jsonify({
        'success': True,
        'arbol': arbol.to_dict(),
        'estadisticas': arbol.obtener_estadisticas()
    })


@arbol_bp.route('/limpiar', methods=['POST'])
def limpiar_arbol():
    global arbol
    arbol = ArbolMvias(m=4)
    return jsonify({
        'success': True,
        'arbol': arbol.to_dict(),
        'estadisticas': arbol.obtener_estadisticas()
    })
