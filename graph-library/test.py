from graphlib.core import Graph
from graphlib.extras import algorithms, analysis, mst, pathfinding, traversals, visuals
from graphlib.utils import graph_info_file

G = Graph(directed=False, weighted=True)
G.add_edge("A", "B", 3)
G.add_edge("B", "C", 1)

_, dist = pathfinding.dijkstra(G, "A")
print(dist)

visuals.draw_graph(G)
