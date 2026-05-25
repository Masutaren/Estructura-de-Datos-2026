class Graph:
    def __init__(self, graph):
        self.graph = graph

    def dijkstra(self, start):
        distancias = {nodo: float("inf") for nodo in self.graph}
        distancias[start] = 0

        camino = {nodo: None for nodo in self.graph}

        no_visitados = set(self.graph.keys())

        while no_visitados:
            nodo_actual = min(no_visitados, key=lambda nodo: distancias[nodo])
            no_visitados.remove(nodo_actual)

            for vecino, peso in self.graph[nodo_actual].items():
                nueva_distancia = distancias[nodo_actual] + peso
                if nueva_distancia < distancias[vecino]:
                    distancias[vecino] = nueva_distancia
                    camino[vecino] = nodo_actual

        return distancias, camino

    def obtener_camino(self, camino, destino):
        ruta = []
        nodo = destino
        while nodo is not None:
            ruta.append(nodo)
            nodo = camino[nodo]
        return ruta[::-1]  # Para invertir la lista

graph = {
   "0": {"1": 9, "4": 6},
   "1": {"0": 9, "3": 8},
   "2": {"4": 5, "5": 6},
   "3": {"1": 8, "5": 1, "7": 7},
   "4": {"0": 6, "2": 5, "6": 3},
   "5": {"2": 6, "3": 1},
   "6": {"4": 3, "7": 2},
   "7": {"3": 7, "6": 2},
}

g = Graph(graph)
distancias, camino = g.dijkstra("0")

print("Distancias desde el nodo 0:", distancias)
print("Camino más corto de 0 a 7:", g.obtener_camino(camino, "7"))