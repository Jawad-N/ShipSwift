import pytest 
import sys, os
from flask import Flask, blueprints, request, jsonify

currentDir = os.path.dirname(os.path.realpath(__file__))
connectorPath = os.path.join(currentDir, '..')
sys.path.append(connectorPath)

import routes

app = Flask(__name__)
app.register_blueprint(routes.customers_bp, url_prefix="/api/customers")




@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_register_customer(client):
    rv_del = client.delete("/api/customers/reset")
    assert rv_del.get_json() == {"message":"Table has been emptied"}
    rv = client.post("/api/customers/register", json={'username': 'username1', 'password': 'password', 'fullName':'fullName', 'address':'address', 'gender':'gender', 'maritalStatus':'maritalStatus', 'wallet':0})
    assert rv.get_json() == {"message": "Customer registered successfully"}
    client.delete("/api/customers/delete/username1")

def test_delete_customer(client):
    rv1 = client.post("/api/customers/register", json={'username': 'username2', 'password': 'password', 'fullName':'fullName', 'address':'address', 'gender':'gender', 'maritalStatus':'maritalStatus', 'wallet':0})
    rv2 = client.delete('/api/customers/delete/username2')
    assert rv2.get_json() == {"message": "Customer username2 deleted"}


def test_update_customer(client):
    rv1 = client.post("/api/customers/register", json={'username': 'username_for_update', 'password': 'password', 'fullName':'fullName', 'address':'address', 'gender':'gender', 'maritalStatus':'maritalStatus', 'wallet':0})
    rv = client.post('/api/customers/update/username_for_update', json={'username': 'username_updated', 'password': 'password2', 'fullName':'fullName', 'address':'address', 'gender':'gender', 'maritalStatus':'maritalStatus', 'wallet':0})
    assert rv.get_json() == {"message": "Customer username_for_update updated"}
    client.delete("/api/customers/delete/username_updated")

def test_get_customer(client):
    rv1 = client.post("/api/customers/register", json={'username': 'username_for_get', 'password': 'password', 'fullName':'fullName', 'address':'address', 'gender':'gender', 'maritalStatus':'maritalStatus', 'wallet':0})
    rv = client.get('/api/customers/get/username_for_get')
    expected_keys = ["id", "username", "password", "fullName", "Address", "Gender", "maritalStatus", "wallet"]
    assert all(key in rv.get_json() for key in expected_keys)
    assert rv.get_json()["username"] == "username_for_get"
    client.delete("/api/customers/delete/username_for_get")

def test_get_customers(client):
    
    # Register some customers for testing
    client.post("/api/customers/register", json={'username': 'user1', 'password': 'password1', 'fullName':'fullName1', 'address':'address1', 'gender':'gender1', 'maritalStatus':'maritalStatus1', 'wallet':0})
    client.post("/api/customers/register", json={'username': 'user2', 'password': 'password2', 'fullName':'fullName2', 'address':'address2', 'gender':'gender2', 'maritalStatus':'maritalStatus2', 'wallet':0})

    # Make a request to get_customers endpoint
    rv = client.get('/api/customers/get')

    # Assert the response
    assert rv.status_code == 200  
    expected_keys = ["user1", "user2"]  
    response_data = rv.get_json()

    for username in expected_keys:
        assert username in response_data
        assert all(key in response_data[username] for key in ["username", "password", "fullName", "Address", "Gender", "maritalStatus", "wallet"])

    client.delete("/api/customers/delete/user1")
    client.delete("/api/customers/delete/user2")

def test_charge_wallet(client):
    # Register a customer for testing
    client.post("/api/customers/register", json={'username': 'charge_test_user', 'password': 'password', 'fullName':'fullName', 'address':'address', 'gender':'gender', 'maritalStatus':'maritalStatus', 'wallet':100})

    # Make a request to charge_wallet endpoint
    rv = client.post('/api/customers/charge/charge_test_user', json={'amount': 50})

    # Assert the response
    assert rv.status_code == 200  # Assuming a successful response status code
    assert rv.get_json() == {"message": "Wallet charged with 50 successfully"}
    client.delete("/api/customers/delete/charge_test_user")

def test_pay_wallet(client):
    # Register a customer for testing
    client.post("/api/customers/register", json={'username': 'pay_wallet_user', 'password': 'password', 'fullName':'fullName', 'address':'address', 'gender':'gender', 'maritalStatus':'maritalStatus', 'wallet':100})
    # Assuming pay_wallet updates the wallet and returns a message
    rv = client.post('/api/customers/pay/pay_wallet_user', json={'amount': 50})

    # Assert the expected outcome based on your implementation
    assert rv.get_json() == {"message": "Wallet paid 50 successfully"}
    
    rv1 = client.post('/api/customers/pay/pay_wallet_user', json={'amount': 150})
    assert rv1.get_json() == {"message": "NOT ENOUGH CREDIT"}
    client.delete("/api/customers/delete/pay_wallet_user")

