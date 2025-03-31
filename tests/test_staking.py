import unittest
from royalnova.staking_contract import StakingContract

class TestStakingContract(unittest.TestCase):

    def setUp(self):
        """Initialize staking contract for each test"""
        self.contract = StakingContract()

    def test_stake_tokens(self):
        """Test staking tokens"""
        self.contract.stake("Alice", 100)
        self.assertEqual(self.contract.stakes["Alice"], 100)

    def test_auto_compounding(self):
        """Test auto-compounding rewards"""
        self.contract.stake("Alice", 100)
        self.contract.auto_compound("Alice")
        self.assertGreater(self.contract.stakes["Alice"], 100)

    def test_unstake_tokens(self):
        """Test unstaking tokens"""
        self.contract.stake("Alice", 100)
        self.contract.unstake("Alice")
        self.assertNotIn("Alice", self.contract.stakes)

if __name__ == "__main__":
    unittest.main()
