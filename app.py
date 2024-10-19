from flask import Flask, request, jsonify
from blockchain import Blockchain  # Ensure correct import from blockchain module

app = Flask(__name__)
blockchain = Blockchain()

# Welcome route
@app.route('/', methods=['GET'])
def welcome():
    return jsonify({
        'message': 'Welcome to the Simple Blockchain API!',
        'available_routes': {
            '/add_transaction': 'POST - Add a new transaction',
            '/mine': 'GET - Mine pending transactions',
            '/chain': 'GET - Get the blockchain'
        }
    })

# Add transaction route
@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    data = request.get_json()
    sender = data.get('sender')
    recipient = data.get('recipient')
    amount = data.get('amount')

    try:
        blockchain.add_transaction(sender, recipient, amount)
        return jsonify({'message': 'Transaction added!'}), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

# Mine pending transactions route
@app.route('/mine', methods=['GET'])
def mine():
    blockchain.mine_pending_transactions()
    return jsonify({'message': 'New block mined!'}), 201

# Retrieve blockchain route
@app.route('/chain', methods=['GET'])
def get_chain():
    chain_data = []
    for block in blockchain.chain:
        chain_data.append({
            'index': block.index,
            'previous_hash': block.previous_hash,
            'transactions': [tx.to_dict() for tx in block.transactions],
            'timestamp': block.timestamp,
            'hash': block.hash
        })
    
    return jsonify(chain_data), 200

if __name__ == '__main__':
    print("Starting Flask server...")
    app.run(port=5000, debug=True)
