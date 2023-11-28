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
    rv = client.post("/api/customers/register", json={'username': 'username', 'password': 'password', 'fullName':'fullName', 'address':'address', 'gender':'gender', 'maritalStatus':'maritalStatus', 'wallet':'wallet'})
    assert rv.get_json() == {"message": "Customer registered successfully"}

def test_delete_customer(client):
    rv = client.delete('/delete', json={'username': 'username'})
    assert rv.get_json() == {"message": "Customer username deleted"}

def test_update_customer(client):
    rv = client.put('/update', json={'username': 'username', 'new_data': 'new_data'})
    assert rv.get_json() == {"message": "Customer username updated"}

def test_get_customer(client):
    rv = client.get('/get', json={'username': 'username'})
    assert rv.get_json() == {"message": "Customer username"}

def test_get_customers():
    assert routes.get_customers() == {"message": "Customers"}

def test_charge_wallet():
    assert routes.charge_wallet("username") == {"message": "Wallet charged with amount successfully"}

def test_pay_wallet():
    assert routes.pay_wallet("username") == {"message": "Wallet paid amount successfully"}

