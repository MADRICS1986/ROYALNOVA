from web3 import Web3
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

RPC_URL = os.getenv("RPC_URL")
PRIVATE_KEY = os.getenv("DEPLOYER_PRIVATE_KEY")

# Connect to the blockchain
w3 = Web3(Web3.HTTPProvider(RPC_URL))

# Ensure connection is successful
if not w3.is_connected():
    print("Failed to connect to the blockchain.")
    exit()

# Load the compiled contract ABI and Bytecode
with open('RoyalnovaStaking.json', 'r') as file:
    contract_data = json.load(file)

abi = contract_data['abi']
bytecode = contract_data['bytecode']

# Create the contract deployment transaction
account = w3.eth.account.from_key(PRIVATE_KEY)
nonce = w3.eth.getTransactionCount(account.address)

# Create the contract
contract = w3.eth.contract(abi=abi, bytecode=bytecode)

# Estimate gas
gas_estimate = contract.constructor().estimate_gas()

# Create the transaction
tx = contract.constructor().build_transaction({
    'from': account.address,
    'nonce': nonce,
    'gas': gas_estimate,
    'gasPrice': w3.to_wei('10', 'gwei')
})

# Sign the transaction
signed_tx = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)

# Send the transaction
tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

# Output the contract address
print(f"✅ Contract deployed at: {tx_receipt.contractAddress}")
