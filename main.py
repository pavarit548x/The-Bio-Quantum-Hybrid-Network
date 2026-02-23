import time
import datetime
import sys
from layer1_net import build_mycelium_topology, get_routing_path
from node import Node, GREEN, RED, CYAN, YELLOW, RESET

def log_main(msg, color=RESET):
    ts = datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]
    print(f"{color}[{ts}] [SYSTEM] {msg}{RESET}")
    sys.stdout.flush()

def main():
    log_main("==================================================", CYAN)
    log_main("   BIO-QUANTUM HYBRID NETWORK EMULATOR STARTED    ", CYAN)
    log_main("==================================================", CYAN)
    
    time.sleep(0.5)
    log_main("Initializing Layer 1: Mycelium Topology...", CYAN)
    topology = build_mycelium_topology()
    nodes_id = list(topology.nodes)
    
    time.sleep(0.5)
    log_main(f"Mycelium Mesh Created. Nodes: {nodes_id}", GREEN)
    
    port_mapping = {}
    base_port = 5001
    for i, n_id in enumerate(nodes_id):
        port_mapping[n_id] = base_port + i
        
    time.sleep(0.5)
    log_main("Network Port Configuration mapped.", CYAN)
    for n_id, port in port_mapping.items():
        log_main(f"    Node {n_id} -> localhost:{port}", CYAN)
    
    time.sleep(0.5)
    log_main("Spinning up Node socket listeners [Slime Mold Pathfinding Enabled]...", CYAN)
    active_nodes = []
    host = '127.0.0.1'
    for n_id in nodes_id:
        # Pass a copy of the networkx topology down to each Node
        node = Node(n_id, host, port_mapping[n_id], topology, port_mapping)
        active_nodes.append(node)
        
    for node in active_nodes:
        node.start()
        time.sleep(0.1) # Stagger boot up
        
    # Give the threads a short moment to establish sockets
    time.sleep(1.0)
    
    # 5. Initiate Packet Transfer Request
    src_node_id = 'A'
    dst_node_id = 'D'
    message = "HELLO QUANTUM WORLD!"
    
    src_node_obj = next(n for n in active_nodes if n.node_id == src_node_id)
    
    print()
    log_main("Initiating Packet Transfer Sequence...", CYAN)
    
    # This call now handles the entire synchronous, blockingly-forwarded chain of Slime Mold
    # routing across threads. It returns once the packet is delivered or failed fully.
    src_node_obj.send_initial_message(dst_node_id, message)
    
    print()
    time.sleep(1.0)
    log_main("Shutting down Bio-Quantum Network...", CYAN)
    for node in active_nodes:
        node.stop()
        
    time.sleep(0.5)
    log_main("All nodes offline. Simulation complete.", GREEN)

if __name__ == "__main__":
    main()
