from models.nodo_mvias import NodoMvias


class ArbolMvias:
    def __init__(self, m=4):
        self.raiz = None
        self.m = m

    def insertar(self, valor):
        if self.raiz is None:
            self.raiz = NodoMvias(self.m)
            self.raiz.insertar_valor(valor)
            return True
        else:
            return self._insertar(self.raiz, valor)

    def _insertar(self, nodo, valor):
        # Verificar si el valor ya existe en este nodo
        if valor in nodo.valores:
            return False  # Valor duplicado

        if nodo.esta_lleno():
            # Encontrar la posición del hijo apropiado
            pos = nodo.encontrar_posicion(valor)
            if nodo.hijos[pos] is None:
                nodo.hijos[pos] = NodoMvias(self.m)
            return self._insertar(nodo.hijos[pos], valor)
        else:
            nodo.insertar_valor(valor)
            return True

    def buscar(self, valor):
        return self._buscar(self.raiz, valor) if self.raiz else False

    def _buscar(self, nodo, valor):
        if nodo is None:
            return False

        if valor in nodo.valores:
            return True

        pos = nodo.encontrar_posicion(valor)
        return self._buscar(nodo.hijos[pos], valor)

    def eliminar(self, valor):
        # Implementación básica de eliminación
        # En un árbol M-Vías completo esto sería más complejo
        pass

    def inorden(self):
        resultado = []
        self._inorden(self.raiz, resultado)
        return resultado

    def _inorden(self, nodo, resultado):
        if nodo is not None:
            for i in range(len(nodo.valores)):
                if nodo.hijos[i] is not None:
                    self._inorden(nodo.hijos[i], resultado)
                resultado.append(nodo.valores[i])
            if nodo.hijos[-1] is not None:
                self._inorden(nodo.hijos[-1], resultado)

    def preorden(self):
        resultado = []
        self._preorden(self.raiz, resultado)
        return resultado

    def _preorden(self, nodo, resultado):
        if nodo is not None:
            resultado.extend(nodo.valores)
            for hijo in nodo.hijos:
                self._preorden(hijo, resultado)

    def por_niveles(self):
        if self.raiz is None:
            return []

        resultado = []
        cola = [self.raiz]

        while cola:
            nivel_actual = []
            siguiente_nivel = []

            for nodo in cola:
                if nodo:
                    nivel_actual.append(nodo.valores)
                    siguiente_nivel.extend(
                        [h for h in nodo.hijos if h is not None])
                else:
                    nivel_actual.append(None)

            resultado.append(nivel_actual)
            cola = siguiente_nivel

        return resultado

    def obtener_estadisticas(self):
        if not self.raiz:
            return {"total_nodos": 0, "utilizacion_promedio": 0}

        total_nodos = 0
        total_utilizacion = 0

        def contar_nodos(nodo):
            nonlocal total_nodos, total_utilizacion
            if nodo:
                total_nodos += 1
                total_utilizacion += len(nodo.valores) / (self.m - 1)
                for hijo in nodo.hijos:
                    contar_nodos(hijo)

        contar_nodos(self.raiz)

        return {
            "total_nodos": total_nodos,
            "utilizacion_promedio": total_utilizacion / total_nodos if total_nodos > 0 else 0,
            "max_valores_por_nodo": self.m - 1
        }

    def to_dict(self):
        """Convierte el árbol a un formato JSON para la visualización"""
        def nodo_a_dict(nodo):
            if nodo is None:
                return None
            return {
                "valores": nodo.valores,
                "hijos": [nodo_a_dict(hijo) for hijo in nodo.hijos],
                "esta_lleno": nodo.esta_lleno(),
                "cantidad_valores": len(nodo.valores),
                "cantidad_hijos": nodo.cantidad_hijos()
            }

        return nodo_a_dict(self.raiz)
