import unittest
from royalnova.dao_governance import DAOGovernance

class TestDAOGovernance(unittest.TestCase):

    def setUp(self):
        """Initialize DAO Governance"""
        self.dao = DAOGovernance()

    def test_create_proposal(self):
        """Test creating a proposal"""
        self.dao.create_proposal("Increase staking rewards", "Alice")
        self.assertEqual(len(self.dao.proposals), 1)

    def test_vote_on_proposal(self):
        """Test voting on a proposal"""
        self.dao.create_proposal("Increase staking rewards", "Alice")
        self.dao.vote(0, "Bob", True)
        self.assertEqual(self.dao.proposals[0]["votes"]["Bob"], True)

    def test_execute_proposal(self):
        """Test executing a proposal"""
        self.dao.create_proposal("Increase staking rewards", "Alice")
        self.dao.vote(0, "Bob", True)
        self.dao.vote(0, "Charlie", True)
        
        result = self.dao.execute_proposal(0)
        self.assertEqual(result, "Proposal executed!")

if __name__ == "__main__":
    unittest.main()
