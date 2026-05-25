class Graph:
    def __init__(self, graph):
        self.graph = graph
        self.edges = self._get_edges()

    def _get_edges(self):
        edges = []
        for nodo, vecinos in self.graph.items():
            for vecino, peso in vecinos.items():
                if (vecino, nodo, peso) not in edges:
                    edges.append((nodo, vecino, peso))
        return edges

    def find(self, parent, i):
        if parent[i] != i:
            parent[i] = self.find(parent, parent[i])
        return parent[i]

    def union(self, parent, rank, x, y):
        xroot = self.find(parent, x)
        yroot = self.find(parent, y)
        if rank[xroot] < rank[yroot]:
            parent[xroot] = yroot
        elif rank[xroot] > rank[yroot]:
            parent[yroot] = xroot
        else:
            parent[yroot] = xroot
            rank[xroot] += 1

    def kruskal(self):
        self.edges.sort(key=lambda x: x[2])
        parent = {}
        rank = {}
        for nodo in self.graph.keys():
            parent[nodo] = nodo
            rank[nodo] = 0
        mst = []
        total_peso = 0
        for u, v, peso in self.edges:
            if self.find(parent, u) != self.find(parent, v):
                mst.append((u, v, peso))
                total_peso += peso
                self.union(parent, rank, u, v)

        return mst, total_peso


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
mst, peso_total = g.kruskal()

print("Árbol de expansión mínimo (MST):", mst)
print("Peso total del MST:", peso_total)
