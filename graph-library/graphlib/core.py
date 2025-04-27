"""
core.py

Defines the Graph class and the DisjointSet (Union-Find) data structure.

Graph:
    - Supports both directed and undirected graphs
    - Supports both weighted and unweighted edges
    - Provides methods for node/edge manipulation, adjacency matrix/list, and edge list generation
    - Includes visual string representation of graph data

DisjointSet:
    - Implements Union-Find with path compression and rank heuristics
    - Useful for graph algorithms like Kruskal's MST
"""


from typing import List, Tuple

class Graph:

    def __init__(self, title="Graph", directed: bool=False, weighted: bool=False):
        # Flags
        self.directed = directed
        self.weighted = weighted

        # Fields
        self.title = title
        self.nodes = set()
        self.adj_list = {}
        self.negative_weights = 0
    
    def __str__(self):
        lines = []
        indent = "   "
        divider = ""
        divider = "=" * 90
        def header(text):
            lines.append(divider)
            lines.append(text)
            lines.append(divider)

        lines.append(divider)
        lines.append(f"\"{self.title}\"")
        lines.append("Directed, ") if self.directed else lines.append("Undirected, ")
        lines[2] = lines[2] + "Weighted" if self.weighted else lines[2] + "Unweighted"
        lines.append(divider)
        lines.append("")

        lines.append("Nodes:")
        nodes = sorted(self.nodes)
        lines.append(f"{nodes}\n")

        header("Adjacency List")
        for source_node, neighbor in sorted(self.adj_list.items()):
            lines.append(f"{indent}Node {source_node}:")
            if not neighbor:
                lines.append(f"{indent}{indent}No adjacencies")
            for dest_node, weight in sorted(self.adj_list[source_node].items()):
                lines.append(f"{indent}{indent}Node {dest_node}, Weight: {weight}")
        lines.append("")
        
        header("Adjacency Matrix")
        lines.append("")

        # Add column headers
        lines.append("-" * 6 + ("-" * 5) * (len(nodes)))
        lines.append(" " * 6 + "".join(f"{node:>5}" for node in nodes))
        lines.append("-" * 6 + ("-" * 5) * (len(nodes)))

        # Add rows with row headers and matrix values
        matrix = self.get_adj_matrix()
        for i, row in enumerate(matrix):
            lines.append(f"{indent}{nodes[i]} |" + "".join(f"{value:>5}" for value in row))
        lines.append("")

        if not self.directed:
            header("Edge List\nUndirected graph: edges are bidirectional")
        else:
            header("Edge List")
        lines.append("")
        lines.append("-" * 35)
        if self.directed:
            lines.append(f"{'Source':>10}{'Destination':>15}{'Weight':>10}")
        else:
            lines.append(f"{'Node':>10}{'Node':>15}{'Weight':>10}")
        lines.append("-" * 35)
        for edge in sorted(self.get_edge_list(), key=lambda x: (x[0], x[1], x[2])):
            source, destination, weight = edge
            lines.append(f"{source:>10}{destination:>15}{weight:>10}")

        return "\n".join(lines)
        

    # Helper functions

    def order(self) -> int:
        return len(self.nodes)
    
    def num_edges(self) -> int:
        return len(self.get_edge_list())
    
    def has_node(self, node: str) -> bool:
        node = str(node)
        return node in self.nodes

    def has_edge(self, source_node: str, dest_node: str) -> bool:
        source_node = str(source_node)
        dest_node = str(dest_node)

        if (not self.has_node(source_node)):
            raise ValueError(f"'{source_node}' not found in '{self.title}'")
        if (not self.has_node(dest_node)):
            raise ValueError(f"'{dest_node}' not found in '{self.title}'")
            
        return dest_node in self.adj_list[source_node]

    def degree(self, node: str) -> int:
        node = str(node)
        if self.has_node(node):
            return len(self.adj_list[node])
        raise ValueError(f"'{node}' not found in '{self.title}'")

    def in_degree(self, node: str) -> int:
        node = str(node)
        counter = 0
        if self.has_node(node):
            for source_node, neighbor in self.adj_list.items():
                for dest_node, weight in neighbor.items():
                    if str(dest_node) == node:
                        counter += 1
            return counter
        raise ValueError(f"'{node}' not found in '{self.title}'")

    def out_degree(self, node: str) -> int:
        return self.degree(node)

    def get_neighbors(self, node: str) -> set:
        node = str(node)
        if self.has_node(node):
            return set(self.adj_list[node].keys())
        raise ValueError(f"'{node}' not found in '{self.title}'")

    def get_weight(self, source_node: str, dest_node: str) -> int:
        source_node = str(source_node)
        dest_node = str(dest_node)

        if not self.has_edge(source_node, dest_node):
            raise ValueError(f"No edge found from {source_node} to {dest_node} in '{self.title}'")
        
        if not self.weighted:
            return 1   # Unweighted graph means all weights equal 1
        return self.adj_list[source_node][dest_node]


    # Graph construction functions

    def add_node(self, node: str) -> None:
        node = str(node)
        if not self.has_node(node):
            self.nodes.add(node)
            self.adj_list[node] = {}

    def remove_node(self, node: str) -> None:
        node = str(node)
        if self.has_node(node):
            self.nodes.remove(node)
            del self.adj_list[node]
            for neighbor in self.adj_list:
                self.adj_list[neighbor].pop(node)
        else:
            raise ValueError(f"'{node}' not found in '{self.title}'")
    
    def add_edge(self, source_node: str, dest_node: str, weight: int=1) -> None:
        source_node = str(source_node)
        dest_node = str(dest_node)

        if source_node == dest_node:
            raise ValueError("Self-loops are not allowed.")
        if (not self.has_node(source_node)):
            self.add_node(source_node)
        if (not self.has_node(dest_node)):
            self.add_node(dest_node)
        
        if not self.weighted: weight = 1

        if weight < 0: self.negative_weights += 1
        
        self.adj_list[source_node][dest_node] = weight
        if not self.directed:
            self.adj_list[dest_node][source_node] = weight

    def remove_edge(self, source_node: str, dest_node: str) -> None:
        source_node = str(source_node)
        dest_node = str(dest_node)

        if not self.has_edge(source_node, dest_node):
            raise ValueError(f"No edge found from {source_node} to {dest_node} in '{self.title}'")
        
        if self.adj_list[source_node][dest_node] < 0: self.negative_weights -= 1

        self.adj_list[source_node].pop(dest_node)
        if not self.directed:
            self.adj_list[dest_node].pop(source_node)

    def clear(self) -> None:
        self.nodes.clear()
        self.adj_list.clear()

    
    # Graph structure functions

    def get_adj_matrix(self) -> List[List[int]]:
        nodes_list = sorted(self.nodes)
        node_index = {node: i for i, node in enumerate(nodes_list)}
        adj_matrix = [[0 for _ in range(len(nodes_list))] for _ in range(len(nodes_list))]

        for source_node, neighbors in self.adj_list.items():
            for dest_node, weight in neighbors.items():
                i, j = node_index[source_node], node_index[dest_node]
                adj_matrix[i][j] = weight

        return adj_matrix

    def get_edge_list(self) -> List[Tuple[str, str, int]]:
        edge_list = []
        visited_edges = set()

        for source_node, neighbors in self.adj_list.items():
            for dest_node, weight in neighbors.items():
                if self.directed or (dest_node, source_node) not in visited_edges:
                    edge_list.append((source_node, dest_node, weight))
                    if not self.directed:
                        visited_edges.add((source_node, dest_node))

        return edge_list
    
class DisjointSet:
    def __init__(self, graph_order):
        self.parent = list(range(graph_order))
        self.rank = [0] * graph_order

    def find(self, u):
        if self.parent[u] != u:
            self.parent[u] = self.find(self.parent[u])
        return self.parent[u]
    
    def union(self, u, v):
        root_u = self.find(u)
        root_v = self.find(v)

        if root_u != root_v:
            if self.rank[root_u] > self.rank[root_v]:
                self.parent[root_v] = root_u
            elif self.rank[root_u] < self.rank[root_v]:
                self.parent[root_u] = root_v
            else:
                self.parent[root_v] = root_u
                self.rank[root_u] += 1
