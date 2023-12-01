"""jawad"""
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
@customers_bp.route("/register", methods=["POST"])
def register_customer():
    """
    Endpoint to register a new customer.

    This route handles POST requests for customer registration, where a new customer is registered based on the provided JSON data.

    **Method:** POST

    **URL:** `/api/customers/register`

    **Parameters (JSON):**
    - `username` (str): The username for the new customer.
    - `password` (str): The password for the new customer.
    - `fullName` (str): The full name of the new customer.
    - `address` (str): The address of the new customer.
    - `gender` (str): The gender of the new customer.
    - `maritalStatus` (str): The marital status of the new customer.
    - `wallet` (float): The initial wallet balance for the new customer.

    **Returns:**
    - If the registration is successful, returns a JSON response with a success message:
      ```json
      {"message": "Customer registered successfully"}
      ```

    - If there's an error during registration, returns a JSON response with a failure message:
      ```json
      {"message": "FAILURE IN REGISTRATION"}
      ```

    **Testing:**
    - This endpoint has been tested using Postman.

    **Example Usage (Postman):**
    - Method: POST
    - URL: `http://your-api-base-url/api/customers/register`
    - Body (JSON):
      ```json
      {
        "username": "new_user",
        "password": "secure_password",
        "fullName": "John Doe",
        "address": "123 Main St",
        "gender": "Male",
        "maritalStatus": "Single",
        "wallet": 100.0
      }
      ```

    - Expected Response (Success):
      ```json
      {"message": "Customer registered successfully"}
      ```

    - Expected Response (Failure):
      ```json
      {"message": "FAILURE IN REGISTRATION"}
      ```
    """
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
    """
    Endpoint to delete a customer.

    This route handles DELETE requests to delete a customer based on the provided username parameter.

    **Method:** DELETE

    **URL:** `/api/customers/delete/<username>`

    **Parameters:**
    - `username` (str): The username of the customer to be deleted.

    **Returns:**
    - If the customer is found and successfully deleted, returns a JSON response with a success message:
      ```json
      {"message": "Customer deleted successfully"}
      ```

    - If the customer is not found, returns a JSON response indicating that the customer was not found:
      ```json
      {"message": "Customer not found"}
      ```

    - If there's an error during the deletion process, returns a JSON response with a failure message:
      ```json
      {"message": "FAILURE IN DELETE"}
      ```

    **Testing:**
    - This endpoint has been tested using Postman.

    **Example Usage (Postman):**
    - Method: DELETE
    - URL: `http://your-api-base-url/api/customers/delete/<username>`

    - Expected Response (Success):
      ```json
      {"message": "Customer deleted successfully"}
      ```

    - Expected Response (Customer Not Found):
      ```json
      {"message": "Customer not found"}
      ```

    - Expected Response (Failure):
      ```json
      {"message": "FAILURE IN DELETE"}
      ```
    """
    try:
        D = getCustomer(username)
        if(len(D) == 0): return jsonify({"message": f"Customer {username} Not found"})
        deleteCustomer(username)
        return jsonify({"message": f"Customer {username} deleted"})
    except:
        return jsonify({"message": "FAILURE IN DELETE"})


