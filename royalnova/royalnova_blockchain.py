import hashlib
import time
import json

class Transaction:
    """Represents a basic transaction with inputs and outputs."""
    def __init__(self, sender, recipient, amount):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.timestamp = time.time()

    def to_dict(self):
        """Converts the transaction to a dictionary format."""
        return {
            'sender': self.sender,
            'recipient': self.recipient,
            'amount': self.amount,
            'timestamp': self.timestamp
        }

    def __repr__(self):
        return f"{self.sender} -> {self.recipient}: {self.amount} RNX"


class Block:
    """Represents a block in the blockchain."""
    def __init__(self, index, previous_hash, transactions, difficulty=4):
        self.index = index
        self.timestamp = time.time()
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = 0
        self.difficulty = difficulty
        self.hash = self.mine_block()

    def calculate_hash(self):
        """Generates a SHA-256 hash of the block."""
        block_data = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": [tx.to_dict() for tx in self.transactions],
            "previous_hash": self.previous_hash,
            "nonce": self.nonce
        }, sort_keys=True)
        return hashlib.sha256(block_data.encode()).hexdigest()

    def mine_block(self):
        """Performs Proof-of-Work mining."""
        print(f"Mining block {self.index}...")
        while True:
            self.hash = self.calculate_hash()
            if self.hash[:self.difficulty] == "0" * self.difficulty:
                print(f"Block mined: {self.hash}")
                break
            self.nonce += 1
        return self.hash


class Blockchain:
    """Represents the Royalnova blockchain."""
    def __init__(self):
        self.chain = []
        self.pending_transactions = []
        self.difficulty = 4
        self.create_genesis_block()

    def create_genesis_block(self):
        """Creates the first block in the chain."""
        print("Creating Genesis Block...")
        genesis_block = Block(0, "0", [], self.difficulty)
        self.chain.append(genesis_block)

    def add_transaction(self, sender, recipient, amount):
        """Adds a transaction to the pending list."""
        tx = Transaction(sender, recipient, amount)
        self.pending_transactions.append(tx)
    
    def mine_pending_transactions(self):
        """Mines the pending transactions into a new block."""
        new_block = Block(len(self.chain), self.chain[-1].hash, self.pending_transactions, self.difficulty)
        self.chain.append(new_block)
        self.pending_transactions = []

    def is_chain_valid(self):
        """Validates the blockchain integrity."""
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]

            if current.hash != current.calculate_hash():
                return False
            if current.previous_hash != previous.hash:
                return False
        return True

    def display_chain(self):
        """Displays the entire blockchain."""
        for block in self.chain:
            print(f"\nBlock {block.index}:")
            print(f"Timestamp: {block.timestamp}")
            print(f"Previous Hash: {block.previous_hash}")
            print(f"Hash: {block.hash}")
            print(f"Transactions:")
            for tx in block.transactions:
                print(f"  {tx}")

# --- Execution ---
if __name__ == "__main__":
    rn_chain = Blockchain()

    # Add some sample transactions
    rn_chain.add_transaction("Alice", "Bob", 50)
    rn_chain.add_transaction("Bob", "Charlie", 25)

    # Mine the transactions into a new block
    rn_chain.mine_pending_transactions()

    # Display the blockchain
    rn_chain.display_chain()

    # Validate the chain
    print("\nBlockchain valid:", rn_chain.is_chain_valid())
