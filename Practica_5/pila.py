class Pila:
    def __init__(self, pila=None, top=-1):
        if pila is None:
            pila = []
        self.pila = pila
        self.top = top
    def push(self, elemento):
        self.pila.append(elemento)
        self.top += 1
    def pop(self):
        if self.top == -1:
            return None
        elemento = self.pila[self.top]
        self.pila.pop()
        self.top -= 1
        return elemento
    def is_empty(self):
        return self.top == -1
    def size(self):
        return len(self.pila)
    def peek(self):
        return self.pila[self.top] if not self.is_empty() else None
