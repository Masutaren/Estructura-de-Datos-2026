from cola import Cola
from pila import Pila

class Estadisticas:
    def __init__(self, datos):
        self.cola = Cola()
        self.pila = Pila()
        for d in datos:
            self.cola.enque(d)
        self.lista = []

    def pasar_a_pila(self):
        n = self.cola.size()
        for i in range(n):
            elemento = self.cola.deque()
            self.pila.push(elemento)

    def pasar_a_lista(self):
        n = self.pila.size()
        for i in range(n):
            self.lista.append(self.pila.pop())

    def calcular_media(self):
        suma = 0
        for i in range(len(self.lista)):
            suma += self.lista[i]
        return suma / len(self.lista)

    def calcular_moda(self):
        max_repeticiones = 0
        moda = []
        for i in range(len(self.lista)):
            repeticiones = 0
            for j in range(len(self.lista)):
                if self.lista[i] == self.lista[j]:
                    repeticiones += 1
            if repeticiones > max_repeticiones:
                max_repeticiones = repeticiones
                moda = [self.lista[i]]
            elif repeticiones == max_repeticiones and self.lista[i] not in moda:
                moda.append(self.lista[i])
        return moda

    def calcular_varianza(self):
        media = self.calcular_media()
        suma = 0
        for i in range(len(self.lista)):
            suma += (self.lista[i] - media) ** 2
        return suma / len(self.lista)

    def preparar(self):
        self.pasar_a_pila()
        self.pasar_a_lista()

datos = [1200.5, 11890.0, 13010.35, 14100.0, 13650.8, 14999.99, 15800.0, 16250.25, 15120.0, 14780.4, 13999.0, 15550.75]

estadisticas = Estadisticas(datos)
estadisticas.preparar()

print("Media:", estadisticas.calcular_media())
print("Moda:", estadisticas.calcular_moda())
print("Varianza:", estadisticas.calcular_varianza())
