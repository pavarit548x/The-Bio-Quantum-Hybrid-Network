# The Bio-Quantum Hybrid Network Emulator

Welcome to the **Bio-Quantum Hybrid Network Emulator**, an implementation of the experimental QSP (Quantum Sensory Protocol) stack.

This project is a Python-based Network Emulator designed to simulate "Technical Reality" network transactions using localized Python sockets. Data is practically transmitted between distinct Node objects bound to unique localhost ports.

## Project Architecture

This emulator implements the following theoretical layers:

1. **Layer 1 (Mycelium Topology)**: A mesh network topology (Nodes A through E) generated via `networkx`. Defines the graph and uses Slime Mold (Dijkstra) algorithm concepts for routing.
2. **Layer 3 (Soul Sync & Psycho-Breaker)**: Authentication via dummy DNA/EEG verification, coupled with a dynamic "Psycho-Breaker". The system monitors pseudo-random Heart Rate Variability (HRV) and Cortisol limits for the connected "Avatar". If bounds are exceeded (e.g. HRV < 40), the node actively terminates the connection.
3. **Layer 4 (Bio-Translation)**: Translates standard text payloads into 8-bit binary, and then encodes them into a 4-base DNA sequence (`A`, `C`, `G`, `T`). At the destination, the DNA sequence is decoded back to the original text.

## Requirements

The simulation requires Python 3.9+ and the `networkx` library.

Install dependencies using:

```bash
pip install -r requirements.txt
```

## How to Run

Execute the simulation orchestration script from the terminal:

```bash
python main.py
```

### What to Expect

When `main.py` is executed, the following sequence occurs automatically:

1. **Topology Generation**: The Mycelium mesh (`layer1_net.py`) maps the connections between Nodes A, B, C, D, and E.
2. **Socket Initialization**: The driver instantiates 5 independent background threads, each binding a standard TCP Socket on localhost ports 5001 through 5005 (`node.py`).
3. **Transmission**: Node A initiates a transfer of the string `"HELLO QUANTUM WORLD!"` targeting Node D.
4. **Encoding**: Node A passes the payload through Layer 4 (`layer4_bio.py`), converting the text mathematically to a DNA string.
5. **Routing & Hopping**: The packet is forwarded across the correct intermediate nodes (e.g., A -> B -> D). Each hop conducts a Layer 3 (`layer3_soul.py`) authentication and Psycho-Breaker check.
6. **Delivery & Decoding**: If the connections aren't dropped by the Psycho-Breaker, the packet arrives at the destination port (Node D), decodes the DNA back to English text, and shuts the network down safely.

> **Note**: Because the Layer 3 Psycho-Breaker relies on *randomly generated* HRV and Cortisol metrics upon every packet hop, the simulation behavior **varies on each run**. In some runs, a packet drop (Emergency Logout) might occur mid-transit, cutting the connection. In other runs, it'll reach Node D perfectly. Simply run `python main.py` a few times to observe all the different behaviors!

## File Structure

- `main.py`: The simulation test driver.
- `node.py`: The `Node` class providing multithreaded socket communication.
- `layer1_net.py`: Infrastructure handling the `networkx` Mycelium mesh and routing.
- `layer3_soul.py`: Security and biometric monitoring limits (Psycho-Breaker).
- `layer4_bio.py`: Bio-Translation algorithms for DNA Data Encoding mechanisms.
- `requirements.txt`: Python package requirements.
