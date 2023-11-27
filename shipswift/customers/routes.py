# customers/routes.py
from flask import Blueprint, request, jsonify
import sys

sys.path.append("..")
import DB.dbCustomersf as dbCustomers


customers_bp = Blueprint("customers", __name__) #Is a way of organizing a group of related views and other code. 

@customers_bp.route("/register", methods=["POST"])
def register_customer():
    data = request.get_json()
    username = data["username"]
    password = data["password"]
    fullName = data["fullName"]
    address = data["address"]
    gender = data["gender"]
    maritalStatus = data["maritalStatus"]
    wallet = data["wallet"]
    dbCustomers.registerCustomer(username, password, fullName, address, gender, maritalStatus, wallet)
    return jsonify({"message": "Customer registered successfully"})

@customers_bp.route("/delete/<username>", methods=["DELETE"])
def delete_customer(username):
    dbCustomers.deleteCustomer(username)
    return jsonify({"message": f"Customer {username} deleted"})

@customers_bp.route("/update/<username>", methods=["PUT"])
def update_customer(username):
    data = request.get_json()
    dbCustomers.updateCustomer(username, data)
    return jsonify({"message": f"Customer {username} updated"})

@customers_bp.route("/get/<username>", methods=["GET"])
def get_customer(username):
    return jsonify(dbCustomers.getCustomer(username))

@customers_bp.route("/get", methods=["GET"])
def get_customers():
    return jsonify(dbCustomers.getCustomers())

@customers_bp.route("/charge/<username>", methods=["POST"])
def charge_wallet(username):
    data = request.get_json()
    amount = data["amount"]
    dbCustomers.chargeWallet(username, amount)
    return jsonify({"message": f"Wallet charged with {amount} successfully"})

@customers_bp.route("/pay/<username>", methods=["POST"])
def pay_wallet(username):
    data = request.get_json()
    amount = data["amount"]
    dbCustomers.payWallet(username, amount)
    return jsonify({"message": f"Wallet paid {amount} successfully"})
