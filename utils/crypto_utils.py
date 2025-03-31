from nacl.secret import SecretBox
from nacl.utils import random

def encrypt(data: bytes, key: bytes) -> bytes:
    """Encrypts the given data using XChaCha20Poly1305."""
    box = SecretBox(key)
    nonce = random(24)
    encrypted = box.encrypt(data, nonce)
    return encrypted

def decrypt(encrypted: bytes, key: bytes) -> bytes:
    """Decrypts the given encrypted data using XChaCha20Poly1305."""
    box = SecretBox(key)
    decrypted = box.decrypt(encrypted)
    return decrypted

if __name__ == "__main__":
    print("\n✅ Crypto module is ready!")

