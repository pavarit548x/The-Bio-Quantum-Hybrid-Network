import socket
import threading
import json
import datetime
import networkx as nx
from src.layer1_quantum import QuantumSubstrate
from src.layer2_sensory import SensoryStream
from src.layer3_soul import SoulSync
from src.layer4_bio import BioTranslation
from src.layer5_neural import NeuralInterface

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
    Purely acts as a physical hardware container (BVC-01).
    Manages TCP sockets, threading, and QSP Stack delegation.
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

        # Output explicit instantiation for layers
        self.layer1 = QuantumSubstrate(self.node_id, log, self)
        self.layer2 = SensoryStream(self.node_id, log)
        self.layer3 = SoulSync(self.node_id, log)
        self.layer4 = BioTranslation(self.node_id, log)
        self.layer5 = NeuralInterface(self.node_id, log)

        # Wire the layers together using strict Separation of Concerns
        self.layer1.set_layers(upper=self.layer2)
        self.layer2.set_layers(upper=self.layer3, lower=self.layer1)
        self.layer3.set_layers(upper=self.layer4, lower=self.layer2)
        self.layer4.set_layers(upper=self.layer5, lower=self.layer3)
        self.layer5.set_layers(lower=self.layer4)

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
        """Handles an incoming packet over the wire and pushes it into the QSP Stack."""
        try:
            raw_msglen = self._recvall(conn, 4)
            if not raw_msglen:
                return
            msglen = int.from_bytes(raw_msglen, 'big')
            
            data_bytes = self._recvall(conn, msglen)
            if not data_bytes:
                return
            
            data = data_bytes.decode('utf-8')
            packet = json.loads(data)
            
            if packet.get('action') == 'stop':
                return
                
            # Delegate entirely to Layer 1 (QuantumSubstrate)
            success = self.layer1.indicate("PACKET_RX", packet)
            
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

    def forward_packet(self, next_hop: str, target_port: int, packet: dict) -> bool:
        """Called by Layer 1. Sends a JSON packet over TCP socket to the next hop and waits for an ACK/NACK."""
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
        """Initiates a message transfer by triggering Layer 5 directly."""
        self.layer5.request("SEND_MESSAGE", {
            "dst": dst,
            "message": message,
            "scenario": scenario
        })
