import pytest 
import sys, os
from flask import Flask, blueprints, request, jsonify

currentDir = os.path.dirname(os.path.realpath(__file__))
connectorPath = os.path.join(currentDir, '..')
sys.path.append(connectorPath)

import routes

app = Flask(__name__)
app.register_blueprint(routes.customers_bp, url_prefix="/api/inventory")




@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_add_product(client):
    #successful add
    rv = client.post("/")
    rv2 = client.post("/api/inventory/add", json={'user': "user", 'item': "item", 'count': 1, 'date': "date"})
    assert rv.status_code == 200  # Assuming a successful response status code
    assert rv.get_json() == {"message": "Purchase added successfully"}

    #user does not exist