#Tested Using Postman
@customers_bp.route("/update/<username>", methods=["POST", "PUT"])
def update_customer(username):
    """
    Endpoint to update customer information.

    This route handles POST and PUT requests to update customer information based on the provided username parameter.

    **Methods:** POST, PUT

    **URL:** `/api/customers/update/<username>`

    **Parameters:**
    - `username` (str): The username of the customer to be updated.

    **Request Data (JSON):**
    - `username` (str, optional): The new username for the customer.
    - `password` (str, optional): The new password for the customer.
    - `fullName` (str, optional): The new full name for the customer.
    - `address` (str, optional): The new address for the customer.
    - `gender` (str, optional): The new gender for the customer.
    - `maritalStatus` (str, optional): The new marital status for the customer.
    - `wallet` (float, optional): The new wallet balance for the customer.

    **Returns:**
    - If the customer is found and successfully updated, returns a JSON response with a success message:
      ```json
      {"message": "Customer updated successfully"}
      ```

    - If the customer is not found, returns a JSON response indicating that the customer was not found:
      ```json
      {"message": "Customer not found"}
      ```

    **Testing:**
    - This endpoint has been tested using Postman.

    **Example Usage (Postman):**
    - Method: POST or PUT
    - URL: `http://your-api-base-url/api/customers/update/<username>`
    - Body (JSON):
      ```json
      {
        "password": "new_password",
        "address": "new_address",
        "gender": "new_gender",
        "maritalStatus": "new_marital_status",
        "wallet": 150.0
      }
      ```

    - Expected Response (Success):
      ```json
      {"message": "Customer updated successfully"}
      ```

    - Expected Response (Customer Not Found):
      ```json
      {"message": "Customer not found"}
      ```
    """
    D = getCustomer(username)
    if(len(D) == 0): return jsonify({"message": f"Customer {username} Not found"})
    data = request.get_json()
    updateCustomer(username, data)

    return jsonify({"message": f"Customer {username} updated"})


#Tested Using Postman
@customers_bp.route("/get/<username>", methods=["GET"])
def get_customer(username):
    """
    Endpoint to retrieve customer information.

    This route handles GET requests to retrieve information about a customer based on the provided username parameter.

    **Method:** GET

    **URL:** `/api/customers/get/<username>`

    **Parameters:**
    - `username` (str): The username of the customer to retrieve information for.

    **Returns:**
    - If the customer is found, returns a JSON response with the customer information.
    - If the customer is not found, returns a JSON response indicating that the customer was not found.

    **Example Usage (Postman):**
    - Method: GET
    - URL: `http://your-api-base-url/api/customers/get/<username>`

    - Expected Response (Success):
      ```json
      {
        "id": 1,
        "username": "customer_username",
        "password": "customer_password",
        "fullName": "Customer Full Name",
        "address": "Customer Address",
        "gender": "Male",
        "maritalStatus": "Single",
        "wallet": 100.0
      }
      ```

    - Expected Response (Customer Not Found):
      ```json
      {"message": "Customer not found"}
      ```
    """
    return jsonify(getCustomer(username))

@customers_bp.route("/reset", methods=["DELETE"])
def reset_table():
    """
    Endpoint to reset the customer table.

    This route handles DELETE requests to reset the customer table, effectively deleting all customer records.

    **Method:** DELETE

    **URL:** `/api/customers/reset`

    **Returns:**
    - If the table is successfully reset, returns a JSON response with a success message:
      ```json
      {"message": "Table has been emptied"}
      ```

    - If there's an error during the reset process, returns a JSON response with a failure message:
      ```json
      {"message": "failure"}
      ```

    **Example Usage (Postman):**
    - Method: DELETE
    - URL: `http://your-api-base-url/api/customers/reset`

    - Expected Response (Success):
      ```json
      {"message": "Table has been emptied"}
      ```

    - Expected Response (Failure):
      ```json
      {"message": "failure"}
      ```

    **Testing:**
    - This endpoint has been tested using Postman.
    """
    try:
        deleteCustomers()
        return jsonify({"message":"Table has been emptied"})
    except:
        return jsonify({"message":"failure"})

