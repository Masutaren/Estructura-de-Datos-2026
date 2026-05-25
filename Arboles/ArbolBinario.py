class Nodo:
    def __init__(self, dato):
        self.dato = dato
        self.izquierdo = None
        self.derecho = None

    def agregar(self, dato):
        if dato < self.dato:
            if self.izquierdo is None:
                self.izquierdo = Nodo(dato)
            else:
                self.izquierdo.agregar(dato)
        else:
            if self.derecho is None:
                self.derecho = Nodo(dato)
            else:
                self.derecho.agregar(dato)

    def preorden(self, nodo):
        if nodo is not None:
            print(nodo.dato, end=", ")
            self.preorden(nodo.izquierdo)
            self.preorden(nodo.derecho)

    def inorden(self, nodo):
        if nodo is not None:
            self.inorden(nodo.izquierdo)
            print(nodo.dato, end=", ")
            self.inorden(nodo.derecho)

    def postorden(self, nodo):
        if nodo is not None:
            self.postorden(nodo.izquierdo)
            self.postorden(nodo.derecho)
            print(nodo.dato, end=", ")


datos = [3,1,2,4,5]
raiz = Nodo(datos[0])
for d in datos[1:]:
    raiz.agregar(d)

print("Preorden: "); raiz.preorden(raiz)    # 3, 1, 2, 4, 5
print("\nInorden: "); raiz.inorden(raiz)    # 1, 2, 3, 4, 5
print("\nPostorden: "); raiz.postorden(raiz) # 2, 1, 5, 4, 3
