from __init__ import create_app

"""
    Run the Flask application for the customers service.

    This script creates the Flask app using the `create_app` function from the `__init__.py` module.
    It then runs the app with debugging enabled and makes it accessible from any host on port 5000.

    **Note:**
    - When this script is executed directly (not imported as a module), the Flask app will start running.

    **Example:**
    ```bash
    python your_script_name.py
    ```
"""

app = create_app()

if __name__ == '__main__':
    app.run( debug=True, port=5000, host= "0.0.0.0" )
    