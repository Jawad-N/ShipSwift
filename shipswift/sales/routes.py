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
    """
    Endpoint to add a new transaction.

    This route handles POST requests to add a new transaction. The transaction involves a user making a purchase of a specific item with a specified quantity.

    **Method:** POST

    **URL:** `/api/sales/transaction`

    **Parameters:**
    - `user` (str): The username of the user making the transaction.
    - `item` (str): The name of the item being purchased.
    - `count` (int): The quantity of units being purchased.

    **Returns:**
    - If the user does not exist, returns a JSON response with a failure message:
      ```json
      {"message": "User Does Not Exist"}
      ```

    - If the item is not found, returns a JSON response with a failure message:
      ```json
      {"message": "Item not found"}
      ```

    - If the user has insufficient balance, returns a JSON response with a failure message:
      ```json
      {"message": "Insufficient Balance with user <username>"}
      ```

    - If there is insufficient stock for the item, returns a JSON response with a failure message:
      ```json
      {"message": "Insufficient stock for item <item>"}
      ```

    - If the transaction is successful, returns a JSON response with a success message:
      ```json
      {"message": "Purchase added successfully"}
      ```

    **Example Usage (Postman):**
    - Method: POST
    - URL: `http://your-api-base-url/api/sales/transaction`
    - Body (JSON):
      ```json
      {
        "user": "username",
        "item": "item_name",
        "count": 2
      }
      ```

    - Expected Response (User Does Not Exist):
      ```json
      {"message": "User Does Not Exist"}
      ```

    - Expected Response (Item not found):
      ```json
      {"message": "Item not found"}
      ```

    - Expected Response (Insufficient Balance):
      ```json
      {"message": "Insufficient Balance with user <username>"}
      ```

    - Expected Response (Insufficient Stock):
      ```json
      {"message": "Insufficient stock for item <item>"}
      ```

    - Expected Response (Purchase added successfully):
      ```json
      {"message": "Purchase added successfully"}
      ```

    **Note:**
    - This endpoint communicates with other services using their respective APIs to perform actions such as checking user details, retrieving item information, updating user wallets, and updating item stock.

    **Testing:**
    - This endpoint has been tested using Postman.
    """
    
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
    """
    Endpoint to retrieve a list of available goods.

    This route handles GET requests to retrieve a list of available goods. The list includes details about each item, such as name, category, price, description, and quantity.

    **Method:** GET

    **URL:** `/api/sales/list`

    **Parameters:**
    None

    **Returns:**
    - If successful, returns a JSON response with the list of goods.
    - If there is an error from the database, returns a JSON response with a failure message:
      ```json
      {"message": "Error from DB"}
      ```

    **Example Usage (Postman):**
    - Method: GET
    - URL: `http://your-api-base-url/api/sales/list`

    - Expected Response (Successful):
      ```json
      [
        {
          "name": "item1",
          "category": "category1",
          "price": 10.99,
          "description": "Description of item1",
          "quantity": 50
        },
        {
          "name": "item2",
          "category": "category2",
          "price": 19.99,
          "description": "Description of item2",
          "quantity": 30
        },
        ...
      ]
      ```

    - Expected Response (Error from DB):
      ```json
      {"message": "Error from DB"}
      ```

    **Note:**
    - This endpoint retrieves the list of goods from the database and returns it as a JSON response.

    **Testing:**
    - This endpoint has been tested using Postman.
    """
    D = listItems()
    if(D == False): return jsonify({"message": "Error from DB"})
    else:
        return jsonify(D)


@salesbp.route('/list/<good>', methods = ["GET"])
def getGood(good):
    """
    Endpoint to retrieve details about a specific good.

    This route handles GET requests to retrieve details about a specific good identified by its name.

    **Method:** GET

    **URL:** `/api/sales/list/{good}`

    **Parameters:**
    - `good` (str): The name of the good for which details are requested.

    **Returns:**
    - If successful, returns a JSON response with details about the specified good.
    - If there is an error from the database or the good is not found, returns a JSON response with a failure message:
      ```json
      {"message": "ERROR FROM DB"}
      ```

    **Example Usage (Postman):**
    - Method: GET
    - URL: `http://your-api-base-url/api/sales/list/item1`

    - Expected Response (Successful):
      ```json
      {
        "name": "item1",
        "category": "category1",
        "price": 10.99,
        "description": "Description of item1",
        "quantity": 50
      }
      ```

    - Expected Response (Error from DB or Good Not Found):
      ```json
      {"message": "ERROR FROM DB"}
      ```

    **Note:**
    - This endpoint retrieves details about a specific good from the database and returns it as a JSON response.

    **Testing:**
    - This endpoint has been tested using Postman.
    """
    D = listItem(good)
    if(D == False): return jsonify({"message": "ERROR FROM DB"})
    else:
        return jsonify(D)

@salesbp.route('/history/<user>', methods = ["GET"])
def History(user):
    """
    Endpoint to retrieve transaction history for a specific user.

    This route handles GET requests to retrieve the transaction history for a specific user identified by their username.

    **Method:** GET

    **URL:** `/api/sales/history/{user}`

    **Parameters:**
    - `user` (str): The username of the user for whom the transaction history is requested.

    **Returns:**
    - If successful and the user has transaction history, returns a JSON response with the user's transaction history.
    - If there is an error from the database, the user does not exist, or the user has no transactions, returns a JSON response with an appropriate message:
      ```json
      {"message": "ERROR FROM DB"}
      ```

    **Example Usage (Postman):**
    - Method: GET
    - URL: `http://your-api-base-url/api/sales/history/username`

    - Expected Response (Successful with History):
      ```json
      [
        {
          "transaction_id": 1,
          "user": "username",
          "item": "item1",
          "count": 2,
          "price_per_unit": 10.99,
          "transaction_date": "2023-12-01 12:30:45"
        },
        {
          "transaction_id": 2,
          "user": "username",
          "item": "item2",
          "count": 3,
          "price_per_unit": 19.99,
          "transaction_date": "2023-12-02 14:45:30"
        },
        ...
      ]
      ```

    - Expected Response (Error from DB or User Not Found or No Transactions):
      ```json
      {"message": "ERROR FROM DB"}
      ```

    **Note:**
    - This endpoint retrieves the transaction history for a specific user from the database and returns it as a JSON response.

    **Testing:**
    - This endpoint has been tested using Postman.
    """
    D = user_log(user)
    if(D == False): return jsonify({"message": "ERROR FROM DB"})
    else:
        if(D == {}): return jsonify({"message": "user did not make any transactions yet"})
        else: return jsonify(D)






