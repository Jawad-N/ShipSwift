from __init__ import create_app



app = create_app()

if __name__ == '__main__':
    """
    Main entry point for the [service_name] service.

    This script creates and runs the Flask application for the [service_name] service. If the script is executed directly
    (not imported as a module), it starts the Flask development server.

    **Note:**
    - The Flask application is created using the `create_app` function from the `__init__.py` module.

    **Testing:**
    - To run the [service_name] service, execute this script. The service will be accessible at http://0.0.0.0:5001/.
    - Set the `debug` parameter to `True` for development purposes.
    """
    app.run( debug=True, port=5001, host= "0.0.0.0" )
    