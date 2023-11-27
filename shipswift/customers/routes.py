# customers/routes.py
from flask import Blueprint, request, jsonify
import sys, os

currentDir = os.path.dirname(os.path.realpath(__file__))
connectorPath = os.path.join(currentDir, "..", "..")
print(connectorPath)
sys.path.append(connectorPath)

from DB.dbCustomersf import * 


customers_bp = Blueprint("customers", __name__) #Is a way of organizing a group of related views and other code. 

#Tested Using Postman
@customers_bp.route("/register", methods=["GET", "POST"])
def register_customer():
    data = request.get_json()
    username = data["username"]
    password = data["password"]
    fullName = data["fullName"]
    address = data["address"]
    gender = data["gender"]
    maritalStatus = data["maritalStatus"]
    wallet = data["wallet"]
    try:
        registerCustomer(username, password, fullName, address, gender, maritalStatus, wallet)
        return jsonify({"message": "Customer registered successfully"})
    except:
        return jsonify({"message": "FAILURE IN REGISTRING"})


#Tested Using Postman
@customers_bp.route("/delete/<username>", methods=["DELETE"])
def delete_customer(username):
    try:
        D = getCustomer(username)
        if(len(D) == 0): return jsonify({"message": f"Customer {username} Not found"})
        deleteCustomer(username)
        return jsonify({"message": f"Customer {username} deleted"})
    except:
        return jsonify({"message": "FAILURE IN DELETE"})


#Tested Using Postman
@customers_bp.route("/update/<username>", methods=["POST"])
def update_customer(username):
    D = getCustomer(username)
    if(len(D) == 0): return jsonify({"message": f"Customer {username} Not found"})
    data = request.get_json()
    print(data)
    updateCustomer(username, data)

    return jsonify({"message": f"Customer {username} updated"})


#Tested Using Postman
@customers_bp.route("/get/<username>", methods=["GET"])
def get_customer(username):
    return jsonify(getCustomer(username))


#Tested Using Postman
@customers_bp.route("/get", methods=["GET"])
def get_customers():
    return jsonify(getCustomers())

#Tested Using Postman
@customers_bp.route("/charge/<username>", methods=["POST"])
def charge_wallet(username):
    data = request.get_json()
    amount = data["amount"]
    print(amount, username)
    try:
        chargeCustomer(username, amount)
        return jsonify({"message": f"Wallet charged with {amount} successfully"})
    except: 
        return jsonify({"message": f"FAILURE IN CHARGE"})

#Tested Using Postman
@customers_bp.route("/pay/<username>", methods=["POST"])
def pay_wallet(username):
    data = request.get_json()
    amount = data["amount"]
    try:
        if(deduceCustomer(username, amount)): return jsonify({"message": f"Wallet paid {amount} successfully"})
        else: return jsonify({"message": "NOT ENOUGH CREDIT"})
    except:
        return jsonify({"message": f"FAILURE IN PAY"})
