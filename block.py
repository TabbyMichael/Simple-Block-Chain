import time
import hashlib

class Block:
    def __init__(self, index, previous_hash, transactions, timestamp=None):
        self.index = index
        self.previous_hash = previous_hash
        self.transactions = transactions
        self.timestamp = timestamp or time.time()
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        """Calculate the hash of the block using SHA-256."""
        block_string = f"{self.index}{self.previous_hash}{self.transactions}{self.timestamp}".encode()
        return hashlib.sha256(block_string).hexdigest()

    def mine_block(self, difficulty):
        """Simulate mining by finding a hash with the specified number of leading zeros."""
        nonce = 0
        while True:
            self.hash = self.calculate_hash()
            if self.hash.startswith('0' * difficulty):
                print(f"Block mined with nonce: {nonce}, Hash: {self.hash}")  # Log the mining process
                break
            nonce += 1
