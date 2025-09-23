from flask import Flask, render_template, request, jsonify
from controllers.arbol_controller import arbol_bp

app = Flask(__name__)
app.secret_key = 'arbol_binario_secret_key'

# Registrar blueprint
app.register_blueprint(arbol_bp)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
