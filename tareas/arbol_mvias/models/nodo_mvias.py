class NodoMvias:
    def __init__(self, m=4):
        self.m = m  # Orden del árbol (máximo de hijos)
        self.valores = []  # Valores almacenados en el nodo
        self.hijos = [None] * m  # Referencias a los hijos

    def esta_lleno(self):
        return len(self.valores) >= self.m - 1

    def esta_vacio(self):
        return len(self.valores) == 0

    def cantidad_valores(self):
        return len(self.valores)

    def cantidad_hijos(self):
        return sum(1 for hijo in self.hijos if hijo is not None)

    def insertar_valor(self, valor):
        """Inserta un valor manteniendo el orden ascendente"""
        self.valores.append(valor)
        self.valores.sort()

    def encontrar_posicion(self, valor):
        """Encuentra la posición donde debería ir un valor"""
        for i, val in enumerate(self.valores):
            if valor < val:
                return i
        return len(self.valores)

    def __str__(self):
        return f"Nodo({self.valores})"
