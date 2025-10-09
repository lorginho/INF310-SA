"""
controllers/graph_controller.py
Autor: Lorgio Añez J.
Fecha: 2025-10-09

Propósito: Orquestar la lógica de la aplicación (Controlador en MVC)
Responsabilidad: Coordinar entre Modelo y Vista, manejar el flujo de la aplicación
Clase Principal: GraphController

❌ NO almacena datos persistentes
❌ NO formatea salidas directamente
✅ SI coordina Modelo y Vista
✅ SI maneja el flujo de la aplicación

Atributos:

- modelo: Instancia de GraphModel
- vista: Instancia de GraphView
- tipo_grafo_actual: String que indica el tipo actual

Métodos Principales:

- ejecutar(): Bucle principal de la aplicación
- agregar_vertice(), eliminar_vertice(): Operaciones con vértices
- agregar_arista(), eliminar_arista(): Operaciones con aristas
- mostrar_lista_adyacencia(), mostrar_matriz_adyacencia(): Visualización
- cambiar_tipo_grafo(): Cambia entre dirigido/no dirigido
- poblar_grafo_aleatorio(): Generación automática de grafos
- _generar_vertices_aleatorios(), _generar_aristas_aleatorias(): Helper methods

Flujo Principal:

1. Inicializa Modelo y Vista
2. Muestra menú principal
3. Procesa selección del usuario
4. Delega operaciones al Modelo
5. Muestra resultados através de la Vista

"""
import random
import string
from models.graph_model import GraphModel
from views.graph_view import GraphView


