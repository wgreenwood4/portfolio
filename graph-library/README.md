# GraphLib

### *A lightweight and extensible Python graph library for education, algorithm demos, and graph theory exploration.*

## Features

* Core graph data structures (`Graph`, `DisjointSet`)
* BFS and DFS traversals
* Pathfinding algorithms:
  * Dijkstra
  * Bellman–Ford
  * Floyd–Warshall
* Minimum Spanning Tree algorithms:
  * Kruskal
  * Prim
* Visualization with Matplotlib
* Graph analysis utilities (e.g. component detection)

## Installation

```bash
git clone https://github.com/your-username/graphlib.git
cd graph-library
pip install -r requirements.txt
```

## Usage

Let's quickly demonstrate how to create the `test.py` demonstration from this repo. Here’s how to get started:

```python
# Import modules as needed
from graphlib.core import Graph
from graphlib.extras import algorithms, analysis, mst, pathfinding, traversals, visuals
from graphlib.utils import graph_info_file
```

Once imported, you can create graphs, run algorithms, and visualize structures.

```python
# Create an undirected, weighted graph
G = Graph(directed=False, weighted=True)
G.add_edge("A", "B", 3)
G.add_edge("B", "C", 1)

# Execute Dijkstra's Algorithm
_, dist = pathfinding.dijkstra(G, "A")
print(dist)

# Create visualization
visuals.draw_graph(G)
```
Finally, run with from **outside the graphlib directory (../graphlib)**:
```bash
python test.py
```
Expected output:
```
{'A': 0, 'B': 3, 'C': 4}
```

## Modules

| Module               | Purpose                        |
|----------------------|--------------------------------|
| `core`               | Base graph data structures     |
| `extras/algorithms`  | Miscellaneous algorithms       |
| `extras/analysis`    | Graph analysis utilities       |
| `extras/mst`         | Minimum spanning tree algorithm|
| `extras/pathfinding` | Shortest-path algorithms       |
| `extras/traversals`  | BFS and DFS                    |
| `extras/visuals`     | Graph visualization            |
| `utils`              | Graph file utilities           |


## Future Goals:
* Clique detection and coloring algorithms (with visualization)
* Planarity checking and related tools
* Expand `pathfinding.py` (e.g., A*)
* Package the library for PyPI (pip installable)

## Author
Will Greenwood | [GitHub](https://github.com/wgreenwood4)
