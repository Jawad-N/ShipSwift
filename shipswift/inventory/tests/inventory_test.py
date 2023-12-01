import pytest 
import sys, os
from flask import Flask, blueprints, request, jsonify

currentDir = os.path.dirname(os.path.realpath(__file__))
connectorPath = os.path.join(currentDir, '..')
sys.path.append(connectorPath)

import routes

app = Flask(__name__)
app.register_blueprint(routes.inventory_bp, url_prefix="/api/inventory")




@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_add_product(client):
    client.delete("/api/inventory/delete")
    rv = client.post("/api/inventory/add", json={'name': 'test_product', 'category': 'test_category', 'price': 10.99, 'description': 'Test product description', 'count': 50})
    assert rv.status_code == 200  # Assuming a successful response status code
    assert rv.get_json() == {"message": "Product added successfully"}
    rv1 = client.post("/api/inventory/add", json={'name': 'test_product', 'category': 'test_category', 'price': 10.99, 'description': 'Test product description', 'count': 50})
    assert rv1.status_code == 200  # Assuming a successful response status code
    assert rv1.get_json() == {"message": "Product with name = test_product already in DB"}
    client.delete("/api/inventory/delete/test_product")

def test_update_product(client):
    #Succesful update 
    rv = client.post("/api/inventory/add", json={'name': 'test_product_update', 'category': 'test_category', 'price': 10.99, 'description': 'Test product description', 'count': 50})
    rv1 = client.put("/api/inventory/update/test_product_update", json={'name': 'test_product_update', 'category': 'test_category_updated', 'price': 10.99, 'description': 'Test product description', 'count': 50})
    assert rv1.status_code == 200  # Assuming a successful response status code
    assert rv1.get_json() == {"message": "Product  updated"}

    #No item with id name
    rv2 = client.put("/api/inventory/update/test_product1", json={'name': 'test_product2', 'category': 'test_category', 'price': 10.99, 'description': 'Test product description', 'count': 50})
    assert rv2.status_code == 200  # Assuming a successful response status code
    assert rv2.get_json() == {"message": "NO ITEM WITH NAME test_product1"}

    #New name is already used
    rv3 = client.post("/api/inventory/add", json={'name': 'test_product_unused', 'category': 'test_category', 'price': 10.99, 'description': 'Test product description', 'count': 50})
    rv4 = client.put("/api/inventory/update/test_product_unused", json={'name': 'test_product_update', 'category': 'test_category', 'price': 10.99, 'description': 'Test product description', 'count': 50})
    assert rv4.status_code == 200  # Assuming a successful response status code
    assert rv4.get_json() == {"message": "new Product Name is already Used"}

    client.delete("/api/inventory/delete/test_product_update")
def test_deduce_product(client):
    #item does not exist 
    rv = client.put("/api/inventory/deduce/test_product_not_exist")
    assert rv.status_code == 200  # Assuming a successful response status code
    assert rv.get_json() == {"message": "Item test_product_not_exist Does Not Exist"}

    #item exist but count = 0
    rv1 = client.post("/api/inventory/add", json={'name': 'test_product_deduce', 'category': 'test_category', 'price': 10.99, 'description': 'Test product description', 'count': 0})
    rv2 = client.put("/api/inventory/deduce/test_product_deduce")
    assert rv2.status_code == 200  # Assuming a successful response status code
    assert rv2.get_json() == {"message": "The stock of test_product_deduce is empty"}
    client.delete("/api/inventory/delete/test_product_deduce")

    #item exist and count > 0
    rv3 = client.post("/api/inventory/add", json={'name': 'test_product_deduce2', 'category': 'test_category', 'price': 10.99, 'description': 'Test product description', 'count': 50})
    rv4 = client.put("/api/inventory/deduce/test_product_deduce2")
    assert rv4.status_code == 200  # Assuming a successful response status code
    assert rv4.get_json() == {"message": "The stock of test_product_deduce2 is decreased by 1"}
    client.delete("/api/inventory/delete/test_product_deduce2")