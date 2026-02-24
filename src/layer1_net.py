# layer1_net.py
import networkx as nx

# Layer 1: Infrastructure (Mycelium & Quantum)

def build_mycelium_topology() -> nx.Graph:
    """
    Creates a mesh topology of 5 Nodes representing the Mycelium network.
    Nodes: A, B, C, D, E
    """
    G = nx.Graph()
    # Add nodes
    nodes = ['A', 'B', 'C', 'D', 'E']
    G.add_nodes_from(nodes)
    
    # Add edges to form a mesh (Mycelium-like interconnectedness)
    # A is connected to B and C
    # B is connected to A, C, D
    # C is connected to A, B, E
    # D is connected to B, E
    # E is connected to C, D
    edges = [
        ('A', 'B', 1),
        ('A', 'C', 2),
        ('B', 'C', 1),
        ('B', 'D', 2),
        ('C', 'E', 3),
        ('D', 'E', 1)
    ]
    
    for u, v, w in edges:
        G.add_edge(u, v, weight=w)
        
    return G

def get_routing_path(graph: nx.Graph, source: str, target: str) -> list[str]:
    """
    Implements a routing function (Slime Mold logic / Dijkstra)
    so a sender node knows which port/node to forward the data to.
    """
    try:
        # Using Dijkstra's algorithm for shortest path based on weight
        path = nx.shortest_path(graph, source=source, target=target, weight='weight')
        return path
    except nx.NetworkXNoPath:
        return []
