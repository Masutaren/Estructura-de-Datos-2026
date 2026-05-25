def BFS(grafo, start):
    visited = set()
    queue = [start]  
    
    while queue:
        node = queue.pop(0)
        if node not in visited:
            print(f"Visito nodo: {node}")
            visited.add(node)
            
            for neighbor in grafo[node]:
                if neighbor not in visited:
                    queue.append(neighbor)
                    print(f"--> Se agrega {neighbor}")
                    print("Cola:", queue)

    print(f"\nLista final de nodos visitados: {list(visited)}")


grafo = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F','G'],
    'D': [],
    'E': [],
    'F': [],
    'G': []
}

BFS(grafo, 'A')
