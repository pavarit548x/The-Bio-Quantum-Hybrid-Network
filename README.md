# The Bio-Quantum Hybrid Network Emulator

## Project Overview

Welcome to **The Bio-Quantum Hybrid Network Emulator**, an implementation of the experimental QSP (Quantum Sensory Protocol) stack developed for CP352005 Networks.

This project simulates a "Technical Reality" of network data transmission. Instead of faking localized print statements, data packets actually traverse distinct port-bound Python Sockets on `localhost`. This proves that physical node-to-node communication is occurring dynamically across a mathematically-generated Mycelium routing mesh. 

### The 5-Layer QSP Stack

1. **Layer 1 (Quantum Substrate & Mycelium Topology)**: Generates a self-healing mesh topology (Nodes A through E) via Python's `networkx` library. Handles dynamic "Slime Mold" pathfinding to successfully route data even when nodes drop out.
2. **Layer 2 (Sensory Stream)**: Implements Stream QoS to fluidly stabilize packet delivery and manage latency/jitter constraints locally at the nodes.
3. **Layer 3 (Soul Sync & Psycho-Breaker)**: Enforces connection security. Simulates physiological monitoring (HRV & Cortisol levels). If the generated values cross abnormal thresholds, the Psycho-Breaker executes an "Emergency Logout", violently cutting the connection off at the socket layer.
4. **Layer 4 (Bio-Translation)**: Standard English text payloads are translated down to 8-bit binary and synthetically mapped into a 4-base DNA sequence (`A`, `C`, `G`, `T`). This payload is shipped across the wire and converted back at the destination.
5. **Layer 5 (Neural Interface)**: The visualization layer. Upon successful decryption of the DNA packet at the target destination, data is theoretically dispatched as Cortical Stimulation to the Visual Cortex.

---

## Technical Improvements

- **Realistic Simulation & Logging**: Employs real-time Wireshark-style ANSI colored logging with precise milliseconds timestamps, and asynchronous delays (`time.sleep`) to simulate real-world propagation and biological processing times dynamically.
- **Dynamic Slime Mold Self-Healing**: Hardware node failure instantly triggers real-time recalculation of paths, forwarding via backup routes dynamically to ensure zero-downtime message delivery.
- **Message Framing**: The socket communication between nodes strictly implements Length-Prefix message framing (4-byte header) to guarantee safety from TCP Stream Fragmentation during rapid bio-data burst transmissions.
- **Architectural Modularity**: The project cleanly encapsulates QSP logic across `src/`, `docs/`, and `logs/`, enforcing separation of concerns between Layer 3 (Security), Layer 4 (Bio-Translation), Layer 5 (Neural Interface) and Layer 1 (Routing).
- **Graceful Shutdown**: The multithreaded daemon listeners gracefully handle timeout exceptions during session exits, clearing resources cleanly without relying on dummy socket connections.

---

## Project Structure

```
├── main.py             # Interactive CLI entry point and simulation runner
├── requirements.txt    # Python dependencies
├── src/                # Core QSP protocol and routing logic
│   ├── layer1_net.py   # Mycelium topology and shortest-path routing
│   ├── layer3_soul.py  # Soul Sync & Psycho-Breaker monitoring
│   ├── layer4_bio.py   # DNA to Binary translation and encoding
│   └── node.py         # Multi-threaded concurrent network node
├── docs/               # Architecture specs and planning documents
├── logs/               # Output execution logs (if applicable)
└── test_core.py        # Comprehensive isolated unit tests
```

---

## Prerequisites

- **Python 3.9** or higher.
- Requires `networkx` for topological graph generation.

```bash
pip install -r requirements.txt
```

### Running Unit Tests

The emulator includes isolated unit tests ensuring zero side-effects across all QSP layers. To validate logic integrity:

```bash
python -m unittest test_core.py
```

---

## Usage Guide (Interactive CLI)

You can launch the emulator's interactive CLI menu by running:

```bash
python main.py
```

### Menu Options

Once the script boots, you will be presented with the following options:

- **[1] Run Standard 5-Layer Simulation (Happy Path - Zero-Latency)**: Executes the full network transmission safely. Assumes all vitals are perfectly stable and traces the standard pathing through to Layer 5.
- **[2] Simulate Node Failure / Decoherence (Demonstrate Slime Mold Rerouting)**: Forcefully causes the primary routing node to suffer sudden hardware failure or decoherence. The simulation recovers utilizing **Slime Mold Zero-Downtime Re-routing**; it automatically purges the dead node from the local topology, calculates an alternate path, and successfully delivers the packet. *(Note: This failure occurs at Layer 1 due to decoherence, independent of biological vitals).*
- **[3] Simulate Psycho-Breaker Crisis (Demonstrate HRV Spike & Force Logout)**: Simulates a catastrophic biological failure at the entry node. Unusual physiological readings (e.g., Cortisol/HRV spikes) force an immediate Layer 3 emergency drop, actively refusing to re-route and rejecting the transmission completely across the array.
- **[4] View Current Mycelium Topology**: Prints out the live node connections defined in the NetworkX array.
- **[5] Exit Emulator**: Safely closes the session.

---

## Team Roles & Contributions

This project was developed under the following architectural roles:

| Role | Name | Responsibilities |
|---|---|---|
| **Architect** | Sarun Phaponchai (Ong) | BVC-01 logic, Mycelium topology, layer definitions. |
| **Engineer** | Pawaris Pamual (Boss) | QSP protocol routing, socket logic, interactive simulation core. |
| **Specialist** | Thanaphum Chanthra (Shogun) | Quantum paradox rules, Bio-Translation DNA encoding algorithms. |
| **DevOps** | Pongpob Srirak (Poom) | Environment configuration, package dependencies, README & documentation. |
| **Tester** | Sirapat Wongwiwatseri (Ohm) | System flow validation, use-case coverage, Psycho-Breaker testing. |
