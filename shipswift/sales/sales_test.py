import pytest 
import sys, os
from flask import Flask, blueprints, request, jsonify

currentDir = os.path.dirname(os.path.realpath(__file__))
connectorPath = os.path.join(currentDir, '..')
sys.path.append(connectorPath)

import routes

app = Flask(__name__)
app.register_blueprint(routes.customers_bp, url_prefix="/api/routes")




@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_add_product(client):
    rv = client.post("/api/routes/add", json={'user': "user", 'item': "item", 'count': 1, 'price': 1, 'date': "date"})
    assert rv.status_code == 200  # Assuming a successful response status code
    assert rv.get_json() == {"message": "Product added successfully"}