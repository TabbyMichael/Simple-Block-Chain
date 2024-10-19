import time
from block import Block
from transaction import Transaction

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.difficulty = 2
        self.pending_transactions = []
        self.user_wallets = {}  # Store user wallets
        self.user_transactions = {}  # Dictionary to track user transactions
        self.event_log = []  # Event logging
        self.chain_metrics = {
            'total_transactions': 0,
            'total_blocks': 1,
            'transaction_volume': 0
        }

    def create_genesis_block(self):
        return Block(0, '0', [], time.time())

    def get_latest_block(self):
        return self.chain[-1]

    def add_transaction(self, sender, recipient, amount, fee=0):
        if amount <= 0:
            raise ValueError("Transaction amount must be positive.")

        # Create a new transaction
        transaction = Transaction(sender, recipient, amount, fee)
        
        # Add the transaction to the pending transactions
        self.pending_transactions.append(transaction)

        # Debug: print pending transactions
        print(f"Pending transactions: {self.pending_transactions}")

        # Add transaction to user_transactions
        if sender not in self.user_transactions:
            self.user_transactions[sender] = []
        self.user_transactions[sender].append(transaction)

        if recipient not in self.user_transactions:
            self.user_transactions[recipient] = []
        self.user_transactions[recipient].append(transaction)

        # Log the event
        self.event_log.append(f"Transaction added: {sender} -> {recipient}, Amount: {amount}, Fee: {fee}")

    def mine_pending_transactions(self):
        if not self.pending_transactions:
            print("No transactions to mine.")
            return "No transactions to mine."

        # Start of mining process
        print("Mining process started...")
        total_fee = sum(tx.fee for tx in self.pending_transactions)
        print(f"Total fee calculated: {total_fee}")

        # Create a new block
        try:
            new_block = Block(previous_hash=self.get_latest_block().hash, transactions=self.pending_transactions)
            print(f"New block created: {new_block}")
            self.chain.append(new_block)
        except Exception as e:
            print(f"Error while creating a new block: {e}")
            return {"error": "Failed to create a new block."}

        # Reset the pending transactions after mining
        self.pending_transactions = []  
        
        # Update chain metrics
        self.chain_metrics['total_blocks'] += 1
        self.chain_metrics['total_transactions'] += len(new_block.transactions)
        self.chain_metrics['transaction_volume'] += sum(tx.amount for tx in new_block.transactions)

        # Log the mining event
        self.event_log.append(f"New block mined! Total fee: {total_fee}")

        print("Mining process completed successfully.")
        return {"message": "New block mined!", "total_fee": total_fee}


    def get_transaction_history(self, user):
        """Retrieve all transactions for a user."""
        history = []
        for block in self.chain:
            for tx in block.transactions:
                if tx.sender == user or tx.recipient == user:
                    history.append(tx.to_dict())
        return history

    def get_chain_metrics(self):
        """Retrieve blockchain metrics."""
        print(f"Current Metrics: {self.chain_metrics}")  # Debug print
        return self.chain_metrics


    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.hash != current_block.calculate_hash():
                return False
            if current_block.previous_hash != previous_block.hash:
                return False

        return True

    def get_wallet_balance(self, user):
        if user not in self.user_transactions:
            return 0
        
        balance = 0
        for tx in self.user_transactions[user]:
            if tx.recipient == user:
                balance += tx.amount  # Incoming transaction
            if tx.sender == user:
                balance -= tx.amount  # Outgoing transaction
        return balance

