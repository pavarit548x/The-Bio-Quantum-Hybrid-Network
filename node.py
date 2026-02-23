import socket
import threading
import json
from layer4_bio import encode_message_to_dna, decode_dna_to_message
from layer3_soul import verify_soul_id, check_psycho_breaker

class Node:
    """
    Represents a network device in the Bio-Quantum network.
    Communicates using local Python Sockets via TCP.
    """
    def __init__(self, node_id: str, host: str, port: int, routing_table: dict, port_mapping: dict):
        self.node_id = node_id
        self.host = host
        self.port = port
        self.routing_table = routing_table
        self.port_mapping = port_mapping
        
        # Setup socket
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        
        self.running = False
        self.thread = threading.Thread(target=self.listen, daemon=True)

    def start(self):
        """Starts the background listening socket thread."""
        self.running = True
        self.thread.start()
        print(f"[Node {self.node_id}] Booted and listening on {self.host}:{self.port}...")

    def stop(self):
        """Stops the socket listener."""
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
        """Handles an incoming packet."""
        try:
            data = conn.recv(4096).decode('utf-8')
            if not data:
                return
            
            # Simple packet structure as JSON
            packet = json.loads(data)
            
            # If the packet has the 'stop' flag, just exit
            if packet.get('action') == 'stop':
                return
                
            self.process_packet(packet)
        except json.JSONDecodeError:
            pass
        except Exception as e:
            print(f"[Node {self.node_id}] Error handling packet: {e}")
        finally:
            conn.close()

    def process_packet(self, packet: dict):
        """Processes the Layer 3 checks, routing, and Layer 4 decoding."""
        src = packet['src']
        dst = packet['dst']
        dna_payload = packet['payload']
        user_id = packet.get('user_id', 'quantum_user_1X')
        
        # When receiving, log the hop
        print(f"\n[Node {self.node_id}] --------------------------------------------------")
        print(f"[Node {self.node_id}] Packet Arrived | From: {src} -> To: {dst}")
        
        # --- Layer 3: Soul Sync Verify ---
        if not verify_soul_id(user_id, "ACTG_VALID", "EEG_WAVES_VALID"):
            print(f"[Node {self.node_id}] ❌ Layer 3 Failed: Invalid Soul ID. Dropping packet.")
            return

        # --- Layer 3: Psycho-Breaker ---
        is_safe, reason = check_psycho_breaker()
        if not is_safe:
            print(f"[Node {self.node_id}] ❌ EMERGENCY LOGOUT! {reason}. Connection cut.")
            return
            
        print(f"[Node {self.node_id}] ✅ Layer 3 Checks Passed: {reason}")

        # Check if this node is the final destination
        if self.node_id == dst:
            print(f"[Node {self.node_id}] 🎯 Packet reached final destination!")
            print(f"[Node {self.node_id}] Encoded payload (DNA): {dna_payload}")
            
            # --- Layer 4: Decoding ---
            original_msg = decode_dna_to_message(dna_payload)
            print(f"[Node {self.node_id}] 🧬 Layer 4 Bio-Translation (Decoded): '{original_msg}'")
            print(f"[Node {self.node_id}] --------------------------------------------------\n")
        else:
            # Routing: We must forward it
            print(f"[Node {self.node_id}] 🛣️ Not the destination. Looking up next hop for '{dst}'...")
            path = self.routing_table.get(dst)
            
            if path and self.node_id in path:
                idx = path.index(self.node_id)
                if idx + 1 < len(path):
                    next_hop = path[idx + 1]
                    print(f"[Node {self.node_id}] ➡️ Forwarding packet to Node {next_hop}...")
                    self.forward_packet(next_hop, packet)
                else:
                    print(f"[Node {self.node_id}] ❌ Routing error: Nowhere to forward.")
            else:
                print(f"[Node {self.node_id}] ❌ Routing error: No route to {dst}.")

    def forward_packet(self, next_hop: str, packet: dict):
        """Sends a JSON packet over TCP socket to the next hop."""
        target_port = self.port_mapping[next_hop]
        try:
             s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
             s.connect((self.host, target_port))
             s.sendall(json.dumps(packet).encode('utf-8'))
             s.close()
        except Exception as e:
             print(f"[Node {self.node_id}] Failed to forward packet to {next_hop} on port {target_port}: {e}")

    def send_initial_message(self, dst: str, message: str):
        """Initiates a message transfer from this node to a destination node."""
        print(f"\n[Node {self.node_id}] ==================================================")
        print(f"[Node {self.node_id}] Initiating Transfer | Target: Node {dst}")
        print(f"[Node {self.node_id}] 🗨️ Original Message: '{message}'")
        
        # --- Layer 4: Encoding ---
        dna_payload = encode_message_to_dna(message)
        print(f"[Node {self.node_id}] 🧬 Layer 4 Bio-Translation (Encoded DNA): {dna_payload}")
        
        packet = {
            'src': self.node_id,
            'dst': dst,
            'payload': dna_payload,
            'user_id': 'quantum_user_1X'
        }
        
        # Find path to determine first hop
        path = self.routing_table.get(dst)
        if path and self.node_id in path:
            idx = path.index(self.node_id)
            if idx + 1 < len(path):
                next_hop = path[idx + 1]
                print(f"[Node {self.node_id}] ➡️ First hop is Node {next_hop}. Sending...")
                print(f"[Node {self.node_id}] ==================================================\n")
                self.forward_packet(next_hop, packet)
            else:
                print(f"[Node {self.node_id}] Cannot send to self.")
        else:
            print(f"[Node {self.node_id}] ❌ Routing error: No route to {dst}.")
