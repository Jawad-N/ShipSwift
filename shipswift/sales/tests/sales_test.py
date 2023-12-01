import pytest 
import sys, os
from flask import Flask, blueprints, request, jsonify

currentDir = os.path.dirname(os.path.realpath(__file__))
connectorPath = os.path.join(currentDir, '..')
sys.path.append(connectorPath)

import routes

app = Flask(__name__)
app.register_blueprint(routes.salesbp, url_prefix="/api/sales")


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_add_transaction(client):
    # Assuming some setup for test data or clearing existing data
    rv_del = client.delete("/api/sales/reset")
    assert rv_del.get_json() == {"message": "Table has been emptied"}

    # Assuming an item and user exist for testing
    client.post("/api/customers/register", json={'username': 'test_user', 'password': 'password', 'fullName':'fullName', 'address':'address', 'gender':'gender', 'maritalStatus':'maritalStatus', 'wallet':100})
    client.post("/api/inventory/add", json={'name': 'item1', 'category': 'category1', 'price': 10.99, 'description': 'Description of item1', 'count': 1})  # Note: Limited stock for testing

    # Making a request to add_transaction endpoint with insufficient balance
    rv_insufficient_balance = client.post('/api/sales/transaction', json={'user': 'test_user', 'item': 'item1', 'count': 20})
    assert rv_insufficient_balance.get_json() == {"message": "Insufficient Balance with user test_user"}

    # Making a request to add_transaction endpoint with insufficient stock
    rv_insufficient_stock = client.post('/api/sales/transaction', json={'user': 'test_user', 'item': 'item1', 'count': 2})
    assert rv_insufficient_stock.get_json() == {"message": "Insufficient stock for item item1"}

    # Making a request to add_transaction endpoint with a non-existing user
    rv_non_existing_user = client.post('/api/sales/transaction', json={'user': 'non_existing_user', 'item': 'item1', 'count': 1})
    assert rv_non_existing_user.get_json() == {"message": "User Does Not Exist"}

    # Making a request to add_transaction endpoint with a non-existing item
    rv_non_existing_item = client.post('/api/sales/transaction', json={'user': 'test_user', 'item': 'non_existing_item', 'count': 1})
    assert rv_non_existing_item.get_json() == {"message": "Item not found"}

    # Making a request to add_transaction endpoint with a successful transaction
    rv_successful_transaction = client.post('/api/sales/transaction', json={'user': 'test_user', 'item': 'item1', 'count': 1})
    assert rv_successful_transaction.get_json() == {"message": "Purchase added successfully"}

    # Cleanup
    client.delete("/api/customers/delete/test_user")
    client.delete("/api/inventory/delete/item1")

def test_get_goods(client):
    # Assuming some setup for test data or clearing existing data
    rv_del = client.delete("/api/sales/reset")
    assert rv_del.get_json() == {"message": "Table has been emptied"}

    # Assuming some items exist for testing
    client.post("/api/inventory/add", json={'name': 'item1', 'category': 'category1', 'price': 10.99, 'description': 'Description of item1', 'count': 5})
    client.post("/api/inventory/add", json={'name': 'item2', 'category': 'category2', 'price': 19.99, 'description': 'Description of item2', 'count': 3})

    # Making a request to get_goods endpoint
    rv = client.get('/api/sales/list')

    # Assert the response
    assert rv.status_code == 200
    expected_items = [
        {
            "name": "item1",
            "category": "category1",
            "price": 10.99,
            "description": "Description of item1",
            "quantity": 5
        },
        {
            "name": "item2",
            "category": "category2",
            "price": 19.99,
            "description": "Description of item2",
            "quantity": 3
        }
    ]
    response_data = rv.get_json()

    for item in expected_items:
        assert item in response_data
        assert all(key in response_data[item] for key in ["name", "category", "price", "description", "quantity"])

    # Cleanup
    client.delete("/api/inventory/delete/item1")
    client.delete("/api/inventory/delete/item2")


def test_get_good(client):
    # Assuming an item is added for testing
    client.post("/api/inventory/add", json={'name': 'item1', 'category': 'category1', 'price': 10.99, 'description': 'Description of item1', 'count': 30})

    # Making a request to get_good endpoint
    rv = client.get('/api/sales/list/item1')

    # Assert the response
    assert rv.status_code == 200  # Assuming a successful response status code
    assert isinstance(rv.get_json(), dict)

    # Cleanup
    client.delete("/api/inventory/delete/item1")

def test_history(client):
    # Assuming some setup for test data or clearing existing data
    rv_del = client.delete("/api/sales/reset")
    assert rv_del.get_json() == {"message": "Table has been emptied"}

    # Assuming a specific user exists for testing
    client.post("/api/customers/register", json={'username': 'test_user', 'password': 'password', 'fullName': 'Test User', 'address': 'Test Address', 'gender': 'Male', 'maritalStatus': 'Single', 'wallet': 100})

    # Making a request to history endpoint for a user with no transactions
    rv_empty = client.get('/api/sales/history/test_user')
    assert rv_empty.status_code == 200
    assert rv_empty.get_json() == {"message": "user did not make any transactions yet"}

    # Assuming a transaction history exists for a user
    client.post("/api/sales/transaction", json={'user': 'test_user', 'item': 'test_item', 'count': 2})

    # Making a request to history endpoint for a user with transactions
    rv_with_history = client.get('/api/sales/history/test_user')
    assert rv_with_history.status_code == 200
    assert isinstance(rv_with_history.get_json(), list)

    # Clean up after the test
    client.delete("/api/sales/reset")
    client.delete("/api/customers/delete/test_user")
