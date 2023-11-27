from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    full_name = db.Column(db.String(150), nullable=False)
    address = db.Column(db.String(150), nullable=False)
    gender = db.Column(db.Boolean, nullable=False)
    marital_status = db.Column(db.String(150), nullable=False)
    wallet = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Customer {self.username}>"
