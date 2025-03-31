from utils.crypto_utils import encrypt, decrypt
from nacl.utils import random

def main():
    print("\n🚀 Testing Royalnova Encryption Integration...\n")

    # Sample transaction data
    transaction_data = "Royalnova transaction: 1000 RNX from Alice to Bob."

    # Generate a random encryption key
    key = random(32)

    # Encrypt the transaction
    encrypted_data = encrypt(transaction_data.encode(), key)
    print(f"🔐 Encrypted Transaction: {encrypted_data}")

    # Decrypt the transaction
    decrypted_data = decrypt(encrypted_data, key).decode()
    print(f"🔓 Decrypted Transaction: {decrypted_data}")

    assert decrypted_data == transaction_data, "Decryption failed!"

    print("\n✅ Encryption Integration Successful!")

if __name__ == "__main__":
    main()
