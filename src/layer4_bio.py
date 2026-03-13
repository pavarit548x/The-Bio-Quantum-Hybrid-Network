class BioTranslation:
    """Layer 4: Bio-Translation - Encodes/decodes between digital text and DNA bases."""
    def __init__(self, node_id, log_cb):
        self.node_id = node_id
        self.log = log_cb
        self.upper_layer = None
        self.lower_layer = None
        
    def set_layers(self, upper, lower):
        self.upper_layer = upper
        self.lower_layer = lower

    def request(self, service: str, parameters: dict):
        if service == "ENCODE_AND_SEND":
            msg = parameters.get("message")
            dna = self._encode(msg)
            self.log(self.node_id, f"🧬 [Layer 4] Bio-Translation (Encoded DNA): {dna[:50]}...", "\033[96m")
            self.lower_layer.request("SECURE_AND_SEND", {
                "dna_payload": dna,
                "dst": parameters.get("dst"),
                "scenario": parameters.get("scenario")
            })

    def indicate(self, event: str, data: dict):
        if event == "PACKET_RX":
            dna = data.get("dna_payload")
            message = self._decode(dna)
            self.log(self.node_id, f"🧬 [Layer 4] Bio-Translation (Decoded): '{message}'", "\033[92m")
            self.upper_layer.indicate("MESSAGE_ASSEMBLED", {"message": message})
            
    def confirm(self, status: str, result: dict):
        if self.upper_layer:
            self.upper_layer.confirm(status, result)

    def _encode(self, text: str) -> str:
        binary = ''.join(format(ord(c), '08b') for c in text)
        mapping = {'00': 'A', '01': 'C', '10': 'G', '11': 'T'}
        if len(binary) % 2 != 0: binary = '0' + binary
        return ''.join(mapping.get(binary[i:i+2], 'A') for i in range(0, len(binary), 2))

    def _decode(self, dna: str) -> str:
        reverse_mapping = {'A': '00', 'C': '01', 'G': '10', 'T': '11'}
        binary = ''.join(reverse_mapping.get(base, '00') for base in dna)
        chars = [chr(int(binary[i:i+8], 2)) for i in range(0, len(binary), 8) if len(binary[i:i+8]) == 8]
        return ''.join(chars)
