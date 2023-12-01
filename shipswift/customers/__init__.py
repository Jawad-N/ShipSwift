# ShipSwift/customers/__init__.py
from flask import Flask
from os import path

def create_app():
    """
    Create and configure the Flask application for the customers service.

    This function initializes a Flask application, registers blueprints (routes), and returns the configured app.

    **Note:**
    - Blueprints are registered to organize and modularize routes. In this case, the `customers_bp` blueprint is registered
      with the prefix '/api/customers'.

    **Returns:**
    - An instance of the Flask application configured for the customers service.

    **Usage:**
    - Import this function in your main application script to create the Flask app.

    **Example:**
    ```python
    from __init__ import create_app

    app = create_app()
    ```
    """
    app = Flask(__name__)
    # Register blueprints (routes) for the customers service
    from routes import customers_bp
    app.register_blueprint(customers_bp, url_prefix='/api/customers')
    return app

