# layer3_soul.py
import random
import time

# Layer 3: Soul Sync & Psycho-Breaker

def verify_soul_id(user_id: str, dna_sample: str, eeg_sample: str) -> bool:
    """
    Checks `verify_soul_id` (dummy DNA+EEG check).
    In a real system, this would compare against a secure database.
    """
    # Dummy check: As long as it's not empty, we consider it valid for the simulation.
    if user_id and dna_sample and eeg_sample:
        return True
    return False

def check_psycho_breaker() -> tuple[bool, str]:
    """
    PsychoBreaker: Generates a random HRV (Heart Rate Variability) and Cortisol level.
    If HRV < 40 or Cortisol > 25, the node MUST actively reject the connection/packet.
    
    Returns:
        (is_safe: bool, reason: str)
    """
    # Generate random physiological data
    hrv = random.uniform(30.0, 100.0) # normal: 50-100, abnormal: < 40
    cortisol = random.uniform(10.0, 30.0) # normal: 10-20, abnormal: > 25
    
    # 10% chance to force an emergency logout for demonstration if we want,
    # but let's stick to the raw probability from the uniform distribution.
    
    if hrv < 40.0:
        return False, f"HRV too low ({hrv:.1f} < 40)"
    if cortisol > 25.0:
        return False, f"Cortisol too high ({cortisol:.1f} > 25)"
        
    return True, f"Vitals OK (HRV: {hrv:.1f}, Cort: {cortisol:.1f})"
