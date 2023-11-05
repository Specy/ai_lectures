import heapq
import manhattan_distance

def best_first_search(graph, start, goal):
    visited = set()
    queue = [(0, start, [])]

    while queue: 
        # Coda di priorita con priorita sulla funzione euristica
        _, current, path = heapq.heappop(queue)

        if current == goal:
            # Se abbiamo raggiunto la destinazione, ritorniamo il percorso
            return path + [current]

        if current in visited:
            continue

        visited.add(current)
        path = path + [current]

        # Per ogni vicino non visitato aggiungiamolo alla coda
        for neighbor in graph.neighbors(current):
            if neighbor not in visited:
                priority = manhattan_distance.manhattan_distance(neighbor, goal)
                heapq.heappush(queue, (priority, neighbor, path))
              
    # Se non abbiamo trovato nessun percorso, ritorniamo None
    return None
