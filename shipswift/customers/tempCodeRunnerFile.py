t.get_json()
        amount = data.get("amount")
        chargeCustomer(username, amount)
        return jsonify({"message": f"Walle