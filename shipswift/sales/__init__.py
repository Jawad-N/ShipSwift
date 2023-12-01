# ShipSwift/customers/__init__.py
from flask import Flask
from os import path

def create_app():
    """
    Create and configure the Flask application for the customers service.

    This function initializes a Flask application instance and registers the blueprints (routes) for the sales service.

    **Returns:**
    - Flask Application: An instance of the Flask application configured for the customers service.

    **Example Usage:**
    ```python
    from customers import create_app

    app = create_app()
    ```

    **Note:**
    - The function uses the Flask `Blueprint` named `salesbp` from the `routes` module.

    **Testing:**
    - This function is typically called in the main application script to create the Flask app for the customers service.
    """
    app = Flask(__name__)
    # Register blueprints (routes) for the customers service
    from routes import salesbp
    app.register_blueprint(salesbp, url_prefix='/api/sales')
    return app