#Tested Using Postman
@customers_bp.route("/get", methods=["GET"])
def get_customers():
    """
    Endpoint to retrieve all customers.

    This route handles GET requests to retrieve information about all customers in the database.

    **Method:** GET

    **URL:** `/api/customers/get`

    **Returns:**
    - If there are customers in the database, returns a JSON response with a list of customer information.
    - If there are no customers, returns a JSON response indicating that there are no customers.

    **Example Usage (Postman):**
    - Method: GET
    - URL: `http://your-api-base-url/api/customers/get`

    - Expected Response (Success):
      ```json
      [
        {
          "id": 1,
          "username": "customer_username_1",
          "password": "customer_password_1",
          "fullName": "Customer Full Name 1",
          "address": "Customer Address 1",
          "gender": "Male",
          "maritalStatus": "Single",
          "wallet": 100.0
        },
        {
          "id": 2,
          "username": "customer_username_2",
          "password": "customer_password_2",
          "fullName": "Customer Full Name 2",
          "address": "Customer Address 2",
          "gender": "Female",
          "maritalStatus": "Married",
          "wallet": 150.0
        },
        ...
      ]
      ```

    - Expected Response (No Customers):
      ```json
      {"message": "No customers found"}
      ```

    **Testing:**
    - This endpoint has been tested using Postman.
    """
    return jsonify(getCustomers())

#Tested Using Postman
@customers_bp.route("/charge/<username>", methods=["POST"])
def charge_wallet(username):
    """
    Endpoint to charge a customer's wallet.

    This route handles POST requests to charge a customer's wallet based on the provided username parameter.

    **Method:** POST

    **URL:** `/api/customers/charge/<username>`

    **Parameters:**
    - `username` (str): The username of the customer whose wallet will be charged.

    **Request Data (JSON):**
    - `amount` (float): The amount to be charged to the customer's wallet.

    **Returns:**
    - If the wallet is successfully charged, returns a JSON response with a success message:
      ```json
      {"message": "Wallet charged with <amount> successfully"}
      ```

    - If there's an error during the charging process, returns a JSON response with a failure message:
      ```json
      {"message": "FAILURE IN CHARGE"}
      ```

    **Example Usage (Postman):**
    - Method: POST
    - URL: `http://your-api-base-url/api/customers/charge/<username>`
    - Body (JSON):
      ```json
      {
        "amount": 50.0
      }
      ```

    - Expected Response (Success):
      ```json
      {"message": "Wallet charged with 50.0 successfully"}
      ```

    - Expected Response (Failure):
      ```json
      {"message": "FAILURE IN CHARGE"}
      ```

    **Testing:**
    - This endpoint has been tested using Postman.
    """
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
    """
    Endpoint to deduct an amount from a customer's wallet for payment.

    This route handles POST requests to deduct an amount from a customer's wallet for payment based on the provided username parameter.

    **Method:** POST

    **URL:** `/api/customers/pay/<username>`

    **Parameters:**
    - `username` (str): The username of the customer making the payment.

    **Request Data (JSON):**
    - `amount` (float): The amount to be deducted from the customer's wallet for payment.

    **Returns:**
    - If the wallet is successfully paid, returns a JSON response with a success message:
      ```json
      {"message": "Wallet paid <amount> successfully"}
      ```

    - If there's not enough credit in the wallet, returns a JSON response indicating insufficient funds:
      ```json
      {"message": "NOT ENOUGH CREDIT"}
      ```

    - If there's an error during the payment process, returns a JSON response with a failure message:
      ```json
      {"message": "FAILURE IN PAY"}
      ```

    **Example Usage (Postman):**
    - Method: POST
    - URL: `http://your-api-base-url/api/customers/pay/<username>`
    - Body (JSON):
      ```json
      {
        "amount": 30.0
      }
      ```

    - Expected Response (Success):
      ```json
      {"message": "Wallet paid 30.0 successfully"}
      ```

    - Expected Response (Insufficient Funds):
      ```json
      {"message": "NOT ENOUGH CREDIT"}
      ```

    - Expected Response (Failure):
      ```json
      {"message": "FAILURE IN PAY"}
      ```

    **Testing:**
    - This endpoint has been tested using Postman.
    """
    data = request.get_json()
    amount = data["amount"]
    try:
        if(deduceCustomer(username, amount)): return jsonify({"message": f"Wallet paid {amount} successfully"})
        else: return jsonify({"message": "NOT ENOUGH CREDIT"})
    except:
        return jsonify({"message": f"FAILURE IN PAY"})
