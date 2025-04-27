"""
traversals.py

Provides Breadth-First Search (BFS) and Depth-First Search (DFS) algorithms for traversing graphs.

Includes:
- Full traversal orders from a starting node
- Boolean search (i.e., "does a path exist to target?")
- Optional callback functions for node visitation side effects

Functions:
- bfs_order(graph, start, bfs_action=None)
- bfs_contains(graph, start, target)
- dfs_order(graph, start, dfs_action=None)
- dfs_contains(graph, start, target)
"""



from graphlib.core import Graph
from typing import List
from collections import deque

def bfs_order(graph: Graph, start: str, bfs_action: str=None) -> List[str]:
    if not graph.has_node(start):
        raise ValueError(f"'{start}' not found in '{graph.title}'")
    
    visited_nodes = {start}
    queue = deque([start])
    traversal = []

    while queue:
        current = queue[0]
        traversal.append(current)

        if bfs_action:
            bfs_action(current)

        for neighbor in graph.get_neighbors(current):
            if neighbor not in visited_nodes:
                visited_nodes.add(neighbor)
                queue.append(neighbor)
        
        queue.popleft()

    return traversal

def bfs_contains(graph: Graph, start: str, target: str) -> bool:
    found = False

    def bfs_action(node: str):
        nonlocal found
        if node == target:
            found = True
            return

    bfs_order(graph, start, bfs_action)
    return found


def dfs_order(graph: Graph, start: str, dfs_action: str=None) -> List[str]:
    if not graph.has_node(start):
        raise ValueError(f"'{start}' not found in '{graph.title}'")
    
    visited_nodes = {start}
    stack = [start]
    traversal = []

    while stack:
        current  = stack[-1]
        if current not in traversal:
            traversal.append(current)
            if dfs_action:
                dfs_action(current)
        stack.pop()

        for neighbor in graph.get_neighbors(current):
            if neighbor not in visited_nodes:
                visited_nodes.add(neighbor)
                stack.append(neighbor)

    return traversal

def dfs_contains(graph: Graph, start: str, target: str) -> bool:
    found = False
    
    def dfs_action(current):
        nonlocal found
        if current == target:
            found = True
            return

    dfs_order(graph, start, dfs_action)
    return found