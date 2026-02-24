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
            self.server_socket.close()
        except:
            pass

    def listen(self):
        """Background thread loop to accept incoming connections."""
        self.server_socket.settimeout(1.0)
        while self.running:
            try:
                conn, addr = self.server_socket.accept()
                if not self.running:
                    break
                conn.settimeout(None)
                threading.Thread(target=self.handle_client, args=(conn,), daemon=True).start()
            except socket.timeout:
                continue
            except BaseException:
                break

    def _recvall(self, conn: socket.socket, n: int) -> bytearray:
        """Helper to read exactly n bytes from a socket."""
        data = bytearray()
        while len(data) < n:
            packet = conn.recv(n - len(data))
            if not packet:
                return None
            data.extend(packet)
        return data

    def handle_client(self, conn: socket.socket):
        """Handles an incoming packet over the wire."""
        try:
            # Read the 4-byte length prefix
            raw_msglen = self._recvall(conn, 4)
            if not raw_msglen:
                return
            msglen = int.from_bytes(raw_msglen, 'big')
            
            # Read the actual JSON data
            data_bytes = self._recvall(conn, msglen)
            if not data_bytes:
                return
            
            data = data_bytes.decode('utf-8')
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

    def _process_layer3_security(self, force_fail: bool, force_safe: bool) -> bool:
        """Handles Layer 3 Psycho-Breaker security and physiological checks."""
        is_safe, reason = check_psycho_breaker(force_fail=force_fail, force_safe=force_safe)
        if not is_safe:
            log(self.node_id, f"EMERGENCY LOGOUT! {reason}. Connection cut via Psycho-Breaker.", RED)
            return False
            
        log(self.node_id, f"Layer 3 Checks Passed: {reason}", GREEN)
        return True

    def _process_destination_layers(self, dna_payload: str) -> bool:
        """Handles Layer 4 Bio-Translation and Layer 5 Neural Interface when payload reaches destination."""
        log(self.node_id, "🎯 Packet reached final destination! Initiating Bio-Translation...", GREEN)
        
        # Simulated Decoding Time
        time.sleep(0.6)
        
        # --- Layer 4: Decoding ---
        original_msg = decode_dna_to_message(dna_payload)
        log(self.node_id, f"🧬 Layer 4 Bio-Translation (Decoded): '{original_msg}'", GREEN)
        
        # Simulated Layer 5 Delay
        time.sleep(0.5)
        # --- Layer 5: Neural Interface ---
        log(self.node_id, "🧠 [Layer 5] Direct Cortical Stimulation active. Delivering data to Visual Cortex...", GREEN)
        
        log(self.node_id, f"SUCCESS: Transmission Delivery Confirmed.", GREEN)
        return True

    def _process_routing_and_forwarding(self, dst: str, packet: dict) -> bool:
        """Handles Layer 1 routing logic and Slime Mold path calculation."""
        log(self.node_id, f"Not the destination. Computing Slime Mold path to '{dst}'...", CYAN)
        return self.route_and_forward(dst, packet)

    def process_packet(self, packet: dict) -> bool:
        """Processes the Layer 3 checks, routing, and Layer 4 decoding. Returns success status."""
        src = packet['src']
        dst = packet['dst']
        dna_payload = packet['payload']
        scenario = packet.get('scenario', 'normal')
        
        # Simulated Network Transfer Time
        time.sleep(0.3)
        
        log(self.node_id, f"Packet Arrived | ETH_HEADER: [SRC: {src} -> DST: {dst}] | TYPE: QSP_DNA", CYAN)
        log(self.node_id, f"Raw Payload: {dna_payload[:30]}...", CYAN)

        # --- Layer 1: Simulated Hardware Failure (For Scenario 2) ---
        dead_nodes = packet.get('dead_nodes', [])
        
        # 1. ป้องกัน Zombie Node
        if self.node_id in dead_nodes:
            log(self.node_id, "👻 [ZOMBIE NODE DETECTED] Ignoring packet. This node is supposed to be dead!", RED)
            return False

        # 2. จำลองโหนด B พังเฉพาะใน Scenario Reroute
        if scenario == 'reroute' and self.node_id == 'B' and 'B' not in dead_nodes:
            log(self.node_id, "💥 [Layer 1] DECOHERENCE DETECTED: Node B hardware failure/unreachable.", RED)
            return False # ตัดการเชื่อมต่อทันที ไม่ต้องไปเช็ค Layer 3
        
        # --- Layer 3: Psycho-Breaker (For Scenario 3) ---
        # บังคับให้เกิดวิกฤตเฉพาะใน scenario 'crisis' เท่านั้น
        force_fail = (scenario == 'crisis')
        force_safe = (scenario in ['happy', 'reroute'])
        
        is_safe, reason = check_psycho_breaker(force_fail=force_fail, force_safe=force_safe)
        if not is_safe:
            log(self.node_id, f"🚨 EMERGENCY LOGOUT! {reason}. Connection cut via Psycho-Breaker.", RED)
            return False
            
        log(self.node_id, f"Layer 3 Checks Passed: {reason}", GREEN)

        # Check if this node is the final destination
        if self.node_id == dst:
            log(self.node_id, "🎯 Packet reached final destination! Initiating Bio-Translation...", GREEN)
            time.sleep(0.6)
            
            # --- Layer 4: Decoding ---
            original_msg = decode_dna_to_message(dna_payload)
            log(self.node_id, f"🧬 Layer 4 Bio-Translation (Decoded): '{original_msg}'", GREEN)
            
            time.sleep(0.5)
            # --- Layer 5: Neural Interface ---
            log(self.node_id, "🧠 [Layer 5] Direct Cortical Stimulation active. Delivering data to Visual Cortex...", GREEN)
            log(self.node_id, f"SUCCESS: Transmission Delivery Confirmed.", GREEN)
            return True
        else:
            # Routing: We must forward it
            log(self.node_id, f"Not the destination. Computing Slime Mold path to '{dst}'...", CYAN)
            return self.route_and_forward(dst, packet)

    def route_and_forward(self, dst: str, packet: dict) -> bool:
        """Finds a path, attempts to forward, and dynamically re-routes if the next hop fails."""
        while True:
            # Synchronize dead nodes from packet memory
            dead_nodes = packet.get('dead_nodes', [])
            for dn in dead_nodes:
                if self.topology.has_node(dn):
                    self.topology.remove_node(dn)

            # Calculate shortest path based on current local view of topology
            path = get_routing_path(self.topology, self.node_id, dst)
            if not path or len(path) < 2:
                log(self.node_id, f"Routing Error: No valid path to {dst}.", RED)
                return False
                
            next_hop = path[1] # index 0 is self
            log(self.node_id, f"➡️ Next hop computed: Node {next_hop}. Forwarding...", CYAN)
            
            # Layer 2 QoS Processing
            log(self.node_id, "🌊 [Layer 2] Applying Fluidic Stream QoS. Stabilizing Jitter to 0.1ms...", CYAN)
            time.sleep(0.4) 
            
            target_port = self.port_mapping[next_hop]
            success = self.forward_packet(next_hop, target_port, packet)
            
            if success:
                # Upstream node accepted and successfully handled/routed the packet
                return True
            else:
                # ถ้าเป็นวิกฤต Psycho-Breaker ห้าม Reroute! ให้หยุดส่งทันที
                if packet.get('scenario') == 'crisis':
                    log(self.node_id, "🛑 [Layer 3] SYSTEM ABORT: Psycho-Breaker สั่งระงับการ Re-route และยกเลิกการส่งข้อมูล!", RED)
                    return False
                
                # Upstream node failed (Psycho-breaker triggered, or node dead)
                log(self.node_id, f"Connection to {next_hop} refused or timed out. Triggering Slime Mold Re-routing...", YELLOW)
                # Temporarily remove the dead/rejected node from local topology
                if self.topology.has_node(next_hop):
                    self.topology.remove_node(next_hop)
                
                # Update packet with dead node to inform future hops
                dead_nodes = packet.get('dead_nodes', [])
                if next_hop not in dead_nodes:
                    dead_nodes.append(next_hop)
                packet['dead_nodes'] = dead_nodes
                
                # Increment attempt parameter to force logic
                packet['attempt'] = packet.get('attempt', 1) + 1
                
                # Sleep briefly before finding a new path
                time.sleep(0.2)

    def forward_packet(self, next_hop: str, target_port: int, packet: dict) -> bool:
        """Sends a JSON packet over TCP socket to the next hop and waits for an ACK/NACK."""
        try:
             s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
             s.settimeout(10.0)
             s.connect((self.host, target_port))
             
             # Apply Length-Prefix Framing
             msg_data = json.dumps(packet).encode('utf-8')
             msg_length = len(msg_data)
             s.sendall(msg_length.to_bytes(4, 'big') + msg_data)
             
             response = s.recv(1024).decode('utf-8')
             s.close()
             if response == 'ACK':
                 return True
             else:
                 return False
        except Exception:
             # Assume node failure (timeout or connection refused)
             return False

    def send_initial_message(self, dst: str, message: str, scenario: str = 'normal'):
        """Initiates a message transfer from this node to a destination node."""
        log(self.node_id, "==================================================", CYAN)
        log(self.node_id, f"Initiating Transfer | Target: Node {dst} | Scenario: {scenario.upper()}", CYAN)
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
            'user_id': 'quantum_user_1X',
            'attempt': 1,
            'scenario': scenario,
            'dead_nodes': []
        }
        
        success = self.route_and_forward(dst, packet)
        
        if success:
            log(self.node_id, "==================================================", GREEN)
            log(self.node_id, "Transmission completed successfully.", GREEN)
        else:
            log(self.node_id, "==================================================", RED)
            log(self.node_id, "Transmission completely FAILED. No routes available.", RED)