class GraphController:
    def __init__(self):
        """Inicializa el controlador con modelo y vista"""
        self.modelo = None
        self.vista = GraphView()
        self.tipo_grafo_actual = "no dirigido"
        self.inicializar_grafo(dirigido=False)

    def inicializar_grafo(self, dirigido=False):
        """Inicializa un nuevo grafo"""
        self.modelo = GraphModel(dirigido=dirigido)
        self.tipo_grafo_actual = "dirigido" if dirigido else "no dirigido"
        self.vista.mostrar_exito(
            f"Nuevo grafo {self.tipo_grafo_actual} creado")

    def cambiar_tipo_grafo(self):
        """Permite cambiar entre grafo dirigido y no dirigido"""
        if self.modelo.obtener_vertices():
            self.vista.mostrar_error(
                "No se puede cambiar el tipo con vértices existentes. Use 'Limpiar Grafo' primero.")
            return

        nuevo_tipo = not self.modelo.es_dirigido()
        self.inicializar_grafo(nuevo_tipo)
        self.vista.mostrar_exito(f"Grafo cambiado a {self.tipo_grafo_actual}")

    def ejecutar(self):
        """Bucle principal de la aplicación"""
        while True:
            try:
                opcion = self.vista.mostrar_menu(self.tipo_grafo_actual)

                if opcion == '1':
                    self.agregar_vertice()
                elif opcion == '2':
                    self.eliminar_vertice()
                elif opcion == '3':
                    self.agregar_arista()
                elif opcion == '4':
                    self.eliminar_arista()
                elif opcion == '5':
                    self.mostrar_lista_adyacencia()
                elif opcion == '6':
                    self.mostrar_matriz_adyacencia()
                elif opcion == '7':
                    self.mostrar_informacion_grafo()
                elif opcion == '8':
                    self.cambiar_tipo_grafo()
                elif opcion == '9':
                    self.limpiar_grafo()
                elif opcion == '10':  # Nueva opción
                    self.poblar_grafo_aleatorio()
                elif opcion == '11':
                    self.vista.mostrar_mensaje("¡Hasta luego!")
                    break
                else:
                    self.vista.mostrar_error("Opción inválida")

            except Exception as e:
                self.vista.mostrar_error(f"Error inesperado: {str(e)}")

    def poblar_grafo_aleatorio(self):
        """Puebla el grafo con vértices y aristas aleatorias"""
        if self.modelo.obtener_vertices():
            self.vista.mostrar_error(
                "El grafo ya tiene vértices. Use 'Limpiar Grafo' primero.")
            return

        num_vertices, num_aristas = self.vista.obtener_parametros_poblacion()

        if num_vertices is None or num_aristas is None:
            return

        # Generar vértices
        vertices_creados = self._generar_vertices_aleatorios(num_vertices)
        self.vista.mostrar_progreso_poblacion(vertices_creados, 0)

        # Generar aristas
        aristas_creadas = self._generar_aristas_aleatorias(num_aristas)

        self.vista.mostrar_exito(
            f"Grafo poblado con {vertices_creados} vértices y {aristas_creadas} aristas")

    def _generar_vertices_aleatorios(self, num_vertices):
        """Genera vértices aleatorios con nombres únicos"""
        nombres_vertices = []

        # Generar nombres de vértices (A, B, C,... o V1, V2, V3,...)
        if num_vertices <= 26:
            # Usar letras A-Z
            nombres_vertices = [chr(65 + i) for i in range(num_vertices)]
        else:
            # Usar V1, V2, V3,...
            nombres_vertices = [f"V{i+1}" for i in range(num_vertices)]

        # Agregar vértices al modelo
        for nombre in nombres_vertices:
            self.modelo.agregar_vertice(nombre)

        return len(nombres_vertices)

    def _generar_aristas_aleatorias(self, num_aristas):
        """Genera aristas aleatorias entre los vértices existentes"""
        vertices = self.modelo.obtener_vertices()
        if len(vertices) < 2 and num_aristas > 0:
            self.vista.mostrar_error(
                "Se necesitan al menos 2 vértices para crear aristas")
            return 0

        aristas_creadas = 0
        max_intentos = num_aristas * 3  # Límite para evitar bucles infinitos
        intentos = 0

        while aristas_creadas < num_aristas and intentos < max_intentos:
            # Seleccionar vértices aleatorios
            vertice1 = random.choice(vertices)
            vertice2 = random.choice(vertices)

            # En grafos no dirigidos, evitar bucles
            if not self.modelo.es_dirigido() and vertice1 == vertice2:
                intentos += 1
                continue

            # Intentar agregar la arista
            if self.modelo.agregar_arista(vertice1, vertice2):
                aristas_creadas += 1
                self.vista.mostrar_progreso_poblacion(
                    len(vertices), aristas_creadas)

            intentos += 1

        if aristas_creadas < num_aristas:
            self.vista.mostrar_error(
                f"Solo se pudieron crear {aristas_creadas} de {num_aristas} aristas solicitadas")

        return aristas_creadas

    def agregar_vertice(self):
        """Maneja la operación de agregar vértice"""
        vertice = self.vista.obtener_entrada_vertice(
            "Ingrese vértice a agregar: ")
        if not vertice:
            self.vista.mostrar_error("El vértice no puede estar vacío")
            return

        if self.modelo.agregar_vertice(vertice):
            self.vista.mostrar_exito(
                f"Vértice '{vertice}' agregado exitosamente")
        else:
            self.vista.mostrar_error(f"El vértice '{vertice}' ya existe")

    def eliminar_vertice(self):
        """Maneja la operación de eliminar vértice"""
        if not self.modelo.obtener_vertices():
            self.vista.mostrar_error("El grafo está vacío")
            return

        vertice = self.vista.obtener_entrada_vertice(
            "Ingrese vértice a eliminar: ")
        if self.modelo.eliminar_vertice(vertice):
            self.vista.mostrar_exito(
                f"Vértice '{vertice}' eliminado exitosamente")
        else:
            self.vista.mostrar_error(f"Vértice '{vertice}' no encontrado")

    def agregar_arista2(self):
        """Maneja la operación de agregar arista"""
        vertices = self.modelo.obtener_vertices()
        if len(vertices) < 2:
            self.vista.mostrar_error(
                "Se necesitan al menos 2 vértices para agregar una arista")
            return

        vertice1, vertice2 = self.vista.obtener_entrada_arista()

        if not vertice1 or not vertice2:
            self.vista.mostrar_error("Ambos vértices son requeridos")
            return

        if vertice1 == vertice2:
            self.vista.mostrar_error("No se puede crear un bucle (self-loop)")
            return

        if self.modelo.agregar_arista(vertice1, vertice2):
            if self.modelo.es_dirigido():
                self.vista.mostrar_exito(
                    f"Arista dirigida ({vertice1} → {vertice2}) agregada exitosamente")
            else:
                self.vista.mostrar_exito(
                    f"Arista no dirigida ({vertice1} - {vertice2}) agregada exitosamente")
        else:
            self.vista.mostrar_error(
                f"Error al agregar arista ({vertice1}-{vertice2})")

    def agregar_arista(self):
        """Maneja la operación de agregar arista"""
        vertices = self.modelo.obtener_vertices()
        if len(vertices) < 1:  # Cambiado de 2 a 1
            self.vista.mostrar_error(
                "Se necesita al menos 1 vértice para agregar una arista")
            return

        vertice1, vertice2 = self.vista.obtener_entrada_arista()

        if not vertice1 or not vertice2:
            self.vista.mostrar_error("Ambos vértices son requeridos")
            return

        # PERMITIR BUCLE EN GRAFOS DIRIGIDOS
        if vertice1 == vertice2 and not self.modelo.es_dirigido():
            self.vista.mostrar_error(
                "No se puede crear un bucle en grafos no dirigidos")
            return

        if self.modelo.agregar_arista(vertice1, vertice2):
            if self.modelo.es_dirigido():
                if vertice1 == vertice2:
                    self.vista.mostrar_exito(
                        f"Bucle dirigido ({vertice1} ↺) agregado exitosamente")
                else:
                    self.vista.mostrar_exito(
                        f"Arista dirigida ({vertice1} → {vertice2}) agregada exitosamente")
            else:
                self.vista.mostrar_exito(
                    f"Arista no dirigida ({vertice1} - {vertice2}) agregada exitosamente")
        else:
            self.vista.mostrar_error(
                f"Error al agregar arista ({vertice1}-{vertice2})")

    def eliminar_arista(self):
        """Maneja la operación de eliminar arista"""
        if not self.modelo.obtener_vertices():
            self.vista.mostrar_error("El grafo está vacío")
            return

        vertice1, vertice2 = self.vista.obtener_entrada_arista()

        if self.modelo.eliminar_arista(vertice1, vertice2):
            if self.modelo.es_dirigido():
                self.vista.mostrar_exito(
                    f"Arista dirigida ({vertice1} → {vertice2}) eliminada exitosamente")
            else:
                self.vista.mostrar_exito(
                    f"Arista no dirigida ({vertice1} - {vertice2}) eliminada exitosamente")
        else:
            self.vista.mostrar_error(
                f"Arista ({vertice1}-{vertice2}) no encontrada")

    def mostrar_lista_adyacencia(self):
        """Muestra la lista de adyacencia"""
        if not self.modelo.obtener_vertices():
            self.vista.mostrar_grafo_vacio()
            return

        datos_grafo = self.modelo.obtener_datos_grafo()
        self.vista.mostrar_lista_adyacencia(datos_grafo)

    def mostrar_matriz_adyacencia(self):
        """Muestra la matriz de adyacencia"""
        if not self.modelo.obtener_vertices():
            self.vista.mostrar_grafo_vacio()
            return

        datos_grafo = self.modelo.obtener_datos_grafo()
        self.vista.mostrar_matriz_adyacencia(datos_grafo)

    def mostrar_informacion_grafo(self):
        """Muestra información completa del grafo"""
        if not self.modelo.obtener_vertices():
            self.vista.mostrar_grafo_vacio()
            return

        datos_grafo = self.modelo.obtener_datos_grafo()
        self.vista.mostrar_informacion_grafo(datos_grafo)

    def limpiar_grafo(self):
        """Limpia todo el grafo"""
        dirigido = self.modelo.es_dirigido()
        self.inicializar_grafo(dirigido)
        self.vista.mostrar_exito("Grafo limpiado exitosamente")
