"""
visuals.py

Visualizes Graph objects using Matplotlib.

- Computes node positions in circular layout
- Draws nodes, edges (with direction and weights), and annotations
- Supports both directed and undirected graphs

Functions:
- calculate_positions(nodes)
- draw_graph(graph)
"""



import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

from graphlib.core import Graph

NODE_RADIUS = 0.1
DEF_EDGE_COLOR = '#353535'

def calculate_positions(nodes):
    n = len(nodes)
    angles = np.linspace(np.pi, 3 * np.pi, n, endpoint=False)
    return {node: (np.cos(angle), np.sin(angle)) for node, angle in zip(nodes, angles)}

def draw_graph(graph: Graph):
    fig, ax = plt.subplots()
    ax.set_aspect('equal')
    
    # Calculate node positions
    positions = calculate_positions(sorted(graph.nodes))
    
    # Draw edges
    for u, v, weight in graph.get_edge_list():
        x1, y1 = positions[u]
        x2, y2 = positions[v]

        # Calculate unit vector
        distance = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        ux = (x2 - x1) / distance
        uy = (y2 - y1) / distance
        
        # Adjust the start and end points
        x1 += NODE_RADIUS * ux
        y1 += NODE_RADIUS * uy
        x2 -= NODE_RADIUS * ux
        y2 -= NODE_RADIUS * uy

        # Draw lines between nodes (edges)
        if graph.directed:
            ax.arrow(x1, y1, x2 - x1, y2 - y1,
                     head_width=0.03, length_includes_head=True, color=DEF_EDGE_COLOR)
        else:
            ax.plot([x1, x2], [y1, y2], color=DEF_EDGE_COLOR)

        # Add edge weights
        if graph.weighted:
            ax.text((x1 + x2) / 2, (y1 + y2) / 2, str(weight), color='black', weight='bold')
    
    # Draw nodes
    for node, (x, y) in positions.items():
        ax.add_patch(patches.Circle((x, y), NODE_RADIUS, color='black', ec='black'))
        ax.text(x, y, str(node), color='white', ha='center', va='center', weight='bold')
    
    plt.axis('off')
    plt.show()