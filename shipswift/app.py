# app.py
from flask import Flask

app = Flask(__name__)

# Import and register blueprints (routes) for each module
from customers.routes import customers_bp
from inventory.routes import inventory_bp
from sales.routes import sales_bp

app.register_blueprint(customers_bp, url_prefix='/customers')
app.register_blueprint(inventory_bp, url_prefix='/inventory')
app.register_blueprint(sales_bp, url_prefix='/sales')

if __name__ == '__main__':
    app.run(debug=True)
