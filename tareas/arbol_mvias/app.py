from flask import Flask
from controllers.arbol_controller import arbol_bp

app = Flask(__name__)
app.register_blueprint(arbol_bp)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
