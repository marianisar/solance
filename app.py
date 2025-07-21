from flask import Flask, request, jsonify
from datetime import datetime
import uuid

app = Flask(__name__)

# In-memory storage for demonstration purposes
customers = {}
accounts = {}
transactions = []
payments = []


@app.route('/workflow/register', methods=['POST'])
def register_customer():
    data = request.get_json()
    if 'name' not in data or 'email' not in data:
        return jsonify({'error': 'Missing required fields'}), 400

    customer_id = str(uuid.uuid4())
    customers[customer_id] = {
        'name': data['name'],
        'email': data['email'],
        'created_at': datetime.utcnow().isoformat()
    }
    return jsonify({'status': 'success', 'customer_id': customer_id}), 201


@app.route('/workflow/account', methods=['POST'])
def open_account():
    data = request.get_json()
    customer_id = data.get('customer_id')
    if customer_id not in customers:
        return jsonify({'error': 'Customer not found'}), 404

    account_id = str(uuid.uuid4())
    accounts[account_id] = {
        'customer_id': customer_id,
        'currency': data.get('currency', 'EUR'),
        'balance': 0.0,
        'created_at': datetime.utcnow().isoformat()
    }
    return jsonify({'status': 'success', 'account_id': account_id}), 201


@app.route('/workflow/deposit', methods=['POST'])
def create_deposit():
    data = request.get_json()
    account_id = data.get('account_id')
    amount = data.get('amount')

    if account_id not in accounts:
        return jsonify({'error': 'Account not found'}), 404
    if not isinstance(amount, (int, float)) or amount <= 0:
        return jsonify({'error': 'Invalid amount'}), 400

    accounts[account_id]['balance'] += amount
    transactions.append({
        'account_id': account_id,
        'amount': amount,
        'type': 'deposit',
        'timestamp': datetime.utcnow().isoformat()
    })
    return jsonify({'status': 'success', 'new_balance': accounts[account_id]['balance']}), 200


@app.route('/workflow/payment', methods=['POST'])
def create_payment():
    data = request.get_json()
    account_id = data.get('account_id')
    amount = data.get('amount')
    beneficiary_iban = data.get('beneficiary_iban')

    if account_id not in accounts:
        return jsonify({'error': 'Account not found'}), 404
    if not isinstance(amount, (int, float)) or amount <= 0:
        return jsonify({'error': 'Invalid amount'}), 400
    if accounts[account_id]['balance'] < amount:
        return jsonify({'error': 'Insufficient funds'}), 400

    accounts[account_id]['balance'] -= amount
    payments.append({
        'account_id': account_id,
        'amount': amount,
        'beneficiary_iban': beneficiary_iban,
        'timestamp': datetime.utcnow().isoformat()
    })
    return jsonify({'status': 'success', 'new_balance': accounts[account_id]['balance']}), 200


@app.route('/workflow/messages', methods=['GET'])
def get_messages():
    return jsonify({
        'customers': customers,
        'accounts': accounts,
        'transactions': transactions,
        'payments': payments
    }), 200


if __name__ == '__main__':
    app.run(debug=True)
