# customers/routes.py
from flask import Blueprint, request, jsonify
import sys, os
import json
import requests
currentDir = os.path.dirname(os.path.realpath(__file__))
connectorPath = os.path.join(currentDir, "..", "..")
print(connectorPath)
sys.path.append(connectorPath)

from DB.dbSalesf import *
salesbp = Blueprint("sales", __name__)


#Our Transaction requires the parameters:
#User who wants to make the transaction defined by their username
#The item he wants to buy
#The number of units that he wants to buy 
#Also we will mark the transaction date
# Last functionality communicate between dockers
@salesbp.route("/transaction", methods=["POST"])
def add_transaction():

    data = request.get_json()
    user = data["user"]
    item = data["item"]
    count = data["count"]

    
    apicall_getUser = f"http://127.0.0.3:5000/api/customers/get/{user}" #TODO
    response_getUser = requests.get(apicall_getUser).json() # Works!


    if response_getUser == {}: return jsonify({"message": "User Does Not Exist"}) #functional Error!

    apicall_getItem = f"http://127.0.0.4:5001/api/inventory/get/{item}"
    response_getItem = requests.get(apicall_getItem).json()
    print(response_getItem)
    if( "message" in response_getItem.keys() ): #functional Error!
        return jsonify({"message": "Item not found"})

    id = None
    for id_ in response_getItem.keys():
        id = id_ 

    #Here both item and guy are found, what remains before doing the transaction is checking that the user has enough and there's enough stock to do the transaction 
    if ( response_getUser["wallet"] < count * response_getItem[id]["price"] ):
        return jsonify({"message": f"Insufficient Balance with user {user}"})
    elif ( response_getItem[id]["count"] < count ):
        return jsonify({"message": f"Insufficient stock for item {item}"})

    # if we make it here then transaction can be made, we update the log
    addPurchase(user, item, count, response_getItem[id]["price"])
    apicall_updateWallet = f"http://127.0.0.3:5000/api/customers/pay/{user}"
    amount = count * response_getItem[id]["price"] 
    response_payUser = requests.post(apicall_updateWallet, json =  { "amount": amount }  )

    if ( response_payUser.json() != {"message": f"Wallet paid {amount} successfully"} ):
        return jsonify({"message": "Error Occured In payment"})
    

    apicall_updateStock = f"http://127.0.0.4:5001/api/inventory/deduce/{item}/{count}"
    response_deduceStock = requests.put(apicall_updateStock)

    if(response_deduceStock.json() != {"message": f"The stock of {item} is decreased by {count}"}):
        return jsonify({"message": "Error Occured in stock update"}) # This might lead to a synchronization problem since transactions are not atomic

    return jsonify( { "message": "Purchase added successfully" } )


@salesbp.route('/list', methods = ["GET"])
def getGoods():
    D = listItems()
    if(D == False): return jsonify({"message": "Error from DB"})
    else:
        return jsonify(D)


@salesbp.route('/list/<good>', methods = ["GET"])
def getGood(good):
    D = listItem(good)
    if(D == False): return jsonify({"message": "ERROR FROM DB"})
    else:
        return jsonify(D)

@salesbp.route('/history/<user>', methods = ["GET"])
def History(user):
    D = user_log(user)
    if(D == False): return jsonify({"message": "ERROR FROM DB"})
    else:
        if(D == {}): return jsonify({"message": "user did not make any transactions yet"})
        else: return jsonify(D)






