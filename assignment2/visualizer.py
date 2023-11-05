import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import a_star
import best_first_search

if __name__ == '__main__':
  # Codice per la visualizzazione (non interessante per l'esercizio)
  G = nx.grid_2d_graph(8, 8)
  black_positions = {(3, 2), (4, 1), (5, 2), (3, 3), (3, 4), (3, 5), (3, 6), (5, 6)}
  for pos in black_positions:
      G.remove_node(pos)

  start_position = (0, 0)
  end_position = (6,4)

  # Seleziona l'algoritmo da visualizzare
  # path = a_star.a_star_search(G, start_position, end_position)
  path = best_first_search.best_first_search(G, start_position, end_position)

  pos = {(x, y): (y, -x) for x, y in G.nodes()}
  nx.draw_networkx_nodes(G, pos=pos, node_size=600, node_color=['black' if node in black_positions else 'white' for node in G.nodes()], edgecolors='black')
  nx.draw_networkx_edges(G, pos=pos)

  point, = plt.plot([], [], marker='o', color='green', markersize=15)

  def update(frame):
      x, y = pos[path[frame]]
      point.set_data(x, y)
      return point,

  animation = FuncAnimation(plt.gcf(), update, frames=len(path), repeat=False, interval=500)
  plt.axis('off')
  plt.show()

