import unittest
from src.layer4_bio import encode_message_to_dna, decode_dna_to_message
from src.layer3_soul import check_psycho_breaker
from src.layer1_net import build_mycelium_topology, get_routing_path

class TestLayer4Bio(unittest.TestCase):
    def test_encode_message_to_dna(self):
        message = "HELLO QUANTUM"
        encoded = encode_message_to_dna(message)
        self.assertIsInstance(encoded, str)
        self.assertGreater(len(encoded), 0, "Encoded string should not be empty")
        for base in encoded:
            self.assertIn(base, ['A', 'C', 'G', 'T'], "Should only contain valid DNA bases")

    def test_decode_dna_to_message(self):
        original = "HELLO QUANTUM"
        encoded = encode_message_to_dna(original)
        decoded = decode_dna_to_message(encoded)
        self.assertEqual(original, decoded, "Decoded string should match exactly")

class TestLayer3Soul(unittest.TestCase):
    def test_check_psycho_breaker_safe(self):
        is_safe, reason = check_psycho_breaker(force_safe=True)
        self.assertTrue(is_safe, "force_safe should return True")
        self.assertIn("Vitals OK", reason, "Reason should include 'Vitals OK'")

    def test_check_psycho_breaker_fail(self):
        is_safe, reason = check_psycho_breaker(force_fail=True)
        self.assertFalse(is_safe, "force_fail should return False")
        self.assertIn("Cortisol too high", reason, "Reason should include 'Cortisol too high'")

class TestLayer1Net(unittest.TestCase):
    def test_build_mycelium_topology(self):
        graph = build_mycelium_topology()
        nodes = list(graph.nodes)
        self.assertEqual(len(nodes), 5, "Graph should contain exactly 5 nodes")
        self.assertCountEqual(nodes, ['A', 'B', 'C', 'D', 'E'], "Nodes should be A, B, C, D, E")

    def test_get_routing_path(self):
        graph = build_mycelium_topology()
        path = get_routing_path(graph, 'A', 'D')
        self.assertGreaterEqual(len(path), 2, "Path length should be >= 2")
        self.assertEqual(path[0], 'A', "Path should start with 'A'")
        self.assertEqual(path[-1], 'D', "Path should end with 'D'")

if __name__ == '__main__':
    unittest.main(verbosity=2)
