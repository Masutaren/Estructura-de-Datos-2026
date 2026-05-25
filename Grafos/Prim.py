class Graph:
    def __init__(self, graph):
        self.graph = graph

    def prim(self, root="0"):
        visitados = set([root])
        mst = []  # Lista de aristas del Minimum Spanning Tree
        total_peso = 0

        while len(visitados) < len(self.graph):
            menor_arista = None
            menor_peso = float("inf")

            for nodo in visitados:
                for vecino, peso in self.graph[nodo].items():
                    if vecino not in visitados and peso < menor_peso:
                        menor_peso = peso
                        menor_arista = (nodo, vecino)
            if menor_arista is None:
                break
            mst.append((menor_arista[0], menor_arista[1], menor_peso))
            total_peso += menor_peso
            visitados.add(menor_arista[1])
        return mst, total_peso

graph = {
   "0": {"1": 10, "2": 20},
   "1": {"0": 10, "3": 50, "4": 10},
   "2": {"0": 20, "3": 20, "4": 20},
   "3": {"1": 50, "2": 20, "4": 20},
   "4": {"1": 10, "2": 33, "3": 20, "5": 1},
   "5": {"3": 2, "4": 1},
}

g = Graph(graph)
mst, peso_total = g.prim("2")

print("Árbol de expansión mínimo (MST):", mst)
print("Peso total del MST:", peso_total)
