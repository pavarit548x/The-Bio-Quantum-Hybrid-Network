import time
from layer1_net import build_mycelium_topology, get_routing_path
from node import Node

def main():
    print("==================================================")
    print("   BIO-QUANTUM HYBRID NETWORK EMULATOR STARTED    ")
    print("==================================================\n")
    
    # 1. Layer 1: Build the Mycelium Topology Mesh
    print("--> Initializing Layer 1: Mycelium Topology...")
    topology = build_mycelium_topology()
    nodes_id = list(topology.nodes)
    
    # Let's see the paths from 'A' to 'D'
    sample_path = get_routing_path(topology, 'A', 'D')
    print(f"--> Mycelium Mesh Created. Nodes: {nodes_id}")
    print(f"--> Computed Route Example (Slime Mold A->D): {sample_path}\n")
    
    # 2. Assign Network Ports Configuration
    port_mapping = {}
    base_port = 5001
    for i, n_id in enumerate(nodes_id):
        port_mapping[n_id] = base_port + i
        
    print("--> Network Port Configuration:")
    for n_id, port in port_mapping.items():
        print(f"    Node {n_id} -> localhost:{port}")
    print("")
    
    # 3. Compute routing tables for all nodes
    routing_tables = {}
    for src in nodes_id:
        routing_tables[src] = {}
        for dst in nodes_id:
            if src != dst:
                 # Dijkstra logic routing
                 routing_tables[src][dst] = get_routing_path(topology, src, dst)
                 
    # 4. Spin up the Node listeners
    print("--> Spinning up Node socket listeners...")
    active_nodes = []
    host = '127.0.0.1'
    for n_id in nodes_id:
        rt = routing_tables[n_id]
        # Pass the map and routing config to allow nodes to perform mesh hops
        node = Node(n_id, host, port_mapping[n_id], rt, port_mapping)
        active_nodes.append(node)
        
    for node in active_nodes:
        node.start()
        
    # Give the threads a short moment to establish sockets
    time.sleep(1.0)
    
    # 5. Initiate Packet Transfer Request
    src_node_id = 'A'
    dst_node_id = 'D'
    message = "HELLO QUANTUM WORLD!"
    
    src_node_obj = next(n for n in active_nodes if n.node_id == src_node_id)
    
    print("\n--> Initiating Packet Transfer Sequence...")
    src_node_obj.send_initial_message(dst_node_id, message)
    
    # Wait to allow the message to propagate across the network threads
    time.sleep(3.0)
    
    # 6. Clean Shutdown
    print("\n--> Shutting down Bio-Quantum Network...")
    for node in active_nodes:
        node.stop()
        
    print("--> All nodes offline. Simulation complete.")

if __name__ == "__main__":
    main()
