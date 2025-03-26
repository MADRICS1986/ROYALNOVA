import time

class StakingContract:
    def __init__(self):
        self.stakes = {}  # {user: {'amount': RNX, 'start_time': timestamp, 'duration': months, 'rewards': RNX}}
        self.reward_rates = {1: 0.05, 3: 0.15, 6: 0.30, 12: 0.50}
        self.early_withdraw_penalty = 0.10
        self.min_stake = 50

    def stake(self, user, amount, duration):
        """ Stake RNX with duration in months """
        if amount < self.min_stake:
            print(f"❌ Minimum stake is {self.min_stake} RNX.")
            return

        if duration not in self.reward_rates:
            print("❌ Invalid staking duration.")
            return

        current_time = time.time()
        self.stakes[user] = {
            'amount': amount,
            'start_time': current_time,
            'duration': duration,
            'rewards': 0
        }

        print(f"✅ {user} staked {amount} RNX for {duration} months!")

    def calculate_rewards(self, user):
        """ Calculate rewards based on staking duration """
        if user not in self.stakes:
            print("❌ User not found.")
            return 0

        stake = self.stakes[user]
        duration = stake['duration']
        amount = stake['amount']
        
        # Time since staking
        current_time = time.time()
        elapsed_time = (current_time - stake['start_time']) / (30 * 24 * 60 * 60)  # Months

        if elapsed_time < duration:
            print(f"⏳ Staking period not completed. {duration - elapsed_time:.2f} months remaining.")
            return 0

        # Calculate rewards with auto-compounding
        reward_rate = self.reward_rates[duration]
        compounded_rewards = amount * ((1 + reward_rate) ** (elapsed_time / duration)) - amount

        # Auto-compounding logic
        self.stakes[user]['rewards'] += compounded_rewards
        print(f"🔥 {user} earned {compounded_rewards:.2f} RNX in rewards!")

        return compounded_rewards

    def withdraw(self, user):
        """ Withdraw staked RNX with rewards """
        if user not in self.stakes:
            print("❌ No stake found.")
            return

        stake = self.stakes[user]
        current_time = time.time()
        elapsed_time = (current_time - stake['start_time']) / (30 * 24 * 60 * 60)  # Months

        if elapsed_time < stake['duration']:
            # Early withdrawal penalty
            penalty = stake['amount'] * self.early_withdraw_penalty
            final_amount = stake['amount'] - penalty
            print(f"❌ Early withdrawal: {penalty:.2f} RNX penalty applied.")
        else:
            final_amount = stake['amount'] + stake['rewards']

        print(f"💰 {user} withdrew {final_amount:.2f} RNX!")
        del self.stakes[user]

    def show_stake(self, user):
        """ Display staking info """
        if user not in self.stakes:
            print("❌ No active stake.")
            return

        stake = self.stakes[user]
        elapsed_time = (time.time() - stake['start_time']) / (30 * 24 * 60 * 60)
        
        print("\n👑 **Royalnova Staking Info**")
        print(f"User: {user}")
        print(f"Staked: {stake['amount']} RNX")
        print(f"Duration: {stake['duration']} months")
        print(f"Elapsed: {elapsed_time:.2f} months")
        print(f"Rewards: {stake['rewards']:.2f} RNX")

# --- Example Usage ---
contract = StakingContract()

# Users staking
contract.stake("alice", 100, 6)
contract.stake("bob", 200, 12)

# Simulate time passing
time.sleep(2)

# Calculate rewards
contract.calculate_rewards("alice")
contract.calculate_rewards("bob")

# Withdraw after staking
contract.withdraw("alice")
contract.show_stake("bob")
