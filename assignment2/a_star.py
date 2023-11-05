import heapq
from manhattan_distance import manhattan_distance

def a_star_search(graph, start, goal):
    visited = set()
    queue = []
    # La priorità è (f_score, stato)
    # Dove f_score = g_score + h_score (costo fino a qui + euristica)
    heapq.heappush(queue, (0 + manhattan_distance(start, goal), start, []))
    g_scores = {start: 0}  # Costo per raggiungere il nodo

    while queue:
        _, current, path = heapq.heappop(queue)

        if current == goal:
            return path + [current]

        if current in visited:
            continue

        visited.add(current)
        path = path + [current]

        for neighbor in graph.neighbors(current):
            if neighbor not in visited:
                # Sulla griglia costa uno spostarsi
                tentative_g_score = g_scores[current] + 1 

                # Se non abbiamo ancora visitato il vicino o abbiamo trovato un percorso migliore
                if neighbor not in g_scores or tentative_g_score < g_scores[neighbor]:
                    g_scores[neighbor] = tentative_g_score
                    f_score = tentative_g_score + manhattan_distance(neighbor, goal)
                    heapq.heappush(queue, (f_score, neighbor, path))

    return None
