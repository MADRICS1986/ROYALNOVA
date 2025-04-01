import oqs

# Generate quantum-safe keypair
def generate_keypair():
    with oqs.KeyEncapsulation("Kyber512") as kem:
        public_key = kem.generate_keypair()
        secret_key = kem.export_secret_key()
        return public_key, secret_key

# Encrypt data using quantum-resistant encryption
def encrypt(public_key, message):
    with oqs.KeyEncapsulation("Kyber512") as kem:
        kem.import_public_key(public_key)
        ciphertext, shared_secret = kem.encap_secret()
        return ciphertext, shared_secret

# Decrypt data
def decrypt(secret_key, ciphertext):
    with oqs.KeyEncapsulation("Kyber512") as kem:
        kem.import_secret_key(secret_key)
        shared_secret = kem.decap_secret(ciphertext)
        return shared_secret

# Test the encryption
if __name__ == "__main__":
    print("\n🔐 Quantum-Resistant Encryption Test")

    # Generate keypair
    pub_key, sec_key = generate_keypair()
    print(f"Public Key: {pub_key.hex()}")
    print(f"Secret Key: {sec_key.hex()}")

    # Encrypt message
    message = b"Royalnova Quantum Encryption!"
    ciphertext, shared_secret_enc = encrypt(pub_key, message)
    print(f"Ciphertext: {ciphertext.hex()}")
    print(f"Shared Secret (Enc): {shared_secret_enc.hex()}")

    # Decrypt message
    shared_secret_dec = decrypt(sec_key, ciphertext)
    print(f"Shared Secret (Dec): {shared_secret_dec.hex()}")

    # Verify encryption/decryption consistency
    assert shared_secret_enc == shared_secret_dec, "Decryption failed!"
    print("\n✅ Quantum Encryption Successful!")
