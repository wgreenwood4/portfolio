"""
algorithms.py

Contains functions to generate classic graphs such as:
- Complete graphs (K_n)
- Complete bipartite graphs (K_{n,m})
- Cycle graphs (C_n)

All graph constructors return instances of the Graph class.
"""


from graphlib.core import Graph

def k_graph(n: int) -> Graph:
    if n < 1:
        raise ValueError("A complete graph is not defined for 'n' less than 1")
    
    k = Graph(f"K_{n}", directed=False, weighted=False)
    
    for i in range(n):
        k.add_node(i)

    if n == 1: return k
    
    for source_node in k.nodes:
        for dest_node in k.nodes:
            if not k.has_edge(source_node, dest_node) and source_node != dest_node:
                k.add_edge(source_node, dest_node)
    
    return k

def k_bipartite_graph(n: int, m: int) -> Graph:
    if n < 0 or m < 0:
        raise ValueError("A complete bipartite graph is not defined for 'n', 'm' less than 0")

    k_bipartite = Graph(f"K_{n},{m}", directed=False, weighted=False)

    set_U = set()
    set_V = set()

    for u_node in range(0, n):
        k_bipartite.add_node(u_node)
        set_U.add(u_node)
    for v_node in range(n, n + m):
        k_bipartite.add_node(v_node)
        set_V.add(v_node)

    for u in set_U:
        for v in set_V:
            k_bipartite.add_edge(u, v)
    
    return k_bipartite

def c_graph(n: int) -> Graph:
    if n < 1:
        raise ValueError("A cycle graph is not defined for 'n' less than 1")
    
    c = Graph(f"C_{n}", directed=False, weighted=False)

    c.add_node(0)

    if n == 1: return c

    for i in range(1, n):
        c.add_node(i)
        c.add_edge(i - 1, i)
    c.add_edge(0, n - 1)

    return c
