import socket
import threading
import json
import time
import datetime
import networkx as nx
from layer4_bio import encode_message_to_dna, decode_dna_to_message
from layer3_soul import verify_soul_id, check_psycho_breaker
from layer1_net import get_routing_path

GREEN = "\033[92m"
RED = "\033[91m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
RESET = "\033[0m"

def log(node_id, msg, color=RESET):
    ts = datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]
    print(f"{color}[{ts}] [Node {node_id}] {msg}{RESET}")

class Node:
    """
    Represents a network device in the Bio-Quantum network.
    Communicates using local Python Sockets via TCP with realistic routing mechanisms.
    """
    def __init__(self, node_id: str, host: str, port: int, topology: nx.Graph, port_mapping: dict):
        self.node_id = node_id
        self.host = host
        self.port = port
        self.topology = topology.copy()  # Each node maintains its own world-view
        self.port_mapping = port_mapping
        
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        
        self.running = False
        self.thread = threading.Thread(target=self.listen, daemon=True)

    def start(self):
        self.running = True
        self.thread.start()
        log(self.node_id, f"Booted and listening on {self.host}:{self.port}...", CYAN)

    def stop(self):
        self.running = False
        try:
            # Send a dummy connection to unblock accept()
            dummy = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            dummy.connect((self.host, self.port))
            dummy.close()
        except:
            pass
        self.server_socket.close()

    def listen(self):
        """Background thread loop to accept incoming connections."""
        while self.running:
            try:
                conn, addr = self.server_socket.accept()
                if not self.running:
                    break
                threading.Thread(target=self.handle_client, args=(conn,), daemon=True).start()
            except BaseException:
                break

    def handle_client(self, conn: socket.socket):
        """Handles an incoming packet over the wire."""
        try:
            data = conn.recv(4096).decode('utf-8')
            if not data:
                return
            
            packet = json.loads(data)
            
            if packet.get('action') == 'stop':
                return
                
            success = self.process_packet(packet)
            
            # Send ACK or NACK back to the sender
            if success:
                conn.sendall(b'ACK')
            else:
                conn.sendall(b'NACK')
        except json.JSONDecodeError:
            pass
        except Exception as e:
            log(self.node_id, f"Error handling packet: {e}", RED)
        finally:
            conn.close()

    def process_packet(self, packet: dict) -> bool:
        """Processes the Layer 3 checks, routing, and Layer 4 decoding. Returns success status."""
        src = packet['src']
        dst = packet['dst']
        dna_payload = packet['payload']
        user_id = packet.get('user_id', 'quantum_user_1X')
        
        # Simulated Network Transfer Time
        time.sleep(0.3)
        
        log(self.node_id, f"Packet Arrived | ETH_HEADER: [SRC: {src} -> DST: {dst}] | TYPE: QSP_DNA", CYAN)
        log(self.node_id, f"Raw Payload: {dna_payload[:30]}...", CYAN)
        
        # --- Layer 3: Soul Sync Verify ---
        if not verify_soul_id(user_id, "ACTG_VALID", "EEG_WAVES_VALID"):
            log(self.node_id, "Layer 3 Failed: Invalid Soul ID. Dropping packet.", RED)
            return False

        # --- Layer 3: Psycho-Breaker ---
        is_safe, reason = check_psycho_breaker()
        if not is_safe:
            log(self.node_id, f"EMERGENCY LOGOUT! {reason}. Connection cut via Psycho-Breaker.", RED)
            return False
            
        log(self.node_id, f"Layer 3 Checks Passed: {reason}", GREEN)

        # Check if this node is the final destination
        if self.node_id == dst:
            log(self.node_id, "🎯 Packet reached final destination! Initiating Bio-Translation...", GREEN)
            
            # Simulated Decoding Time
            time.sleep(0.6)
            
            # --- Layer 4: Decoding ---
            original_msg = decode_dna_to_message(dna_payload)
            log(self.node_id, f"🧬 Layer 4 Bio-Translation (Decoded): '{original_msg}'", GREEN)
            log(self.node_id, f"SUCCESS: Transmission Delivery Confirmed.", GREEN)
            return True
        else:
            # Routing: We must forward it
            log(self.node_id, f"Not the destination. Computing Slime Mold path to '{dst}'...", CYAN)
            return self.route_and_forward(dst, packet)

    def route_and_forward(self, dst: str, packet: dict) -> bool:
        """Finds a path, attempts to forward, and dynamically re-routes if the next hop fails."""
        while True:
            # Calculate shortest path based on current local view of topology
            path = get_routing_path(self.topology, self.node_id, dst)
            if not path or len(path) < 2:
                log(self.node_id, f"Routing Error: No valid path to {dst}.", RED)
                return False
                
            next_hop = path[1] # index 0 is self
            log(self.node_id, f"➡️ Next hop computed: Node {next_hop}. Forwarding...", CYAN)
            
            # Processing Time & Hopping
            time.sleep(0.4) 
            target_port = self.port_mapping[next_hop]
            success = self.forward_packet(next_hop, target_port, packet)
            
            if success:
                # Upstream node accepted and successfully handled/routed the packet
                return True
            else:
                # Upstream node failed (Psycho-breaker triggered, or node dead)
                log(self.node_id, f"Connection to {next_hop} refused or timed out. Triggering Slime Mold Re-routing...", YELLOW)
                # Temporarily remove the dead/rejected node from local topology
                if self.topology.has_node(next_hop):
                    self.topology.remove_node(next_hop)
                
                # Sleep briefly before finding a new path
                time.sleep(0.2)

    def forward_packet(self, next_hop: str, target_port: int, packet: dict) -> bool:
        """Sends a JSON packet over TCP socket to the next hop and waits for an ACK/NACK."""
        try:
             s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
             s.settimeout(2.0)
             s.connect((self.host, target_port))
             s.sendall(json.dumps(packet).encode('utf-8'))
             response = s.recv(1024).decode('utf-8')
             s.close()
             if response == 'ACK':
                 return True
             else:
                 return False
        except Exception:
             # Assume node failure (timeout or connection refused)
             return False

    def send_initial_message(self, dst: str, message: str):
        """Initiates a message transfer from this node to a destination node."""
        log(self.node_id, "==================================================", CYAN)
        log(self.node_id, f"Initiating Transfer | Target: Node {dst}", CYAN)
        log(self.node_id, f"🗨️ Original Message: '{message}'", CYAN)
        
        # Simulate initial encoding delay
        time.sleep(0.5)
        
        # --- Layer 4: Encoding ---
        dna_payload = encode_message_to_dna(message)
        log(self.node_id, f"🧬 Layer 4 Bio-Translation (Encoded DNA): {dna_payload[:50]}...", CYAN)
        
        packet = {
            'src': self.node_id,
            'dst': dst,
            'payload': dna_payload,
            'user_id': 'quantum_user_1X'
        }
        
        success = self.route_and_forward(dst, packet)
        
        if success:
            log(self.node_id, "==================================================", GREEN)
            log(self.node_id, "Transmission completed successfully.", GREEN)
        else:
            log(self.node_id, "==================================================", RED)
            log(self.node_id, "Transmission completely FAILED. No routes available.", RED)
