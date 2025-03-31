import time
import hashlib

# -------------------------------
# Origin Coin Tokenomics
# -------------------------------
TOTAL_SUPPLY = 10_000_000  # 10 million coins (fixed supply)
BLOCK_REWARD = 50  # Initial block reward
HALVING_INTERVAL = 210_000  # Halving every 210,000 blocks
DIFFICULTY = 5  # Initial mining difficulty (adjust as needed)

class Block:
    def __init__(self, index, previous_hash, timestamp, data, nonce=0):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.nonce = nonce
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        value = f"{self.index}{self.previous_hash}{self.timestamp}{self.data}{self.nonce}"
        return hashlib.sha256(value.encode()).hexdigest()

    def mine_block(self, difficulty):
        """Simple Proof-of-Work algorithm"""
        target = "0" * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()

        print(f"Block mined: {self.hash}")


# -------------------------------
# Blockchain Initialization
# -------------------------------
def create_genesis_block():
    return Block(0, "0", int(time.time()), "Genesis Block")

def create_new_block(previous_block, data):
    return Block(previous_block.index + 1, previous_block.hash, int(time.time()), data)

# -------------------------------
# Mining Simulation
# -------------------------------
def simulate_mining():
    blockchain = [create_genesis_block()]
    print("Genesis Block created!")

    for i in range(1, 6):  # Simulate mining 5 blocks
        new_block = create_new_block(blockchain[-1], f"Block #{i} Data")
        print(f"Mining Block {i}...")
        new_block.mine_block(DIFFICULTY)
        blockchain.append(new_block)
        print(f"Block {i} mined with hash: {new_block.hash}\n")


if __name__ == "__main__":
    simulate_mining()
