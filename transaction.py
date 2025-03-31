from utils.crypto_utils import encrypt, decrypt
from nacl.utils import random
from nacl.secret import SecretBox
import time

# Function to create a transaction with encryption
def create_transaction(sender, receiver, amount, public_key):
    # Create the transaction message
    message = f"Royalnova transaction: {amount} RNX from {sender} to {receiver}."
    
    # Generate a random encryption key
    key = random(SecretBox.KEY_SIZE)
    
    # Encrypt the transaction data
    encrypted_transaction = encrypt(message, key, public_key)  # using the encryption function
    
    # Create the transaction with encrypted data
    transaction = {
        'sender': sender,
        'receiver': receiver,
        'amount': amount,
        'encrypted_data': encrypted_transaction,
        'timestamp': time.time(),  # Add timestamp to the transaction
    }
    
    return transaction

# Function to verify the transaction with decryption
def verify_transaction(transaction, private_key):
    # Decrypt the transaction data to verify it
    decrypted_data = decrypt(transaction['encrypted_data'], private_key)
    
    # Check if the decrypted data matches the expected transaction string
    if decrypted_data == f"Royalnova transaction: {transaction['amount']} RNX from {transaction['sender']} to {transaction['receiver']}.":
        return True
    else:
        return False

# Example Usage
if __name__ == "__main__":
    sender = "Alice"
    receiver = "Bob"
    amount = 1000
    public_key = "SomePublicKey"  # Replace with actual public key
    private_key = "SomePrivateKey"  # Replace with actual private key

    # Create a transaction
    transaction = create_transaction(sender, receiver, amount, public_key)
    print("Created Transaction:", transaction)

    # Verify the transaction
    is_valid = verify_transaction(transaction, private_key)
    print("Transaction valid:", is_valid)

