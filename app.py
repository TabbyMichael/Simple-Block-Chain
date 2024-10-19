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
            '/chain': 'GET - Get the blockchain',
            '/validate': 'GET - Validate the blockchain',
            '/transactions': 'GET - View transaction history for a user',
            '/wallet_balance': 'GET - Get wallet balance for a user',
            '/metrics': 'GET - Get blockchain metrics',
            '/event_log': 'GET - Get event logs',
        }
    })

# Add transaction route
@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    data = request.get_json()
    try:
        sender = data['sender']
        recipient = data['recipient']
        amount = data['amount']
        fee = data.get('fee', 0)

        blockchain.add_transaction(sender, recipient, amount, fee)
        return jsonify({'message': 'Transaction added!'}), 201
    except KeyError as e:
        return jsonify({'error': f'Missing field: {str(e)}'}), 400
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

# Mine pending transactions route
@app.route('/mine', methods=['GET'])
def mine():
    result = blockchain.mine_pending_transactions()
    return jsonify(result), 201

# Get transaction history route
@app.route('/transactions', methods=['GET'])
def get_transactions():
    user = request.args.get('user')
    if user not in blockchain.user_transactions:
        return jsonify([]), 200
    return jsonify([tx.to_dict() for tx in blockchain.user_transactions[user]]), 200


# Get wallet balance route
@app.route('/wallet_balance', methods=['GET'])
def get_wallet_balance():
    user = request.args.get('user')
    balance = blockchain.get_wallet_balance(user)
    return jsonify({'balance': balance}), 200


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

# Validate blockchain route
@app.route('/validate', methods=['GET'])
def validate_chain():
    is_valid = blockchain.is_chain_valid()
    if is_valid:
        return jsonify({'message': 'Blockchain is valid!'}), 200
    else:
        return jsonify({'message': 'Blockchain is invalid!'}), 400

# Get blockchain metrics route
@app.route('/metrics', methods=['GET'])
def get_metrics():
    metrics = blockchain.get_chain_metrics()
    return jsonify(metrics), 200

# Get event logs route
@app.route('/event_log', methods=['GET'])
def get_event_log():
    return jsonify(blockchain.event_log), 200

if __name__ == '__main__':
    print("Starting Flask server...")
    app.run(port=5000, debug=True)
