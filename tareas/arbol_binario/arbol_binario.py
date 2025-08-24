from nodo import Nodo


class ArbolBinario:
    def __init__(self):
        """
        Inicializa la instancia de ArbolBinario
        """
        self.raiz = Nodo()
        self.raiz = None

    def insertar_nodo(self, ele):
        nuevo = Nodo()
        nuevo.set_elemento(ele)

        if self.raiz == None:
            self.raiz = nuevo
        else:
            aux = self.raiz

            while aux != None:
                padre = aux
                if (ele < aux.get_elemento()):
                    aux = aux.get_hijo_izq()
                else:
                    aux = aux.get_hijo_der()
            if padre.get_elemento() > nuevo.get_elemento():
                padre._izq = nuevo
            else:
                padre._der = nuevo

    def recorrer(self, n):
        """Imprime en consola el arbol ordenado por valores"""
        if (n != None):
            self.recorrer(n.get_hijo_izq())
            print(n.get_elemento())
            self.recorrer(n.get_hijo_der())


def main():
    a = ArbolBinario()
    a.insertar_nodo(107)
    a.insertar_nodo(15)
    a.insertar_nodo(6)
    a.insertar_nodo(2230)
    a.insertar_nodo(322)
    a.recorrer(a.raiz)

    n = Nodo()
    n.set_hijo_der(10)
    n.set_hijo_izq(21)
    # n.set_elemento(15)
    print("Elemento raiz del nodo")
    print(n.get_elemento())
    print(n.get_hijo_izq())
    print(n.get_hijo_der())


if __name__ == '__main__':
    main()
