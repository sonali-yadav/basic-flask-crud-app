from flask_sqlalchemy import SQLAlchemy
import hashlib

# models for app go here

db = SQLAlchemy()


class User(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(12), nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)

    def __init__(self, name, email, phone, username, password):
        h = hashlib.md5(password.encode())
        self.name = name
        self.email = email
        self.phone = phome
        self.username = username
        self.password = h.hexdigest()

class Customer(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(12), nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    def __init__(self, name, email, phone):
        self.name = name
        self.email = email
        self.phone = phome
