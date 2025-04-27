"""
utils.py

Provides utility functions for interacting with graph objects.

Includes:
- Writing graph summary (adjacency list, matrix, and edge list) to a formatted text file
"""


from graphlib.core import Graph

def graph_info_file(graph: Graph, file_name: str=None) -> None:
    if file_name == None:
        file_name = graph.title
    file_name = file_name.replace(" ", "_")  + ".txt"

    with open(file_name, 'w') as fd:
        fd.write(str(graph))