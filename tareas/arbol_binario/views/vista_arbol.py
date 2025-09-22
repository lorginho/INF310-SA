"""
views/vista_arbol.py
Vista para interfaz de usuario del árbol binario (MVC)
Autor: Lorgio Añez J.
Fecha: 2025-09-01
Descripción: Vista que proporciona una interfaz de consola para interactuar con el árbol binario
"""


from controllers.controlador_arbol import ControladorArbol


class VistaArbol:
    """Vista para interactuar con el árbol binario a través de la consola."""

    def __init__(self):
        """Inicializa la vista con un controlador de árbol."""
        self.controlador = ControladorArbol()

    def ejecutar(self):
        """Método principal que inicia la interfaz de usuario."""
        while True:
            print("\n--- MENÚ ÁRBOL BINARIO ---")
            print("1. Insertar Nodo INDIVIDUAL")
            print("2. Insertar MULTIPLES Nodos")
            print("3. Verificar si está VACIO")
            print("4. Verificar si es HOJA")
            print("5. Buscar VALOR")
            print("6. Recorrido IN-Orden Iz.Ra.De")
            print("7. Recorrido PRE-Orden Ra.Iz.De")
            print("8. Recorrido POST-Orden Iz.De.Ra")
            print("9. Recorrido por AMPLITUD (Niveles)")
            print("0. Salir")

            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                self._insertar_nodo_individual()
            elif opcion == "2":
                self._insertar_multiples_nodos()
            elif opcion == "3":
                self._verificar_vacio()
            elif opcion == "4":
                self._verificar_hoja()
            elif opcion == "5":
                self._buscar_valor()
            elif opcion == "6":
                self._recorrido_in_orden()
            elif opcion == "7":
                self._recorrido_pre_orden()
            elif opcion == "8":
                self._recorrido_post_orden()
            elif opcion == "9":
                self._recorrido_amplitud()
            elif opcion == "0":
                print("Saliendo del programa...")
                break
            else:
                print("Opción no válida. Intente nuevamente.")

    def _insertar_nodo_individual(self):
        """Maneja la inserción de un nodo individual."""
        try:
            valor = int(input("Ingrese el valor a insertar: "))
            if self.controlador.insertar_nodo(valor):
                print(f"Valor {valor} insertado correctamente.")
            else:
                print(f"Valor {valor} ya existe en el arbol. No se inserto.")
        except ValueError:
            print("Error: Por favor ingrese un valor entero válido.")

    def _insertar_multiples_nodos(self):
        """Maneja la inserción de múltiples nodos a la vez."""
        try:
            valores_str = input(
                "Ingrese los valores a insertar (separados por comas o espacios): ")

            # Procesar la entrada para aceptar tanto comas como espacios como separadores
            valores = []
            for parte in valores_str.replace(',', ' ').split():
                if parte.strip():  # Ignorar partes vacías
                    valores.append(int(parte.strip()))

            if not valores:
                print("No se ingresaron valores válidos.")
                return

            insertados = 0
            duplicados = 0

            # Insertar todos los valores
            for valor in valores:
                if self.controlador.insertar_nodo(valor):
                    insertados += 1
                else:
                    duplicados += 1

            print(f"Se insertaron {insertados} nodos correctamente.")
            if duplicados > 0:
                print(f"Se omitieron {duplicados} valores duplicados.")

        except ValueError:
            print(
                "Error: Por favor ingrese valores enteros válidos separados por comas o espacios.")

    def _verificar_vacio(self):
        """Maneja la verificación de árbol vacío."""
        vacio = self.controlador.es_vacio()
        print("El árbol está vacío." if vacio else "El árbol no está vacío.")

    def _verificar_hoja(self):
        """Maneja la verificación de nodo hoja."""
        try:
            valor = int(input("Ingrese el valor a verificar: "))
            es_hoja = self.controlador.es_hoja(valor)
            if es_hoja:
                print(f"El nodo con valor {valor} es una hoja.")
            else:
                print(f"El nodo con valor {valor} no es una hoja o no existe.")
        except ValueError:
            print("Error: Por favor ingrese un valor entero válido.")

    def _buscar_valor(self):
        """Maneja la búsqueda de un valor."""
        try:
            valor = int(input("Ingrese el valor a buscar: "))
            encontrado = self.controlador.buscar_x(valor)
            print(
                f"Valor {valor} encontrado." if encontrado else f"Valor {valor} no encontrado.")
        except ValueError:
            print("Error: Por favor ingrese un valor entero válido.")

    def _recorrido_in_orden(self):
        """Maneja el recorrido in-orden."""
        print("Recorrido In-Orden Iz.Ra.De:", end=" ")
        self.controlador.in_orden()

    def _recorrido_pre_orden(self):
        """Maneja el recorrido pre-orden."""
        print("Recorrido Pre-Orden Ra.Iz.De:", end=" ")
        self.controlador.pre_orden()

    def _recorrido_post_orden(self):
        """Maneja el recorrido post-orden."""
        print("Recorrido Post-Orden Iz.De.Ra:", end=" ")
        self.controlador.post_orden()

    def _recorrido_amplitud(self):
        """Maneja el recorrido por amplitud."""
        resultado = self.controlador.amplitud()
        print("Recorrido por Amplitud:", resultado)
