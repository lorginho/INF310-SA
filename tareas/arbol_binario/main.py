"""
main.py
Punto de entrada principal de la aplicación
Autor: Lorgio Añez J.
Fecha: 2025-08-283
Descripción: Archivo principal que inicia la aplicación del árbol binario
"""

from views.vista_arbol import VistaArbol


if __name__ == "__main__":
    vista = VistaArbol()
    vista.ejecutar()
