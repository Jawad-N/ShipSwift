# models.py

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    fullName = db.Column(db.String(150), nullable=False)
    address = db.Column(db.String(150), nullable=False)
    gender = db.Column(db.Boolean, nullable=False)
    maritalStatus = db.Column(db.String(150), nullable=False)
    wallet = db.Column(db.Integer, nullable=False)

class Inventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    category = db.Column(db.String(150), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(150))
    count = db.Column(db.Integer, nullable=False)

class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    buyer = db.Column(db.String(150), nullable=False)
    item = db.Column(db.String(150), nullable=False)
    count = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, nullable=True)  # Assuming date can be nullable
