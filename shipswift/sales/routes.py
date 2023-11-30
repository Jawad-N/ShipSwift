# customers/routes.py
from flask import Blueprint, request, jsonify
import sys, os
from datetime import datetime

currentDir = os.path.dirname(os.path.realpath(__file__))
connectorPath = os.path.join(currentDir, "..", "..")
print(connectorPath)
sys.path.append(connectorPath)

from DB.dbSalesf import *

salesbp = Blueprint("sales", __name__)



def getUser(user):
    #user is the username
    #function returns corresponding user in a dictionary if there exist a user with that name, and false o.w.
    1 == 1

def getItem(item):
    #item is the item name
    #function returns corresponding item in a dictionary if there exist an item with such a name, and false o.w.
    1==1

@salesbp.route("/transaction", methods=["POST"])
def add_product():

    data = request.get_json()
    user = data["user"]
    item = data["item"]
    count = data["count"]
    #Our Transaction requires the parameters:
    #User who wants to make the transaction defined by their username
    #The item he wants to buy
    #The number of units that he wants to buy 
    #Also we will mark the transaction date
    x = getUser(user)
    #apicall_inventory = "http://$IP_inventory:5001/api/"
    #apicall_users = "http://$IP_users:5000/api/" #TODO
    if(x == False): return jsonify({"message": "Mentioned User does not exist"})
    y = getItem(item)
    if( y == False ): return jsonify({"message": "Mentioned item does not exist"})
    addPurchase(user, item, count)
    return jsonify({"message": "Purchase added successfully"})







