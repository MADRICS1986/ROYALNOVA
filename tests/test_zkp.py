import unittest
from royalnova.zkp_privacy import ZKPPrivacy as ZKPPrivacy

class TestZKPPrivacy(unittest.TestCase):

    def setUp(self):
        """Initialize ZKP privacy module"""
        self.zkp = ZKPPrivacy()

    def test_generate_proof(self):
        """Test generating proof"""
        sender = "Alice"
        receiver = "Bob"
        amount = 50

        proof = self.zkp.generate_proof(sender, receiver, amount)
        self.assertIsNotNone(proof)

    def test_verify_proof(self):
        """Test verifying proof"""
        sender = "Alice"
        receiver = "Bob"
        amount = 50

        proof = self.zkp.generate_proof(sender, receiver, amount)
        self.assertTrue(self.zkp.verify_proof(proof))

if __name__ == "__main__":
    unittest.main()
