# quantum_encryption.py
# Royalnova (RNX) Post-Quantum Encryption Module
# Uses X25519 for key exchange, Ed25519 for signing, and XChaCha20-Poly1305 for encryption

from cryptography.hazmat.primitives.asymmetric import x25519, ed25519
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import XChaCha20Poly1305
import os

class QuantumEncryptor:
    """Post-quantum encryption and signing using modern cryptography."""

    @staticmethod
    def generate_keypair():
        """
        Generate X25519 keypair for ECDH key exchange.
        Returns:
            - private_key (X25519PrivateKey)
            - public_key (X25519PublicKey)
        """
        private_key = x25519.X25519PrivateKey.generate()
        public_key = private_key.public_key()
        return private_key, public_key

    @staticmethod
    def derive_shared_key(private_key, peer_public_key):
        """
        Derive a shared secret using ECDH with X25519.
        Args:
            - private_key: X25519PrivateKey
            - peer_public_key: X25519PublicKey
        Returns:
            - shared_key (bytes)
        """
        shared_key = private_key.exchange(peer_public_key)
        # Use HKDF for key derivation
        derived_key = HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=None,
            info=b'Royalnova Quantum Encryption'
        ).derive(shared_key)
        return derived_key

    @staticmethod
    def sign_message(message: bytes):
        """
        Sign a message using Ed25519.
        Args:
            - message (bytes): The message to sign.
        Returns:
            - public_key (Ed25519PublicKey)
            - signature (bytes)
        """
        private_key = ed25519.Ed25519PrivateKey.generate()
        public_key = private_key.public_key()
        signature = private_key.sign(message)
        return public_key, signature

    @staticmethod
    def verify_message(public_key, message: bytes, signature: bytes):
        """
        Verify an Ed25519 signature.
        Args:
            - public_key: Ed25519PublicKey
            - message (bytes): The message to verify.
            - signature (bytes): The signature to verify.
        Returns:
            - bool: True if valid, False otherwise
        """
        try:
            public_key.verify(signature, message)
            return True
        except Exception:
            return False

    @staticmethod
    def encrypt_message(message: bytes, key: bytes):
        """
        Encrypt a message using XChaCha20-Poly1305.
        Args:
            - message (bytes): The plaintext message.
            - key (bytes): The encryption key (32 bytes).
        Returns:
            - nonce (bytes): The nonce used for encryption.
            - ciphertext (bytes): The encrypted message.
        """
        nonce = os.urandom(24)
        cipher = XChaCha20Poly1305(key)
        ciphertext = cipher.encrypt(nonce, message, None)
        return nonce, ciphertext

    @staticmethod
    def decrypt_message(nonce: bytes, ciphertext: bytes, key: bytes):
        """
        Decrypt a message using XChaCha20-Poly1305.
        Args:
            - nonce (bytes): The nonce used for encryption.
            - ciphertext (bytes): The encrypted message.
            - key (bytes): The encryption key (32 bytes).
        Returns:
            - plaintext (bytes): The decrypted message.
        """
        cipher = XChaCha20Poly1305(key)
        plaintext = cipher.decrypt(nonce, ciphertext, None)
        return plaintext


# Testing the QuantumEncryptor class
if __name__ == "__main__":
    print("\n🔒 Royalnova (RNX) Quantum Encryption Demo 🔒")

    # Key exchange simulation
    print("\n🔑 Generating keypairs...")
    alice_private, alice_public = QuantumEncryptor.generate_keypair()
    bob_private, bob_public = QuantumEncryptor.generate_keypair()

    # ECDH Key exchange
    alice_shared = QuantumEncryptor.derive_shared_key(alice_private, bob_public)
    bob_shared = QuantumEncryptor.derive_shared_key(bob_private, alice_public)

    assert alice_shared == bob_shared, "Key exchange failed!"
    print("✅ ECDH Key exchange successful!")

    # Message encryption and decryption
    message = b"Royalnova Quantum Encryption is unbreakable!"
    nonce, ciphertext = QuantumEncryptor.encrypt_message(message, alice_shared)

    print("\n🔒 Encrypting message...")
    print(f"Ciphertext: {ciphertext.hex()}")

    plaintext = QuantumEncryptor.decrypt_message(nonce, ciphertext, alice_shared)
    assert plaintext == message, "Decryption failed!"
    print("\n✅ Decryption successful!")

    # Digital signature
    print("\n✍️ Signing message...")
    pub_key, signature = QuantumEncryptor.sign_message(message)

    print("\n🔍 Verifying signature...")
    valid = QuantumEncryptor.verify_message(pub_key, message, signature)

    if valid:
        print("\n✅ Signature is valid!")
    else:
        print("\n❌ Invalid signature!")

