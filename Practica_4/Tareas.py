class Tarea:
    def __init__(self, nombre, fallos, intentos=0):
        self.nombre = nombre
        self.fallos = fallos
        self.intentos = intentos
    def fallo(self):
        self.fallos -= 1
        self.intentos += 1
        print("TAREA:", self.nombre, "- FALLIDA")
    def exito(self):
        print("TAREA:", self.nombre, "- COMPLETADA")

class GestorTareas:
    def __init__(self):
        self.cola = []
    def enque_tail(self, tarea):
        self.cola.append(tarea)
    def deque_head(self):
        if not self.is_empty():
            return self.cola.pop(0)
        return None
    def head(self):
        if not self.is_empty():
            return self.cola[0]
        return None
    def is_empty(self):
        return self.cola == []
    def fallo(self):
        tarea = self.head()
        if tarea:
            tarea.fallo()
            self.deque_head()
            self.enque_tail(tarea)
    def exito(self):
        tarea = self.head()
        if tarea:
            tarea.exito()
            self.deque_head()
    def mostrar(self):
        estado = [[t.nombre, t.fallos, t.intentos] for t in self.cola]
        print("Cola:", estado)

gestor = GestorTareas()

tareas = [
    Tarea("T1", 1, 0),
    Tarea("T2", 0, 0),
    Tarea("T3", 2, 0),
    Tarea("T4", 1, 0),
    Tarea("T5", 2, 2),
    Tarea("T6", 2, 1),
]

for t in tareas:
    gestor.enque_tail(t)

gestor.fallo()
gestor.mostrar()
gestor.exito()
gestor.mostrar()
gestor.fallo()
gestor.mostrar()
gestor.fallo()
gestor.mostrar()
gestor.fallo()
gestor.mostrar()
gestor.fallo()
gestor.mostrar()
