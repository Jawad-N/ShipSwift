# inventory/routes.py
from flask import Blueprint, request, jsonify
import sys

sys.path.append("..")
import DB.dbInventoryf as dbInventory

inventory_bp = Blueprint("inventory", __name__)

@inventory_bp.route("/add", methods=["POST"])
def add_product():
    data = request.get_json()
    name = data["name"]
    category = data["category"]
    price = data["price"]
    description = data["description"]
    quantity = data["count"]
    dbInventory.add(name, category, price, description, quantity)
    return jsonify({"message": "Product added successfully"})

@inventory_bp.route("/update/<name>", methods=["PUT"])
def update_product(name):
    data = request.get_json()
    dbInventory.updateItem(name, data)
    return jsonify({"message": f"Product {productID} updated"})

@inventory_bp.route("/deduce/<name>", methods=["DELETE"])
def deduce_product(name):
    data = request.get_json()
    value = data["quantity"] - 1
    dbInventory.deduce(name, value)
    return jsonify({"message": f"Product {name} deducted by 1"})

@inventory_bp.route("/get/<name>", methods=["GET"])
def get_product(name):
    product = dbInventory.retrieve(name)
    if product:
        return jsonify(product)
    else:
        return jsonify({"message": "Product not found"}), 404
