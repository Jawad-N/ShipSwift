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
    """
    Endpoint to add a new product to the inventory.

    This route handles POST requests to add a new product to the inventory based on the provided JSON data.

    **Method:** POST

    **URL:** `/api/inventory/add`

    **Request Data (JSON):**
    - `name` (str): The name of the product.
    - `category` (str): The category of the product.
    - `price` (float): The price of the product.
    - `description` (str): The description of the product.
    - `count` (int): The quantity of the product.

    **Returns:**
    - If a product with the same name already exists in the database, returns a JSON response indicating the duplication:
      ```json
      {"message": "Product with name = <name> already in DB"}
      ```

    - If the product is successfully added, returns a JSON response with a success message:
      ```json
      {"message": "Product added successfully"}
      ```

    - If there's an error during the database operation, returns a JSON response with a failure message:
      ```json
      {"message": "FAILURE IN DATABASE"}
      ```

    **Example Usage (Postman):**
    - Method: POST
    - URL: `http://your-api-base-url/api/inventory/add`
    - Body (JSON):
      ```json
      {
        "name": "New Product",
        "category": "Electronics",
        "price": 99.99,
        "description": "A description of the new product.",
        "count": 10
      }
      ```

    - Expected Response (Duplicate Product):
      ```json
      {"message": "Product with name = New Product already in DB"}
      ```

    - Expected Response (Success):
      ```json
      {"message": "Product added successfully"}
      ```

    - Expected Response (Failure in Database):
      ```json
      {"message": "FAILURE IN DATABASE"}
      ```

    **Testing:**
    - This endpoint has been tested using Postman.
    """
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
    """
    Endpoint to update product information in the inventory.

    This route handles PUT requests to update product information in the inventory based on the provided JSON data.

    **Method:** PUT

    **URL:** `/api/inventory/update/<name>`

    **Parameters:**
    - `name` (str): The name of the product to be updated.

    **Request Data (JSON):**
    - `name` (str, optional): The new name for the product.
    - `category` (str, optional): The new category for the product.
    - `price` (float, optional): The new price for the product.
    - `description` (str, optional): The new description for the product.
    - `count` (int, optional): The new quantity for the product.

    **Returns:**
    - If no product with the provided name is found, returns a JSON response indicating that there's no item with that name:
      ```json
      {"message": "NO ITEM WITH NAME <name>"}
      ```

    - If the product is successfully updated, returns a JSON response with a success message:
      ```json
      {"message": "Product updated"}
      ```

    - If the new product name is already used, returns a JSON response indicating the duplication:
      ```json
      {"message": "New Product Name is already Used"}
      ```

    - If there's an error during the database operation, returns a JSON response with a failure message:
      ```json
      {"message": "DB ERROR"}
      ```

    **Example Usage (Postman):**
    - Method: PUT
    - URL: `http://your-api-base-url/api/inventory/update/<name>`
    - Body (JSON):
      ```json
      {
        "name": "New Name",
        "category": "Updated Category",
        "price": 129.99,
        "description": "Updated description.",
        "count": 15
      }
      ```

    - Expected Response (No Item with Name):
      ```json
      {"message": "NO ITEM WITH NAME New Name"}
      ```

    - Expected Response (Success):
      ```json
      {"message": "Product updated"}
      ```

    - Expected Response (Duplicate Product Name):
      ```json
      {"message": "New Product Name is already Used"}
      ```

    - Expected Response (Failure in Database):
      ```json
      {"message": "DB ERROR"}
      ```

    **Testing:**
    - This endpoint has been tested using Postman.
    """
    data = request.get_json()
    x = updateItem(name, data)
    if (x == 0): return jsonify({"message": f"NO ITEM WITH NAME {name}"})
    elif (x == 1): return jsonify({"message": f"Product  updated"})
    elif (x == 2): return jsonify({"message": f"new Product Name is already Used"})
    else: return jsonify({"message": "DB ERROR"})





#Tested using postman
@inventory_bp.route("/deduce/<name>", methods=["PUT"])
def deduce_product(name):
    """
    Endpoint to deduce the stock of a product in the inventory.

    This route handles PUT requests to deduce the stock of a product in the inventory based on the provided product name.

    **Method:** PUT

    **URL:** `/api/inventory/deduce/<name>`

    **Parameters:**
    - `name` (str): The name of the product to deduce the stock.

    **Returns:**
    - If no product with the provided name is found, returns a JSON response indicating that the item does not exist:
      ```json
      {"message": "Item <name> Does Not Exist"}
      ```

    - If the stock of the product is empty, returns a JSON response indicating that the stock is empty:
      ```json
      {"message": "The stock of <name> is empty"}
      ```

    - If the stock of the product is successfully decreased by 1, returns a JSON response with a success message:
      ```json
      {"message": "The stock of <name> is decreased by 1"}
      ```

    - If there's an error during the database operation, returns a JSON response with a failure message:
      ```json
      {"message": "DB ERROR"}
      ```

    **Example Usage (Postman):**
    - Method: PUT
    - URL: `http://your-api-base-url/api/inventory/deduce/<name>`

    - Expected Response (Item Does Not Exist):
      ```json
      {"message": "Item <name> Does Not Exist"}
      ```

    - Expected Response (Stock is Empty):
      ```json
      {"message": "The stock of <name> is empty"}
      ```

    - Expected Response (Stock Decreased by 1):
      ```json
      {"message": "The stock of <name> is decreased by 1"}
      ```

    - Expected Response (Failure in Database):
      ```json
      {"message": "DB ERROR"}
      ```

    **Testing:**
    - This endpoint has been tested using Postman.
    """
    x = deduce(name)
    if(x == 0): return jsonify({"message": f"Item {name} Does Not Exist"})
    elif( x == 1 ): return jsonify({"message": f"The stock of {name} is empty"})
    elif( x == 2 ): return jsonify({"message": f"The stock of {name} is decreased by 1"})
    else: return jsonify({"message": "DB ERROR"})

