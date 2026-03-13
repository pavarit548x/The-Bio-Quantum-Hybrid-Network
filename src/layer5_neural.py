import time

class NeuralInterface:
    """Layer 5: Neural Interface - Direct Cortical Stimulation. The Top of the stack."""
    def __init__(self, node_id, log_cb):
        self.node_id = node_id
        self.log = log_cb
        self.lower_layer = None
        
    def set_layers(self, lower):
        self.lower_layer = lower

    def request(self, service: str, parameters: dict):
        if service == "SEND_MESSAGE":
            dst = parameters.get("dst")
            msg = parameters.get("message")
            scenario = parameters.get("scenario", "normal")
            
            self.log(self.node_id, "==================================================", "\033[96m")
            self.log(self.node_id, f"Initiating Transfer | Target: Node {dst} | Scenario: {scenario.upper()}", "\033[96m")
            self.log(self.node_id, f"🗨️ Original Message: '{msg}'", "\033[96m")
            
            time.sleep(0.5)
            self.lower_layer.request("ENCODE_AND_SEND", parameters)

    def indicate(self, event: str, data: dict):
        if event == "MESSAGE_ASSEMBLED":
            time.sleep(0.5)
            self.log(self.node_id, "🧠 [Layer 5] Direct Cortical Stimulation active. Delivering data to Visual Cortex...", "\033[92m")
            self.log(self.node_id, "SUCCESS: Transmission Delivery Confirmed.", "\033[92m")
            self.log(self.node_id, "==================================================", "\033[92m")

    def confirm(self, status: str, result: dict):
        pass
