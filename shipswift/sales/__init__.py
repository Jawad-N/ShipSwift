# ShipSwift/customers/__init__.py
from flask import Flask
from os import path

def create_app():
    app = Flask(__name__)
    # Register blueprints (routes) for the customers service
    from routes import salesbp
    app.register_blueprint(salesbp, url_prefix='/api/tradeSpace')
    return app

