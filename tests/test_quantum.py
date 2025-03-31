import unittest
from royalnova.quantum_encryption import QuantumEncryptor

class TestQuantumEncryption(unittest.TestCase):

    def setUp(self):
        """Initialize Quantum Encryptor"""
        self.encryptor = QuantumEncryptor()

    def test_key_generation(self):
        """Test if quantum keys are generated"""
        self.assertIsNotNone(self.encryptor.dilithium_public_key)
        self.assertIsNotNone(self.encryptor.falcon_public_key)

    def test_sign_and_verify(self):
        """Test signing and verification"""
        message = b"Royalnova is the king of crypto!"
        signature = self.encryptor.sign_message(message)
        self.assertTrue(self.encryptor.verify_signature(message, signature))

if __name__ == "__main__":
    unittest.main()
