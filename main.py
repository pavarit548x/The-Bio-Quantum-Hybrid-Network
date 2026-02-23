import time
import datetime
import sys
import os
from layer1_net import build_mycelium_topology, get_routing_path
from node import Node, GREEN, RED, CYAN, YELLOW, RESET
import networkx as nx

def log_main(msg, color=RESET):
    ts = datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]
    print(f"{color}[{ts}] [SYSTEM] {msg}{RESET}")
    sys.stdout.flush()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    ascii_art = r"""
  ____  _             ___                    _                 
 |  _ \(_)           / _ \                  | |                
 | |_) | | ___ ____ | | | |_   _  __ _ _ __ | |_ _   _ _ __ ___  
 |  _ <| |/ _ \____|| | | | | | |/ _` | '_ \| __| | | | '_ ` _ \ 
 | |_) | | (_) |    | |_| | |_| | (_| | | | | |_| |_| | | | | | |
 |____/|_|\___/      \__\_\\__,_|\__,_|_| |_|\__|\__,_|_| |_| |_|
 
         HYBRID NETWORK EMULATOR v1.0 - QSP 5-LAYER STACK
"""
    print(CYAN + ascii_art + RESET)

def run_simulation_scenario(scenario: str):
    print("\n" + "="*60)
    log_main(f"INITIALIZING SCENARIO: {scenario.upper()}", CYAN)
    print("="*60 + "\n")
    
    topology = build_mycelium_topology()
    nodes_id = list(topology.nodes)
    
    port_mapping = {}
    base_port = 5001
    for i, n_id in enumerate(nodes_id):
        port_mapping[n_id] = base_port + i
        
    active_nodes = []
    host = '127.0.0.1'
    for n_id in nodes_id:
        node = Node(n_id, host, port_mapping[n_id], topology, port_mapping)
        active_nodes.append(node)
        
    for node in active_nodes:
        node.start()
        
    time.sleep(1.0)
    
    src_node_id = 'A'
    dst_node_id = 'D'
    message = "HELLO QUANTUM WORLD!"
    
    src_node_obj = next(n for n in active_nodes if n.node_id == src_node_id)
    
    print()
    log_main("Initiating Packet Transfer Sequence...", CYAN)
    
    # Run the specific scenario
    src_node_obj.send_initial_message(dst_node_id, message, scenario=scenario)
    
    print()
    time.sleep(1.0)
    log_main("Shutting down Bio-Quantum Network local nodes...", CYAN)
    for node in active_nodes:
        node.stop()
        
    time.sleep(0.5)
    log_main("All local simulation nodes offline. Scenario complete.", GREEN)

def print_topology():
    print("\n" + "="*60)
    log_main("CURRENT MYCELIUM TOPOLOGY:", CYAN)
    topology = build_mycelium_topology()
    for node in topology.nodes:
        neighbors = list(topology.neighbors(node))
        log_main(f"Node {node} is connected to: {neighbors}", GREEN)
    print("="*60 + "\n")

def main():
    while True:
        clear_screen()
        print_header()
        print(f"{YELLOW}Select an execution sequence:{RESET}")
        print("  [1] Run Standard 5-Layer Simulation (Happy Path - Zero-Latency)")
        print("  [2] Simulate Node Failure / Decoherence (Demonstrate Slime Mold Rerouting)")
        print("  [3] Simulate Psycho-Breaker Crisis (Demonstrate HRV Spike & Force Logout)")
        print("  [4] View Current Mycelium Topology")
        print("  [5] Exit Emulator\n")
        
        choice = input("Enter your choice (1-5): ").strip()
        
        if choice == '1':
            run_simulation_scenario("happy")
            input("\nPress Enter to return to menu...")
        elif choice == '2':
            run_simulation_scenario("reroute")
            input("\nPress Enter to return to menu...")
        elif choice == '3':
            run_simulation_scenario("crisis")
            input("\nPress Enter to return to menu...")
        elif choice == '4':
            print_topology()
            input("Press Enter to return to menu...")
        elif choice == '5':
            print(f"\n{GREEN}Exiting Bio-Quantum Hybrid Network Emulator. Goodbye!{RESET}\n")
            break
        else:
            print(f"\n{RED}Invalid choice. Please enter a number between 1 and 5.{RESET}")
            time.sleep(1.5)

if __name__ == "__main__":
    main()
