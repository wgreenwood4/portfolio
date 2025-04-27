"""
analysis.py

Graph-theoretic tools for analyzing Graph objects.

Includes:
- Connected component detection
- Cycle detection using DFS
- Eulerian circuit checks and retrieval
"""



from graphlib.core import Graph
from graphlib.extras import traversals as trv
from typing import List

def get_components(graph: Graph, sorted: bool=False) -> List[List[str]]:
    components = []
    remaining_nodes = graph.nodes

    while remaining_nodes:
        current_component = trv.dfs_order(graph, next(iter(remaining_nodes)))
        if sorted: current_component.sort()
        components.append(current_component)
        remaining_nodes = remaining_nodes - set(current_component)

    if sorted: components.sort(key=len, reverse=True)
    return components

def has_cycles(graph: Graph) -> bool:
    def dfs_cycle(node, parent, stack, visited_nodes):
        visited_nodes.add(node)
        stack.add(node)

        for neighbor in graph.get_neighbors(node):
            if neighbor not in visited_nodes:
                if dfs_cycle(neighbor, node, stack, visited_nodes):
                    return True
            elif neighbor in stack and neighbor != parent:
                return True

        stack.remove(node)
        return False

    visited_nodes = set()

    for node in graph.nodes:
        if node not in visited_nodes:
            if dfs_cycle(node, None, set(), visited_nodes):
                return True

    return False

def is_eulerian(graph: Graph) -> bool:
    if graph.directed:
        for node in graph.nodes:
            if graph.in_degree(node) != graph.out_degree(node):
                return False
        return True
    else:
        for node in graph.nodes:
            degree = graph.degree(node)
            if degree % 2 != 0:
                return False
        return True

def get_eulerian_circuit(graph: Graph) -> Graph:
    if not is_eulerian(graph):
        return None
    
