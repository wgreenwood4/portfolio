"""
pathfinding.py

Implements classical shortest path algorithms:

- Dijkstra's Algorithm: Computes shortest paths from a source in graphs with non-negative weights.
- Bellman-Ford Algorithm: Handles graphs with negative weights, detects negative cycles.
- Floyd-Warshall Algorithm: All-pairs shortest paths via dynamic programming.

Returns shortest path trees and/or distance matrices. Raises errors for invalid inputs or negative cycles.

Functions:
- dijkstra(graph, source_node)
- bellman_ford(graph, source_node)
- floyd_warshall(graph)
"""



import heapq
from typing import Tuple, List
from graphlib.core import Graph

def dijkstra(graph: Graph, source_node: str) -> Tuple[Graph, dict]:
    if graph.negative_weights > 0:
        raise ValueError("Dijkstra's Algorithm may only be applied to non-negative edge weights")

    if not graph.has_node(source_node):
        raise ValueError(f"'{source_node}' not found in '{graph.title}'")
    
    # Dijkstra's Algorithm
    distances = {node: float('inf') for node in graph.nodes}
    distances[source_node] = 0
    min_heap = [(0, source_node)]
    parent = {}

    while min_heap:
        distance, current_node = heapq.heappop(min_heap)

        for neighbor in graph.adj_list[current_node]:
            tenative_distance = distances[current_node] + graph.adj_list[current_node][neighbor]
            if tenative_distance < distances[neighbor]:
                distances[neighbor] = tenative_distance
                parent[neighbor] = current_node
                heapq.heappush(min_heap, (tenative_distance, neighbor))
    
    # Construct shortest path tree (spt)
    spt = Graph(f"{graph.title}_(dijkstra_spt)", directed=graph.directed, weighted=graph.weighted)
    for node, neighbor in parent.items():
        spt.add_node(node)
        spt.add_node(neighbor)
        spt.add_edge(neighbor, node, graph.adj_list[neighbor][node])

    return spt, distances

def bellman_ford(graph: Graph, source_node: str) -> Tuple[Graph, dict]:
    if not graph.has_node(source_node):
        raise ValueError(f"'{source_node}' not found in '{graph.title}'")

    # Bellman–Ford Algorithm
    distances = {node: float('inf') for node in graph.nodes}
    distances[source_node] = 0
    parent = {}
    
    for i in range(graph.order()):
        for u, v, weight in graph.get_edge_list():
            if distances[u] != float('inf') and distances[u] + weight < distances[v]:
                if i == graph.order() - 1:  # On the V-th iteration
                    raise ValueError("Negative cycle detected")
                distances[v] = distances[u] + weight
                parent[v] = u
    
    # Construct shortest path tree (SPT)
    spt = Graph(f"{graph.title}_(bf_spt)", directed=graph.directed, weighted=graph.weighted)
    for node, neighbor in parent.items():
        spt.add_node(node)
        spt.add_node(neighbor)
        spt.add_edge(neighbor, node, graph.adj_list[neighbor][node])

    return spt, distances

def floyd_warshall(graph: Graph) -> List[List[int]]:
    # Check for trivial graphs
    if graph.order() == 1:
        return [[0]]
    elif graph.order() == 0:
        return [[]]

    n = graph.order()
    adj_matrix = graph.get_adj_matrix()
    distances = []
    for i in range(n):
        row = []
        for j in range(n):
            if i == j:
                row.append(0)
            elif adj_matrix[i][j] == 0:
                row.append(float('inf'))
            else:
                row.append(adj_matrix[i][j])
        distances.append(row)
    
    for k in range(n):
        for i in range(n):
            for j in range(n):
                distances[i][j] = min(distances[i][j], distances[i][k] + distances[k][j])
        
        if distances[k][k] < 0:
            raise ValueError("Negative cycle detected")

    return distances