#deduce custom number 
#Tested using postman
@inventory_bp.route("/deduce/<name>/<val>", methods=["PUT"])
def deduce_product2(name,val):
    """
    Endpoint to custom deduce the stock of a product in the inventory.

    This route handles PUT requests to custom deduce the stock of a product in the inventory based on the provided product name and custom deduction value.

    **Method:** PUT

    **URL:** `/api/inventory/deduce/<name>/<val>`

    **Parameters:**
    - `name` (str): The name of the product to deduce the stock.
    - `val` (int): The custom deduction value for the stock. Must be a positive integer.

    **Returns:**
    - If no product with the provided name is found, returns a JSON response indicating that the item does not exist:
      ```json
      {"message": "Item <name> Does Not Exist"}
      ```

    - If the stock of the product is empty, returns a JSON response indicating that the stock is empty:
      ```json
      {"message": "The stock of <name> is empty"}
      ```

    - If the stock of the product is successfully decreased by the custom value, returns a JSON response with a success message:
      ```json
      {"message": f"The stock of <name> is decreased by {val}"}
      ```

    - If there's an error during the database operation, returns a JSON response with a failure message:
      ```json
      {"message": "DB ERROR"}
      ```

    - If the provided custom deduction value is not a positive integer, returns a plain text response indicating that the URL does not exist:
      ```
      "URL DNE"
      ```

    **Example Usage (Postman):**
    - Method: PUT
    - URL: `http://your-api-base-url/api/inventory/deduce/<name>/<val>`

    - Expected Response (Item Does Not Exist):
      ```json
      {"message": "Item <name> Does Not Exist"}
      ```

    - Expected Response (Stock is Empty):
      ```json
      {"message": "The stock of <name> is empty"}
      ```

    - Expected Response (Stock Decreased by Custom Value):
      ```json
      {"message": "The stock of <name> is decreased by <val>"}
      ```

    - Expected Response (Failure in Database):
      ```json
      {"message": "DB ERROR"}
      ```

    - Expected Response (Invalid Custom Deduction Value):
      ```
      "URL DNE"
      ```

    **Testing:**
    - This endpoint has been tested using Postman.
    """
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
    """
    Endpoint to retrieve product information from the inventory.

    This route handles GET requests to retrieve information about a product in the inventory based on the provided product name.

    **Method:** GET

    **URL:** `/api/inventory/get/<name>`

    **Parameters:**
    - `name` (str): The name of the product to retrieve information.

    **Returns:**
    - If the product is not found, returns a JSON response with a message indicating that the product is not found:
      ```json
      {"message": "Product not found"}
      ```

    - If there's a failure in the database operation, returns a JSON response with a failure message:
      ```json
      {"message": "FAILURE IN DB"}
      ```

    - If the product is found, returns a JSON response with information about the product.

    **Example Usage (Postman):**
    - Method: GET
    - URL: `http://your-api-base-url/api/inventory/get/<name>`

    - Expected Response (Product Not Found):
      ```json
      {"message": "Product not found"}
      ```

    - Expected Response (Failure in Database):
      ```json
      {"message": "FAILURE IN DB"}
      ```

    - Expected Response (Product Found):
      ```json
      {
        "name": "<product_name>",
        "category": "<product_category>",
        "price": <product_price>,
        "description": "<product_description>",
        "count": <product_quantity>
      }
      ```

    **Testing:**
    - This endpoint has been tested using Postman.
    """
    #The product is not unique by name, thus might display multiple items
    product = retrieve(name)
    if(product == False): return jsonify({"message": f"FAILURE IN DB"})
    else:
        if(len(product) == 0): return jsonify({"message": "Product not found"}), 404
        else: return jsonify(product)
    
#Tested Using Postman
@inventory_bp.route("/get", methods = ["GET"])
def get_products():
    """
    Endpoint to retrieve information about all products in the inventory.

    This route handles GET requests to retrieve information about all products in the inventory.

    **Method:** GET

    **URL:** `/api/inventory/get`

    **Parameters:**
    None

    **Returns:**
    - If there's a failure in displaying the inventory, returns a JSON response with a failure message:
      ```json
      {"message": "FAILURE IN DISPLAYING INVENTORY"}
      ```

    - If the inventory is successfully displayed, returns a JSON response with information about all products.

    **Example Usage (Postman):**
    - Method: GET
    - URL: `http://your-api-base-url/api/inventory/get`

    - Expected Response (Failure in Displaying Inventory):
      ```json
      {"message": "FAILURE IN DISPLAYING INVENTORY"}
      ```

    - Expected Response (Inventory Displayed):
      ```json
      [
        {
          "name": "<product_name1>",
          "category": "<product_category1>",
          "price": <product_price1>,
          "description": "<product_description1>",
          "count": <product_quantity1>
        },
        {
          "name": "<product_name2>",
          "category": "<product_category2>",
          "price": <product_price2>,
          "description": "<product_description2>",
          "count": <product_quantity2>
        },
        ...
      ]
      ```

    **Testing:**
    - This endpoint has been tested using Postman.
    """
    D = display()
    if(D == False): return jsonify({"message": "FAILURE IN DISPLAYING INVENTORY"})
    else: return jsonify(D)
    
