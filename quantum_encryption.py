from pqcrypto.sign import dilithium3, falcon512
import hashlib

# Quantum-Resistant Key Generation
def generate_keys():
    # Generate Dilithium keys (for transaction signing)
    dilithium_pk, dilithium_sk = dilithium3.generate_keypair()
    
    # Generate Falcon keys (for wallet key generation)
    falcon_pk, falcon_sk = falcon512.generate_keypair()
    
    print("✅ Quantum-resistant keys generated successfully!")
    return {
        'dilithium': {'public': dilithium_pk, 'secret': dilithium_sk},
        'falcon': {'public': falcon_pk, 'secret': falcon_sk}
    }

# Quantum-Resistant Signing
def sign_transaction(private_key, message):
    signature = dilithium3.sign(message.encode(), private_key)
    print("✅ Transaction signed securely with Dilithium!")
    return signature

# Verification of Signature
def verify_signature(public_key, message, signature):
    try:
        dilithium3.verify(signature, message.encode(), public_key)
        print("✅ Signature verified successfully!")
        return True
    except Exception as e:
        print(f"❌ Signature verification failed: {e}")
        return False

# Secure Hashing with SHA-256
def hash_data(data):
    return hashlib.sha256(data.encode()).hexdigest()

# Example Usage
if __name__ == '__main__':
    # Generate keys
    keys = generate_keys()
    
    # Sample transaction message
    message = "Send 100 RNX to address XYZ"
    
    # Signing the transaction
    signature = sign_transaction(keys['dilithium']['secret'], message)
    
    # Verifying the signature
    is_verified = verify_signature(keys['dilithium']['public'], message, signature)
    
    # Display the hashed transaction data
    hashed_message = hash_data(message)
    print(f"🔐 Hashed Transaction Data: {hashed_message}")
