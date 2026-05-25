class NodoArbol:
    def __init__(self, clave, valor, izquierdo=None, derecho=None, padre=None):
        self.clave = clave
        self.cargaUtil = valor
        self.hijoIzquierdo = izquierdo
        self.hijoDerecho = derecho
        self.padre = padre

    def tieneHijoIzquierdo(self):
        return self.hijoIzquierdo

    def tieneHijoDerecho(self):
        return self.hijoDerecho

    def esRaiz(self):
        return not self.padre

    def esHoja(self):
        return not (self.hijoDerecho or self.hijoIzquierdo)

    def tieneAlgunHijo(self):
        return self.hijoDerecho or self.hijoIzquierdo

    def tieneAmbosHijos(self):
        return self.hijoDerecho and self.hijoIzquierdo


def insertar_nodo(raiz, clave, valor=None):
    if raiz is None:
        return NodoArbol(clave, valor)

    actual = raiz
    while True:
        if clave < actual.clave:
            if actual.hijoIzquierdo is None:
                actual.hijoIzquierdo = NodoArbol(clave, valor, padre=actual)
                break
            else:
                actual = actual.hijoIzquierdo
        elif clave > actual.clave:
            if actual.hijoDerecho is None:
                actual.hijoDerecho = NodoArbol(clave, valor, padre=actual)
                break
            else:
                actual = actual.hijoDerecho
        else:
            actual.cargaUtil = valor
            break
    return raiz


def arbol_a_diccionario(nodo):
    if nodo is None:
        return None
    if not nodo.tieneAlgunHijo():
        return None
    
    hijos = {}
    if nodo.hijoIzquierdo:
        hijos[nodo.hijoIzquierdo.clave] = arbol_a_diccionario(nodo.hijoIzquierdo)
    if nodo.hijoDerecho:
        hijos[nodo.hijoDerecho.clave] = arbol_a_diccionario(nodo.hijoDerecho)
    return hijos if hijos else None



lista = [1, 13, 11, 5, 9, 10, 1, 12, 3, 6] 

raiz = None
for numero in lista:
    raiz = insertar_nodo(raiz, numero, numero)

resultado = {raiz.clave: arbol_a_diccionario(raiz)}

print("Diccionario del árbol:")
print(resultado)
