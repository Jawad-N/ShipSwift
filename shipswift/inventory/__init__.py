# ShipSwift/customers/__init__.py
from flask import Flask

def create_app():
    app = Flask(__name__)
    # Register blueprints (routes) for the customers service
    from routes import inventory_bp
    app.register_blueprint(inventory_bp, url_prefix='/api/inventory')
    return app

