import hashlib
import time
from origin_config import BLOCK_TIME, GENESIS_REWARD, DIFFICULTY_ADJUSTMENT_INTERVAL

class Block:
    def __init__(self, index, previous_hash, timestamp, data, reward, difficulty):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.reward = reward
        self.difficulty = difficulty
        self.nonce = 0
        self.hash = self.calculate_hash()
    
    def calculate_hash(self):
        block_data = f"{self.index}{self.previous_hash}{self.timestamp}{self.data}{self.reward}{self.difficulty}{self.nonce}"
        return hashlib.sha256(block_data.encode()).hexdigest()
    
    def mine_block(self):
        target = '0' * self.difficulty
        while not self.hash.startswith(target):
            self.nonce += 1
            self.hash = self.calculate_hash()
        return self.hash

def create_genesis_block():
    return Block(0, "0" * 64, int(time.time()), "Genesis Block", GENESIS_REWARD, 4)

def add_block(blockchain, data, reward):
    previous_block = blockchain[-1]
    new_block = Block(
        index=len(blockchain),
        previous_hash=previous_block.hash,
        timestamp=int(time.time()),
        data=data,
        reward=reward,
        difficulty=adjust_difficulty(blockchain)
    )
    new_block.mine_block()
    blockchain.append(new_block)
    return new_block

def adjust_difficulty(blockchain):
    if len(blockchain) % DIFFICULTY_ADJUSTMENT_INTERVAL == 0:
        actual_time = blockchain[-1].timestamp - blockchain[-DIFFICULTY_ADJUSTMENT_INTERVAL].timestamp
        expected_time = DIFFICULTY_ADJUSTMENT_INTERVAL * BLOCK_TIME
        if actual_time < expected_time // 2:
            return blockchain[-1].difficulty + 1
        elif actual_time > expected_time * 2:
            return max(1, blockchain[-1].difficulty - 1)
    return blockchain[-1].difficulty

def print_blockchain(blockchain):
    for block in blockchain:
        print(f"Block {block.index}: {block.hash}")

# Execution for testing
if __name__ == '__main__':
    blockchain = [create_genesis_block()]
    print("Genesis Block created!")
    
    # Mine 5 blocks for demonstration
    for i in range(1, 6):
        print(f"Mining Block {i}...")
        add_block(blockchain, f"Block {i} data", GENESIS_REWARD)
        print(f"Block {i} mined with hash: {blockchain[-1].hash}\n")

    print_blockchain(blockchain)
