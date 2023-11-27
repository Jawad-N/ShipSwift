# ShipSwift/customers/__init__.py
from flask import Flask

def create_app():
    app = Flask(__name__)

    # Load configuration from a config file or environment variables if needed

    # Initialize database
    from .models import db
    db.init_app(app)

    # Register blueprints (routes) for the customers service
    from .routes import customers_bp
    app.register_blueprint(customers_bp, url_prefix='/customers')

    return app
