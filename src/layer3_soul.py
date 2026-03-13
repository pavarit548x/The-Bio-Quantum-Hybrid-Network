import random

class PsychoBreaker:
    """Manages physiological safety of the user session."""
    def check(self, force_fail=False, force_safe=False) -> tuple[bool, str]:
        if force_fail: return False, "Cortisol too high (29.9 > 25) [FORCED SIMULATION FAILURE]"
        if force_safe: return True, "Vitals OK (HRV: 85.0, Cort: 15.0) [FORCED SIMULATION SUCCESS]"

        hrv = random.uniform(30.0, 100.0)
        cortisol = random.uniform(10.0, 30.0)
        if hrv < 40.0: return False, f"HRV too low ({hrv:.1f} < 40)"
        if cortisol > 25.0: return False, f"Cortisol too high ({cortisol:.1f} > 25)"
        return True, f"Vitals OK (HRV: {hrv:.1f}, Cort: {cortisol:.1f})"

class SoulSync:
    """Layer 3: Soul Sync & Psycho-Breaker - Manages Identity and Vitality."""
    def __init__(self, node_id, log_cb):
        self.node_id = node_id
        self.log = log_cb
        self.upper_layer = None
        self.lower_layer = None
        self.psycho_breaker = PsychoBreaker()
        
    def set_layers(self, upper, lower):
        self.upper_layer = upper
        self.lower_layer = lower

    def request(self, service: str, parameters: dict):
        if service == "SECURE_AND_SEND":
            self.lower_layer.request("STREAM_AND_SEND", parameters)

    def indicate(self, event: str, data: dict):
        if event in ["PACKET_RX", "INTERMEDIATE_NODE_CHECK"]:
            scenario = data.get("scenario", "normal")
            force_fail = (scenario == 'crisis')
            force_safe = (scenario in ['happy', 'reroute'])
            
            is_safe, reason = self.psycho_breaker.check(force_fail=force_fail, force_safe=force_safe)
            if not is_safe:
                self.log(self.node_id, f"🚨 [Layer 3] EMERGENCY LOGOUT! {reason}. Connection cut via Psycho-Breaker.", "\033[91m")
                if scenario == 'crisis':
                    self.log(self.node_id, "🛑 [Layer 3] SYSTEM ABORT: Psycho-Breaker สั่งระงับการ Re-route และยกเลิกการส่งข้อมูล!", "\033[91m")
                return False
                
            self.log(self.node_id, f"🛡️ [Layer 3] Checks Passed: {reason}", "\033[92m")
            
            if event == "INTERMEDIATE_NODE_CHECK":
                return True
            return self.upper_layer.indicate("PACKET_RX", data)
            
    def confirm(self, status: str, result: dict):
        if self.upper_layer:
            self.upper_layer.confirm(status, result)
