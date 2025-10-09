"""
main.py
Autor: Lorgio Añez J.
Fecha: 2025-10-09

Propósito: Punto de entrada principal de la aplicación
Responsabilidad: Inicializar y lanzar el sistema
Contenido:
-   Función main() que crea el controlador principal
-   Mensaje de bienvenida
-   Gestión del flujo de ejecución inicial

"""
from controllers.graph_controller import GraphController


def main():
    """Punto de entrada principal de la aplicación"""
    print("=== APLICACIÓN GRAFOS MVC ===")
    print("Creando grafo no dirigido...")

    # Inicializar y ejecutar la aplicación
    aplicacion = GraphController()
    aplicacion.ejecutar()


if __name__ == "__main__":
    main()
