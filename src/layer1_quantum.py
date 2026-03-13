import networkx as nx
import time

def build_mycelium_topology() -> nx.Graph:
    """Creates a mesh topology of 5 Nodes representing the Mycelium network."""
    G = nx.Graph()
    nodes = ['A', 'B', 'C', 'D', 'E']
    G.add_nodes_from(nodes)
    edges = [
        ('A', 'B', 1), ('A', 'C', 2),
        ('B', 'C', 1), ('B', 'D', 2),
        ('C', 'E', 3), ('D', 'E', 1)
    ]
    for u, v, w in edges:
        G.add_edge(u, v, weight=w)
    return G

def get_routing_path(graph: nx.Graph, source: str, target: str) -> list[str]:
    try:
        return nx.shortest_path(graph, source=source, target=target, weight='weight')
    except nx.NetworkXNoPath:
        return []

class QuantumSubstrate:
    """Layer 1: Physical Quantum and Mycelium Infrastructure Routing."""
    def __init__(self, node_id, log_cb, hardware_node):
        self.node_id = node_id
        self.log = log_cb
        self.upper_layer = None
        self.hardware = hardware_node
        self.topology = hardware_node.topology
        self.port_mapping = hardware_node.port_mapping
        
    def set_layers(self, upper):
        self.upper_layer = upper

    def request(self, service: str, parameters: dict):
        if service == "ROUTE_AND_SEND":
            dst = parameters.get("dst")
            packet = {
                'src': self.node_id,
                'dst': dst,
                'payload': parameters.get("dna_payload"),
                'user_id': 'quantum_user_1X',
                'attempt': parameters.get("attempt", 1),
                'scenario': parameters.get("scenario", "normal"),
                'dead_nodes': parameters.get("dead_nodes", [])
            }
            success = self._route_and_forward(dst, packet)
            if success:
                return True
            else:
                return False

    def indicate(self, event: str, data: dict):
        if event == "PACKET_RX":
            packet = data
            src = packet['src']
            dst = packet['dst']
            dna_payload = packet['payload']
            scenario = packet.get('scenario', 'normal')
            dead_nodes = packet.get('dead_nodes', [])
            
            time.sleep(0.3)
            self.log(self.node_id, f"📦 [Layer 1] Packet Arrived | ETH_HEADER: [SRC: {src} -> DST: {dst}]", "\033[96m")
            
            # Simulated Hardware Failure (Decoherence)
            if self.node_id in dead_nodes:
                self.log(self.node_id, "👻 [ZOMBIE NODE DETECTED] Ignoring packet. This node is supposed to be dead!", "\033[91m")
                return False

            if scenario == 'reroute' and self.node_id == 'B' and 'B' not in dead_nodes:
                self.log(self.node_id, "💥 [Layer 1] DECOHERENCE DETECTED: Node B hardware failure/unreachable.", "\033[91m")
                return False
                
            if self.node_id == dst:
                self.log(self.node_id, "🎯 Packet reached final destination! Forwarding up the stack...", "\033[92m")
                return self.upper_layer.indicate("PACKET_RX", {"dna_payload": dna_payload, "scenario": scenario})
            else:
                self.log(self.node_id, f"Not the destination. Computing Slime Mold path to '{dst}'...", "\033[96m")
                # Intermediary check
                is_safe = self.upper_layer.indicate("INTERMEDIATE_NODE_CHECK", {"scenario": scenario})
                if not is_safe:
                    return False
                return self._route_and_forward(dst, packet)

    def _route_and_forward(self, dst: str, packet: dict) -> bool:
        while True:
            dead_nodes = packet.get('dead_nodes', [])
            for dn in dead_nodes:
                if self.topology.has_node(dn):
                    self.topology.remove_node(dn)

            path = get_routing_path(self.topology, self.node_id, dst)
            if not path or len(path) < 2:
                self.log(self.node_id, f"Routing Error: No valid path to {dst}.", "\033[91m")
                return False
                
            next_hop = path[1]
            self.log(self.node_id, f"➡️ Next hop computed: Node {next_hop}. Forwarding...", "\033[96m")
            
            # Apply QoS from Layer 2
            self.upper_layer.indicate("APPLY_QOS", {})
            
            target_port = self.port_mapping[next_hop]
            success = self.hardware.forward_packet(next_hop, target_port, packet)
            
            if success:
                return True
            else:
                if packet.get('scenario') == 'crisis':
                    return False
                self.log(self.node_id, f"Connection to {next_hop} refused or timed out. Triggering Slime Mold Re-routing...", "\033[93m")
                if self.topology.has_node(next_hop):
                    self.topology.remove_node(next_hop)
                if next_hop not in dead_nodes:
                    dead_nodes.append(next_hop)
                packet['dead_nodes'] = dead_nodes
                packet['attempt'] = packet.get('attempt', 1) + 1
                time.sleep(0.2)
