from datetime import datetime, timedelta

class DAOGovernance:
    def __init__(self):
        self.proposals = []  # Store all proposals
        self.votes = {}       # Track votes for each proposal
        self.balances = {}    # Simulated RNX token balances

    def create_proposal(self, title, description, duration_hours):
        deadline = datetime.utcnow() + timedelta(hours=duration_hours)
        proposal_id = len(self.proposals)
        self.proposals.append({
            'id': proposal_id,
            'title': title,
            'description': description,
            'deadline': deadline,
            'votes_for': 0,
            'votes_against': 0,
            'executed': False
        })
        self.votes[proposal_id] = {}
        print(f"Proposal '{title}' created with ID: {proposal_id}")

    def vote(self, proposal_id, voter, vote_for):
        if proposal_id >= len(self.proposals):
            print("Invalid proposal ID")
            return

        proposal = self.proposals[proposal_id]
        if datetime.utcnow() > proposal['deadline']:
            print("Voting period has ended")
            return

        if voter in self.votes[proposal_id]:
            print("Voter has already voted")
            return
        
        weight = self.balances.get(voter, 0)
        if weight == 0:
            print("No voting power")
            return

        if vote_for:
            proposal['votes_for'] += weight
        else:
            proposal['votes_against'] += weight

        self.votes[proposal_id][voter] = vote_for
        print(f"{voter} voted {'FOR' if vote_for else 'AGAINST'} with {weight} votes")

    def execute_proposal(self, proposal_id):
        if proposal_id >= len(self.proposals):
            print("Invalid proposal ID")
            return
        
        proposal = self.proposals[proposal_id]
        if proposal['executed']:
            print("Proposal already executed")
            return
        
        if datetime.utcnow() <= proposal['deadline']:
            print("Voting period not over")
            return
        
        if proposal['votes_for'] > proposal['votes_against']:
            print(f"Proposal '{proposal['title']}' PASSED and is being executed.")
            proposal['executed'] = True
        else:
            print(f"Proposal '{proposal['title']}' FAILED.")

    def add_balance(self, voter, amount):
        if voter not in self.balances:
            self.balances[voter] = 0
        self.balances[voter] += amount
        print(f"Added {amount} RNX to {voter}'s balance")

    def get_proposals(self):
        for p in self.proposals:
            status = 'Executed' if p['executed'] else 'Pending'
            print(f"[ID: {p['id']}] {p['title']} - {status}, Votes: {p['votes_for']} For / {p['votes_against']} Against")


# Example Usage:
# dao = DAOGovernance()
# dao.add_balance('alice', 100)
# dao.add_balance('bob', 50)
# dao.create_proposal('Increase Staking Rewards', 'Proposal to increase rewards by 10%', 24)
# dao.vote(0, 'alice', True)
# dao.vote(0, 'bob', False)
# dao.execute_proposal(0)
# dao.get_proposals()
