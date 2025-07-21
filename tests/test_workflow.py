import pytest
from app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_register_customer(client):
    response = client.post('/workflow/register', json={
        'name': 'Alice',
        'email': 'alice@example.com'
    })
    assert response.status_code == 201
    assert 'customer_id' in response.get_json()


def test_open_account_invalid_customer(client):
    response = client.post('/workflow/account', json={
        'customer_id': 'non-existent'
    })
    assert response.status_code == 404


def test_create_deposit_invalid_amount(client):
    response = client.post('/workflow/deposit', json={
        'account_id': 'non-existent',
        'amount': -100
    })
    assert response.status_code in [400, 404]


def test_create_payment_insufficient_funds(client):
    reg = client.post('/workflow/register', json={'name': 'Bob', 'email': 'bob@example.com'}).get_json()
    customer_id = reg['customer_id']
    acc = client.post('/workflow/account', json={'customer_id': customer_id}).get_json()
    account_id = acc['account_id']

    response = client.post('/workflow/payment', json={
        'account_id': account_id,
        'amount': 1000,
        'beneficiary_iban': 'FR123456'
    })
    assert response.status_code == 400
