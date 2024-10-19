import time
from block import Block  # Ensure correct import from block module
from transaction import Transaction  # Ensure correct import from transaction module

class Blockchain:
    def __init__(self):
        """Initialize the blockchain with the genesis block and default difficulty."""
        self.chain = [self.create_genesis_block()]
        self.difficulty = 2  # Mining difficulty level
        self.pending_transactions = []

    def create_genesis_block(self):
        """Create the genesis (first) block with no transactions and a default previous hash."""
        return Block(0, '0', [], time.time())

    def get_latest_block(self):
        """Return the latest block on the blockchain."""
        return self.chain[-1]

    def add_transaction(self, sender, recipient, amount):
        """Add a new transaction to the pending list after basic validation."""
        if not sender or not recipient or amount <= 0:
            raise ValueError("Invalid transaction data. Make sure sender, recipient, and a valid amount are provided.")
        self.pending_transactions.append(Transaction(sender, recipient, amount))

    def mine_pending_transactions(self):
        """
        Mine the pending transactions by creating a new block, 
        calculating the proof-of-work, and appending it to the chain.
        """
        latest_block = self.get_latest_block()
        new_block = Block(
            index=len(self.chain),
            previous_hash=latest_block.hash,
            transactions=self.pending_transactions,
            timestamp=time.time()
        )
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)
        # Reset pending transactions after mining
        self.pending_transactions = []

    def is_chain_valid(self):
        """
        Validate the entire blockchain by ensuring each block’s hash is correctly calculated 
        and linked to the previous block.
        """
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            # Check if the hash of the block is valid
            if current_block.hash != current_block.calculate_hash():
                return False

            # Check if the block links correctly to the previous one
            if current_block.previous_hash != previous_block.hash:
                return False

        return True
