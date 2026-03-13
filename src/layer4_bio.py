import random
from reedsolo import RSCodec

class BioTranslation:
    """Layer 4: Bio-Translation - Encodes/decodes between digital text and DNA bases with RS ECC."""
    def __init__(self, node_id, log_cb):
        self.node_id = node_id
        self.log = log_cb
        self.upper_layer = None
        self.lower_layer = None
        # Initialize Reed-Solomon Codec RS(255, 223) -> 32 error correction bytes
        self.rsc = RSCodec(32)
        
    def set_layers(self, upper, lower):
        self.upper_layer = upper
        self.lower_layer = lower

    def request(self, service: str, parameters: dict):
        if service == "ENCODE_AND_SEND":
            msg = parameters.get("message")
            dna = self._encode(msg)
            self.log(self.node_id, f"[i] [Layer 4] RS ECC Applied. DNA length extended.", "\033[93m")
            
            dna_display = ""
            for i in range(0, min(len(dna), 64), 16):
                chunk = dna[i:i+16]
                colored = chunk.replace('A', '\033[91mA\033[96m').replace('T', '\033[92mT\033[96m').replace('C', '\033[93mC\033[96m').replace('G', '\033[94mG\033[96m')
                dna_display += f"        [DNA-BLOCK {idx:02X}0] {colored}\n" if 'idx' in locals() else f"        [DNA-BLOCK {i//16:02X}0] {colored}\n"
            
            self.log(self.node_id, f"[i] [Layer 4] Bio-Translation (Encoded DNA):\n{dna_display.rstrip()}\033[0m", "\033[96m")
            self.lower_layer.request("SECURE_AND_SEND", {
                "dna_payload": dna,
                "dst": parameters.get("dst"),
                "scenario": parameters.get("scenario")
            })

    def indicate(self, event: str, data: dict):
        if event == "PACKET_RX":
            dna = data.get("dna_payload")
            scenario = data.get("scenario", "normal")
            
            # Simulate Base Substitution Check (BSC) mutation
            dna = self.check_mutation(dna, scenario)
            
            message = self._decode(dna)
            
            if message:
                self.log(self.node_id, f"[SUCCESS] [Layer 4] Bio-Translation (Decoded): '{message}'", "\033[92m")
                return self.upper_layer.indicate("MESSAGE_ASSEMBLED", {"message": message})
            else:
                self.log(self.node_id, f"[CRITICAL] [Layer 4] Decoded message is corrupted beyond RS recovery.", "\033[91m")
                return False
            
    def confirm(self, status: str, result: dict):
        if self.upper_layer:
            self.upper_layer.confirm(status, result)

    def check_mutation(self, dna_sequence: str, scenario: str) -> str:
        """Simulates DNA mutation (Base Substitution Check) during transmission."""
        if scenario == 'reroute' and random.random() < 0.5: # 50% chance of mutation in reroute path
            self.log(self.node_id, f"[WARN] [Layer 4] BSC detected structural DNA mutation (Radiation/Decoherence).", "\033[93m")
            # Flip a random base
            idx = random.randint(0, len(dna_sequence) - 1)
            bases = ['A', 'C', 'G', 'T']
            bases.remove(dna_sequence[idx])
            mutated_dna = dna_sequence[:idx] + random.choice(bases) + dna_sequence[idx+1:]
            return mutated_dna
        return dna_sequence

    def _encode(self, text: str) -> str:
        # Encode string to bytes, apply RS, then byte array to binary string
        message_bytes = text.encode('utf-8')
        encoded_bytes = self.rsc.encode(message_bytes)
        
        binary = ''.join(format(b, '08b') for b in encoded_bytes)
        mapping = {'00': 'A', '01': 'C', '10': 'G', '11': 'T'}
        if len(binary) % 2 != 0: binary = '0' + binary
        return ''.join(mapping.get(binary[i:i+2], 'A') for i in range(0, len(binary), 2))

    def _decode(self, dna: str) -> str:
        reverse_mapping = {'A': '00', 'C': '01', 'G': '10', 'T': '11'}
        binary = ''.join(reverse_mapping.get(base, '00') for base in dna)
        
        # Convert binary string to bytes
        byte_list = [int(binary[i:i+8], 2) for i in range(0, len(binary), 8) if len(binary[i:i+8]) == 8]
        encoded_bytes = bytes(byte_list)
        
        try:
            # RS Decoder automatically fixes errors if within limit
            decoded_message, decoded_message_with_ecc, err_positions = self.rsc.decode(encoded_bytes)
            if len(err_positions) > 0:
                 self.log(self.node_id, f"[+] [Layer 4] RS Decoder successfully corrected {len(err_positions)} byte errors.", "\033[92m")
            # RSCodec returns the decoded message as bytearray
            return decoded_message.decode('utf-8', errors='ignore')
        except Exception as e:
            self.log(self.node_id, f"[X] [Layer 4] RS Decode Failure: {e}", "\033[91m")
            return None
