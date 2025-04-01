# origin_config.py

# Core Blockchain Parameters
BLOCK_SIZE = 2 * 1024 * 1024  # 2 MB
BLOCK_TIME = 600  # 10 minutes (in seconds)
MAX_SUPPLY = 10_000_000  # 10 million coins
INITIAL_REWARD = 50  # 50 coins per block
HALVING_INTERVAL = 210_000  # Halves every 210,000 blocks

# Mining Difficulty
DIFFICULTY_ADJUSTMENT_INTERVAL = 2016  # Every 2016 blocks
target_time_per_block = 600  # 10 minutes (in seconds)

# Genesis Block Info
GENESIS_REWARD = 50  # Reward for mining the genesis block

# Transaction Fees and Limits
MIN_TRANSACTION_FEE = 0.0001  # Minimum fee per transaction
MAX_TRANSACTIONS_PER_BLOCK = 1000  # Limit for transactions in one block
