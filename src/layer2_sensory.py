import time

class SensoryStream:
    """Layer 2: Sensory Stream - handles smooth flow and avoids jitter."""
    def __init__(self, node_id, log_cb):
        self.node_id = node_id
        self.log = log_cb
        self.upper_layer = None
        self.lower_layer = None
        
    def set_layers(self, upper, lower):
        self.upper_layer = upper
        self.lower_layer = lower

    def request(self, service: str, parameters: dict):
        if service == "STREAM_AND_SEND":
            self.lower_layer.request("ROUTE_AND_SEND", parameters)

    def indicate(self, event: str, data: dict):
        if event == "PACKET_RX":
            return self.upper_layer.indicate("PACKET_RX", data)
        elif event == "INTERMEDIATE_NODE_CHECK":
            return self.upper_layer.indicate("INTERMEDIATE_NODE_CHECK", data)
        elif event == "APPLY_QOS":
            self.log(self.node_id, "🌊 [Layer 2] Applying Fluidic Stream QoS. Stabilizing Jitter to 0.1ms...", "\033[96m")
            time.sleep(0.4)
            return True
            
    def confirm(self, status: str, result: dict):
        if self.upper_layer:
            self.upper_layer.confirm(status, result)
