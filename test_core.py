import unittest
from unittest.mock import patch, MagicMock

# Import layer logic exclusively (do not import node.py or main.py to prevent socket listeners)
from src.layer4_bio import BioTranslation
from src.layer3_soul import PsychoBreaker, SoulSync
from src.layer2_sensory import SensoryStream
from src.layer1_quantum import QuantumSubstrate, DecoherenceTracker
import networkx as nx

class DummyLogger:
    def __call__(self, node_id, msg, color=None):
        pass # Silent logger for fast unit tests

class TestPsychoBreaker(unittest.TestCase):
    def setUp(self):
        self.pb = PsychoBreaker()

    def test_force_fail(self):
        """Test PsychoBreaker Cortisol Spike (Crisis scenario) triggers emergency logout."""
        is_safe, reason = self.pb.check(force_fail=True)
        self.assertFalse(is_safe, "PsychoBreaker should fail on force_fail=True")
        self.assertIn("Cortisol too high", reason)

    def test_force_safe(self):
        """Test PsychoBreaker Happy Path ensures connection stays open."""
        is_safe, reason = self.pb.check(force_safe=True)
        self.assertTrue(is_safe, "PsychoBreaker should pass on force_safe=True")
        self.assertIn("Vitals OK", reason)

class TestBioTranslation(unittest.TestCase):
    def setUp(self):
        self.bio = BioTranslation(node_id="TEST", log_cb=DummyLogger())

    def test_encode_decode_happy_path(self):
        """Test strict digital text to DNA base translation and back without mutations."""
        original = "QUANTUM FLUIDIC DATA"
        dna = self.bio._encode(original)
        
        self.assertIsInstance(dna, str)
        self.assertTrue(all(base in 'ACGT' for base in dna), "Output must be valid DNA bases.")
        
        decoded = self.bio._decode(dna)
        self.assertEqual(original, decoded, "Decoded text should exactly match the original string.")

    def test_base_substitution_and_rs_repair(self):
        """Test BSC detection and Reed-Solomon ECC capability to repair mutations."""
        original = "MISSION CRITICAL PAYLOAD"
        dna = self.bio._encode(original)
        
        # Force a mutation using the 'mutate' scenario string (forces 2-byte structural deviation)
        mutated_dna = self.bio.check_mutation(dna, scenario="mutate")
        self.assertNotEqual(dna, mutated_dna, "DNA should have mutated.")
        
        # RS Decoder should still be able to mathematically repair it and map back to the string
        repaired_text = self.bio._decode(mutated_dna)
        self.assertEqual(original, repaired_text, "Reed-Solomon failed to correct the mutated DNA bases.")

class TestQuantumSubstrate(unittest.TestCase):
    def setUp(self):
        self.tracker = DecoherenceTracker(log_cb=DummyLogger(), node_id="TEST")

    def test_decoherence_decay(self):
        """Test physical distance negatively degrades entanglement quality."""
        initial = self.tracker.get_quality("PEER_A")
        self.assertEqual(initial, 1.0)
        
        # Apply intense decay based on arbitrary weight 10
        self.tracker.apply_decay("PEER_A", distance=10)
        after_decay = self.tracker.get_quality("PEER_A")
        
        self.assertLess(after_decay, 1.0, "Entanglement quality should have dropped after decay applied.")
        self.assertGreaterEqual(after_decay, 0.0, "Quality shouldn't drop below absolute zero.")

    @patch('time.sleep', return_value=None)
    def test_entanglement_refresh(self, mock_sleep):
        """Test Quantum Refresh successfully restores quality to 1.0 without delays."""
        self.tracker.apply_decay("PEER_B", distance=20) # Guarantee drop below 0.85
        dropped_quality = self.tracker.get_quality("PEER_B")
        self.assertLess(dropped_quality, 0.85)
        
        self.tracker.refresh_entanglement("PEER_B")
        restored = self.tracker.get_quality("PEER_B")
        self.assertEqual(restored, 1.0, "Entanglement should be restored strictly to 1.0")

class TestSensoryStream(unittest.TestCase):
    def setUp(self):
        self.stream = SensoryStream(node_id="TEST", log_cb=DummyLogger())

    @patch('time.sleep', return_value=None)
    def test_fluidic_interpolation(self, mock_sleep):
        """Test Sensory Layer successfully buffers and creates interpolation variance without latency."""
        # Mock upper and lower interfaces just in case indicating loops back
        upper_mock = MagicMock()
        self.stream.set_layers(upper=upper_mock, lower=MagicMock())
        
        result = self.stream.indicate(event="APPLY_QOS", data={})
        
        self.assertTrue(result, "QoS should return success flag.")
        # Although variance mathematically drops instantly with sleep mocked, the flow buffer logic should clear up 1 item.
        self.assertEqual(len(self.stream.buffer), 0, "Wait, buffer appends 1 burst then pops it immediately, so it should be empty.")

if __name__ == '__main__':
    unittest.main(verbosity=2)
