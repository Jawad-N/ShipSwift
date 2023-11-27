# inventory/routes.py
from flask import Blueprint, request, jsonify
import sys

sys.path.append("..")
import DB.dbSalesf as dbSales

inventory_bp = Blueprint("sales", __name__)

@inventory_bp.route("/add", methods=["POST"])
def add_product():
    data = request.get_json()
    user = data["user"]
    item = data["item"]
    count = data["count"]
    price = data["price"]
    date = data["date"]
    dbSales.addPurchase(user, item, count, price, date)
    return jsonify({"message": "Purchase added successfully"})

