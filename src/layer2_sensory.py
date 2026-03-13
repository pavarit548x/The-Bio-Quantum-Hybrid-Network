import time
import random

class SensoryStream:
    """Layer 2: Sensory Stream - handles smooth flow and avoids jitter."""
    def __init__(self, node_id, log_cb):
        self.node_id = node_id
        self.log = log_cb
        self.upper_layer = None
        self.lower_layer = None
        self.buffer = [] # Flow control buffer
        
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
            self.log(self.node_id, "📥 [Layer 2] Buffering burst payload...", "\033[94m") # Blue
            
            # Simulate placing payload size in buffer
            # Normally we'd take the data payload length, but data is empty dict here from layer 1
            # We'll mock a burst sizing
            burst_size = random.randint(50, 200) 
            self.buffer.append(burst_size)
            
            # Continuous Wave Interpolation Mock
            variance = random.uniform(0.001, 0.005)
            # Mathematical smoothing simulation (Jitter < 5ms)
            time.sleep(0.4) # Simulate strict stabilization duration
            
            self.log(self.node_id, f"🌊 [Layer 2] Applying Interpolation. Jitter stabilized to 0.1ms. Variance: {variance:.3f}", "\033[96m") # Cyan
            self.log(self.node_id, "✨ [Layer 2] Fluidic Stream converted to Continuous Wave. Proceeding.", "\033[96m")
            
            # Release buffer
            if len(self.buffer) > 0:
                self.buffer.pop(0)
                
            return True
            
    def confirm(self, status: str, result: dict):
        if self.upper_layer:
            self.upper_layer.confirm(status, result)
