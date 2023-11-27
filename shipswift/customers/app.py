from flask import request, Flask, jsonify
import sys, os
import json
from __init__ import create_app
from routes import customers_bp

app = create_app()

if __name__ == '__main__':
    app.run( debug=True, port=5000, host= "0.0.0.0" )