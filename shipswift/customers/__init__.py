# ShipSwift/customers/__init__.py
from flask import Flask
from os import path

def create_app():
    app = Flask(__name__)
    # Register blueprints (routes) for the customers service
    from routes import customers_bp
    app.register_blueprint(customers_bp, url_prefix='/api/customers')
    return app

