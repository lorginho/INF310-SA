"""
views/graph_view.py
Autor: Lorgio Añez J.
Fecha: 2025-10-09

Propósito: Manejar la interfaz de usuario (Vista en MVC)
Responsabilidad: Mostrar información y capturar entradas del usuario
Clase Principal: GraphView

❌ NO conoce la lógica de negocio
❌ NO modifica datos directamente
✅ SI formatea la presentación
✅ SI captura entradas del usuario


Métodos Principales:

- mostrar_menu(tipo_actual): Muestra el menú principal
- mostrar_lista_adyacencia(datos_grafo): Muestra la lista de adyacencia
- mostrar_matriz_adyacencia(datos_grafo): Muestra la matriz de adyacencia
- mostrar_informacion_grafo(datos_grafo): Muestra estadísticas del grafo
- obtener_entrada_vertice(), obtener_entrada_arista(): Capturan inputs
- mostrar_exito(), mostrar_error(), mostrar_mensaje(): Feedback al usuario
- obtener_parametros_poblacion(): Parámetros para generación aleatoria

Características:

- Todos los métodos son estáticos
- Interfaz completamente en español
- Validación básica de entradas

"""

import random
import string


class GraphView:
    @staticmethod
    def mostrar_menu(tipo_actual):
        """Muestra las opciones del menú principal"""
        print(f"\n=== SISTEMA GRAFOS MVC (Grafo {tipo_actual}) ===")
        print("1. Agregar Vértice")
        print("2. Eliminar Vértice")
        print("3. Agregar Arista")
        print("4. Eliminar Arista")
        print("5. Mostrar Lista de Adyacencia")
        print("6. Mostrar Matriz de Adyacencia")
        print("7. Mostrar Información del Grafo")
        print("8. Cambiar Tipo de Grafo")
        print("9. Limpiar Grafo")
        print("10. Poblar Grafo Aleatoriamente")
        print("11. DFS - Recorrido en Profundidad")
        print("0. Salir")
        return input("Seleccione opción (1-11) Salir(0): ")

    @staticmethod
    def mostrar_lista_adyacencia(datos_grafo):
        """Muestra la lista de adyacencia"""
        print("\n--- LISTA DE ADYACENCIA ---")
        lista_adyacencia = datos_grafo['lista_adyacencia']
        for vertice in sorted(lista_adyacencia.keys()):
            vecinos = sorted(lista_adyacencia[vertice])
            print(f"{vertice}: {vecinos}")

    @staticmethod
    def mostrar_matriz_adyacencia(datos_grafo):
        """Muestra la matriz de adyacencia"""
        print("\n--- MATRIZ DE ADYACENCIA ---")
        vertices = datos_grafo['vertices']
        matriz = datos_grafo['matriz_adyacencia']

        # Encabezado
        print("   ", end="")
        for vertice in vertices:
            print(f"{vertice:>3}", end="")
        print()

        # Filas
        for i, vertice in enumerate(vertices):
            print(f"{vertice}: ", end="")
            for j in range(len(vertices)):
                print(f"{matriz[i][j]:>3}", end="")
            print()

    @staticmethod
    def mostrar_informacion_grafo(datos_grafo):
        """Muestra información completa del grafo"""
        print("\n--- INFORMACIÓN DEL GRAFO ---")
        vertices = datos_grafo['vertices']
        lista_adyacencia = datos_grafo['lista_adyacencia']
        dirigido = datos_grafo['dirigido']

        print(f"Tipo de Grafo: {'Dirigido' if dirigido else 'No Dirigido'}")
        print(f"Número de vértices: {len(vertices)}")
        print(f"Vértices: {vertices}")

        total_aristas = sum(len(vecinos)
                            for vecinos in lista_adyacencia.values())
        if not dirigido:
            total_aristas //= 2
        print(f"Número de aristas: {total_aristas}")

        print("\nGrados de los vértices:")
        for vertice in sorted(vertices):
            grado = len(lista_adyacencia.get(vertice, []))
            print(f"  {vertice}: {grado}")

    @staticmethod
    def obtener_entrada_vertice(mensaje="Ingrese vértice: "):
        """Obtiene entrada de vértice del usuario"""
        return input(mensaje).strip().upper()

    @staticmethod
    def obtener_entrada_arista():
        """Obtiene entrada de arista del usuario"""
        vertice1 = input("Ingrese primer vértice: ").strip().upper()
        vertice2 = input("Ingrese segundo vértice: ").strip().upper()
        return vertice1, vertice2

    @staticmethod
    def obtener_parametros_poblacion():
        """Obtiene parámetros para población aleatoria"""
        print("\n=== POBLAR GRAFO ALEATORIAMENTE ===")

        try:
            num_vertices = int(input("Número de vértices (3-15): "))
            if num_vertices < 3 or num_vertices > 15:
                raise ValueError(
                    "El número de vértices debe estar entre 3 y 15")

            max_aristas = num_vertices * (num_vertices - 1)

            num_aristas = int(input(f"Número de aristas (0-{max_aristas}): "))
            if num_aristas < 0 or num_aristas > max_aristas:
                raise ValueError(
                    f"El número de aristas debe estar entre 0 y {max_aristas}")

            return num_vertices, num_aristas

        except ValueError as e:
            print(f"Error: {e}")
            return None, None

    @staticmethod
    def mostrar_progreso_poblacion(vertices_creados, aristas_creadas):
        """Muestra el progreso de la población aleatoria"""
        print(f"Vértices creados: {vertices_creados}")
        print(f"Aristas creadas: {aristas_creadas}")

    @staticmethod
    def mostrar_mensaje(mensaje):
        """Muestra mensaje al usuario"""
        print(f"\n{mensaje}")

    @staticmethod
    def mostrar_error(error):
        """Muestra mensaje de error"""
        print(f"\nERROR: {error}")

    @staticmethod
    def mostrar_exito(mensaje):
        """Muestra mensaje de éxito"""
        print(f"\nÉXITO: {mensaje}")

    @staticmethod
    def mostrar_grafo_vacio():
        """Muestra mensaje cuando el grafo está vacío"""
        print("\nEl grafo está vacío")

    # MÉTODOS DFS
    @staticmethod
    def obtener_vertice_inicio_dfs():
        """Obtiene el vértice de inicio para DFS"""
        return input("Ingrese vértice de inicio para DFS: ").strip().upper()

    @staticmethod
    def mostrar_resultado_dfs(resultado, vertice_inicio):
        """Muestra el resultado del DFS"""
        print(f"\n--- DFS DESDE {vertice_inicio} ---")
        if not resultado:
            print("No se encontraron vértices alcanzables")
        else:
            print("Recorrido: " + " → ".join(resultado))
            print(f"Total de vértices visitados: {len(resultado)}")
