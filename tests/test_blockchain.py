import unittest
from royalnova.royalnova_blockchain import Blockchain, Transaction

class TestBlockchain(unittest.TestCase):
    
    def setUp(self):
        """Initialize a new blockchain for each test"""
        self.blockchain = Blockchain()

    def test_initialization(self):
        """Test blockchain initialization"""
        self.assertEqual(len(self.blockchain.chain), 1)  # Should start with genesis block
        self.assertEqual(len(self.blockchain.pending_transactions), 0)

    def test_add_transaction(self):
        """Test adding a new transaction"""
        tx = Transaction("Alice", "Bob", 10)
        self.blockchain.add_transaction(tx)
        self.assertEqual(len(self.blockchain.pending_transactions), 1)

    def test_mine_block(self):
        """Test mining a new block"""
        tx = Transaction("Alice", "Bob", 10)
        self.blockchain.add_transaction(tx)
        previous_length = len(self.blockchain.chain)
        
        self.blockchain.mine_block("miner1")
        self.assertEqual(len(self.blockchain.chain), previous_length + 1)
        self.assertEqual(len(self.blockchain.pending_transactions), 0)

    def test_block_validation(self):
        """Test if blockchain validates properly"""
        self.blockchain.mine_block("miner1")
        self.assertTrue(self.blockchain.is_valid())

if __name__ == "__main__":
    unittest.main()
