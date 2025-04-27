"""
mst.py

Implements Minimum Spanning Tree (MST) algorithms for undirected, connected graphs:

- Kruskal's Algorithm: Greedy approach using Disjoint Set (Union-Find) to build MST by edge weight.
- Prim's Algorithm: Greedy approach expanding MST from an initial node using a priority queue.

Raises exceptions for invalid graph types (e.g., directed or disconnected).

Functions:
- kruskal(graph, verbose=False)
- prim(graph, verbose=False)
"""



import heapq
from graphlib.core import Graph, DisjointSet
from graphlib.extras import analysis

def kruskal(graph: Graph, verbose: bool=False) -> Graph:

    # Check for trivial graphs
    if graph.order() <= 1:
        return graph
    
    # Check for incompatible graphs
    if graph.directed:
        raise ValueError("Kruskal's Algorithm may only be applied to undirected graphs")
    if len(analysis.get_components(graph)) != 1:
        raise ValueError("Kruskal's Algorithm may only be applied to connected graphs")
    
    # New minimum spanning tree setup
    mst = Graph(graph.title + "_(mst)", directed=False, weighted=graph.weighted)
    for node in graph.nodes:
        mst.add_node(node)
    if graph.weighted:
        edge_pool = sorted(graph.get_edge_list(), key=lambda x: x[2])
    else:
        edge_pool = graph.get_edge_list()

    # Kruskal's Algorithm using DisjointSet structure
    node_to_index = {node: i for i, node in enumerate(graph.nodes)}
    ds = DisjointSet(graph.order())
    for u, v, weight in edge_pool:
        if ds.find(node_to_index[u]) != ds.find(node_to_index[v]):
            ds.union(node_to_index[u], node_to_index[v])
            mst.add_edge(u, v, weight)
            if verbose: print(f"Adding edge: ({u}, {v}, {weight})")

    return mst

def prim(graph: Graph, verbose: bool=False) -> Graph:

    # Check for trivial graphs
    if graph.order() <= 1:
        return graph

    # Check for incompatible graphs
    if graph.directed:
        raise ValueError("Prim's Algorithm may only be applied to undirected graphs")
    if len(analysis.get_components(graph)) != 1:
        raise ValueError("Prim's Algorithm may only be applied to connected graphs")
    
    # New minimum spanning tree setup
    mst = Graph(graph.title + "_(mst)", directed=False, weighted=graph.weighted)
    for node in graph.nodes:
        mst.add_node(node)
    
    # Prim's Algorithm
    nodes_list = list(graph.nodes)
    start_node = nodes_list[0]
    edge_pool = []
    visited_nodes = {start_node}

    for neighbor, weight in graph.adj_list[start_node].items():
        heapq.heappush(edge_pool, (weight, start_node, neighbor))
    
    while edge_pool:
        weight, source_node, dest_node = heapq.heappop(edge_pool)

        if dest_node not in visited_nodes:
            mst.add_edge(source_node, dest_node, weight)
            if verbose: print(f"Adding edge: ({source_node}, {dest_node}, {weight})")
            visited_nodes.add(dest_node)

            for neighbor, weight in graph.adj_list[dest_node].items():
                if neighbor not in visited_nodes:
                    heapq.heappush(edge_pool, (weight, dest_node, neighbor))
    
    return mst
        