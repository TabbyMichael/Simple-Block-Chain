class Transaction:
    def __init__(self, sender, recipient, amount, fee=0):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.fee = fee  # Store the fee

    def to_dict(self):
        """Returns the transaction as a dictionary."""
        return {
            'sender': self.sender,
            'recipient': self.recipient,
            'amount': self.amount,
            'fee': self.fee
        }

    def __repr__(self):
        return f"Transaction(sender={self.sender}, recipient={self.recipient}, amount={self.amount}, fee={self.fee})"
