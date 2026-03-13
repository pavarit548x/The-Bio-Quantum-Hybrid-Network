import time
import datetime
import sys
import os
from src.layer1_quantum import QuantumSubstrate, build_mycelium_topology
from src.layer2_sensory import SensoryStream
from src.layer3_soul import SoulSync
from src.layer4_bio import BioTranslation
from src.layer5_neural import NeuralInterface
from src.node import Node, log, GREEN, RED, CYAN, YELLOW, RESET
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

def run_simulation_scenario(scenario: str, custom_message: str = None):
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
    layer5_map = {}
    host = '127.0.0.1'
    for n_id in nodes_id:
        node = Node(n_id, host, port_mapping[n_id], topology, port_mapping)
        
        # Explicitly instantiate the 5 layers
        layer1 = QuantumSubstrate(n_id, log, node)
        layer2 = SensoryStream(n_id, log)
        layer3 = SoulSync(n_id, log)
        layer4 = BioTranslation(n_id, log)
        layer5 = NeuralInterface(n_id, log)

        # Wire the layers together using strict Separation of Concerns
        layer1.set_layers(upper=layer2)
        layer2.set_layers(upper=layer3, lower=layer1)
        layer3.set_layers(upper=layer4, lower=layer2)
        layer4.set_layers(upper=layer5, lower=layer3)
        layer5.set_layers(lower=layer4)

        # Bind hardware container to the physical quantum substrate
        node.set_layer1(layer1)
        
        layer5_map[n_id] = layer5
        active_nodes.append(node)
        
    for node in active_nodes:
        node.start()
        
    time.sleep(1.0)
    
    src_node_id = 'A'
    dst_node_id = 'D'
    message = custom_message if custom_message else "HELLO QUANTUM WORLD!"
        
    print()
    log_main("Initiating Packet Transfer Sequence...", CYAN)
    
    # Run the specific scenario
    try:
        src_layer5 = layer5_map[src_node_id]
        src_layer5.request("SEND_MESSAGE", {
            "dst": dst_node_id,
            "message": message,
            "scenario": scenario
        })
    except Exception as e:
        log_main(f"Simulation exception: {e}", RED)
    
    print()
    time.sleep(1.0)
    log_main("Shutting down Bio-Quantum Network local nodes...", CYAN)
    for node in active_nodes:
        node.stop()
        
    time.sleep(0.5)
    log_main("All local simulation nodes offline. Scenario complete.", GREEN)

def print_topology():
    print("\n" + CYAN + "="*60 + RESET)
    print(f"{CYAN}>> INITIALIZING MYCELIUM TOPOLOGY SCAN...{RESET}")
    time.sleep(0.5)
    print(f"{CYAN}>> ESTABLISHING SECURE UPLINK... OK{RESET}")
    time.sleep(0.5)
    print(CYAN + "="*60 + RESET)
    
    topology = build_mycelium_topology()
    
    ascii_topo = f"""
{GREEN}       [ NODE A ]{RESET} ====== (1) ====== {GREEN}[ NODE B ]{RESET}
           ||                           ||
          (2)                          (2)
           ||                           ||
{GREEN}       [ NODE C ]{RESET} ====== (1) ====== {GREEN}[ NODE D ]{RESET}
           \\                            /
           (3)                        (1)
             \\                        /
              ====== {GREEN}[ NODE E ]{RESET} ======
    """
    print(ascii_topo)
    
    print(f"{CYAN}--- ROUTING METRICS ---{RESET}")
    for node in topology.nodes:
        neighbors = list(topology.neighbors(node))
        print(f" [*] {GREEN}NODE {node}{RESET} {CYAN}UP{RESET} | Links: {', '.join(neighbors)}")
        time.sleep(0.1)
    
    print(CYAN + "="*60 + RESET + "\n")

def main():
    while True:
        clear_screen()
        print_header()
        print(f"{YELLOW}Select an execution sequence:{RESET}")
        print("  [1] Run Standard 5-Layer Simulation (Happy Path - Zero-Latency)")
        print("  [2] Simulate Node Failure / Decoherence (Demonstrate Slime Mold Rerouting)")
        print("  [3] Simulate Psycho-Breaker Crisis (Demonstrate HRV Spike & Force Logout)")
        print("  [4] Custom Payload Injection (Live Data Transmission)")
        print("  [5] Simulate DNA Mutation (Demonstrate Reed-Solomon ECC)")
        print("  [6] View Current Mycelium Topology")
        print("  [7] Exit Emulator\n")
        
        choice = input("Enter your choice (1-7): ").strip()
        
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
            print(f"\n{CYAN}--- CUSTOM PAYLOAD INJECTION ---{RESET}")
            custom_msg = input(f"{YELLOW}Enter your message to transmit: {RESET}").strip()
            if not custom_msg:
                custom_msg = "HELLO CUSTOM QUANTUM WORLD!"
            run_simulation_scenario("happy", custom_message=custom_msg)
            input("\nPress Enter to return to menu...")
        elif choice == '5':
            run_simulation_scenario("mutate")
            input("\nPress Enter to return to menu...")
        elif choice == '6':
            print_topology()
            input("Press Enter to return to menu...")
        elif choice == '7':
            print(f"\n{GREEN}Exiting Bio-Quantum Hybrid Network Emulator. Goodbye!{RESET}\n")
            break
        else:
            print(f"\n{RED}Invalid choice. Please enter a number between 1 and 7.{RESET}")
            time.sleep(1.5)

if __name__ == "__main__":
    main()
