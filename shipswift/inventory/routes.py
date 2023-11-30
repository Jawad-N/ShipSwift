#Inventory routes
from flask import Blueprint, request, jsonify
import sys, os
"""
currentDir = os.path.dirname(os.path.realpath(__file__))
connectorPath = os.path.join(currentDir, "..", "..")
print(connectorPath)
sys.path.append(connectorPath)
"""
from DB.dbInventoryf import * 


inventory_bp = Blueprint("inventory", __name__)


#Tested Using Postman
@inventory_bp.route("/add", methods=["POST"])
def add_product():
    data = request.get_json()
    name = data["name"]
    category = data["category"]
    price = data["price"]
    description = data["description"]
    quantity = data["count"]
    flag = add(name, category, price, description, quantity)
    if(flag == 0):
        return jsonify({"message": f"Product with name = {name} already in DB"})
    elif(flag == 1):
        return jsonify({"message": "Product added successfully"})
    elif (flag == 2):
        return jsonify({"message": "FAILURE IN DATABASE"})
    


#Tested Using Postman
@inventory_bp.route("/update/<name>", methods=["PUT"])
def update_product(name):
    data = request.get_json()
    print(data)
    x = updateItem(name, data)
    print(x)
    if (x == 0): return jsonify({"message": f"NO ITEM WITH NAME {name}"})
    elif (x == 1): return jsonify({"message": f"Product  updated"})
    elif (x == 2): return jsonify({"message": f"new Product Name is already Used"})
    else: return jsonify({"message": "DB ERROR"})





#Tested using postman
@inventory_bp.route("/deduce/<name>", methods=["PUT"])
def deduce_product(name):
    x = deduce(name)
    if(x == 0): return jsonify({"message": f"Item {name} Does Not Exist"})
    elif( x == 1 ): return jsonify({"message": f"The stock of {name} is empty"})
    elif( x == 2 ): return jsonify({"message": f"The stock of {name} is decreased by 1"})
    else: return jsonify({"message": "DB ERROR"})

#deduce custom number 
#Tested using postman
@inventory_bp.route("/deduce/<name>/<val>", methods=["PUT"])
def deduce_product2(name,val):
    print(name, val)
    try:
        val = int(val)
    except:
        return "URL DNE"
    x = deduce2(name,val)
    if(x == 0): return jsonify({"message": f"Item {name} Does Not Exist"})
    elif( x == 1 ): return jsonify({"message": f"The stock of {name} is empty"})
    elif( x == 2 ): return jsonify({"message": f"The stock of {name} is decreased by {val}"})
    else: return jsonify({"message": "DB ERROR"})

#Tested Using Postman
@inventory_bp.route("/get/<name>", methods=["GET"])
def get_product(name):
    #The product is not unique by name, thus might display multiple items
    product = retrieve(name)
    if(product == False): return jsonify({"message": f"FAILURE IN DB"})
    else:
        if(len(product) == 0): return jsonify({"message": "Product not found"}), 404
        else: return jsonify(product)
    
#Tested Using Postman
@inventory_bp.route("/get", methods = ["GET"])
def get_products():
    D = display()
    if(D == False): return jsonify({"message": "FAILURE IN DISPLAYING INVENTORY"})
    else: return jsonify(D)
    
