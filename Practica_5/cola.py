class Cola:
    def __init__(self, cola=None):
        if cola is None:
            cola = []
        self.cola = cola
    def enque(self, item):
        self.cola.append(item)
    def deque(self):
        if self.is_empty():
            return None
        return self.cola.pop(0)
    def peek(self):
        return self.cola[0] if not self.is_empty() else None
    def is_empty(self):
        return self.cola == []
    def size(self):
        return len(self.cola)