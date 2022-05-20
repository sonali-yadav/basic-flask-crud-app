from flask_sqlalchemy import SQLAlchemy
import hashlib
from datetime import datetime

# models for app go here

db = SQLAlchemy()


class User(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(12), nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    cust_id = db.Column(db.Integer, db.ForeignKey('customer.id'))

    def __init__(self, name, email, phone, username, password, is_admin, cust_id):
        h = hashlib.md5(password.encode())
        self.name = name
        self.email = email
        self.phone = phone
        self.username = username
        self.password = h.hexdigest()
        self.is_admin = is_admin
        self.cust_id = cust_id


class Customer(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(12), nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    def __init__(self, name, email, phone):
        self.name = name
        self.email = email
        self.phone = phone


class Document(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    path = db.Column(db.String(200))
    created_at = db.Column(db.DateTime(timezone=False), default=datetime.now)
    cust_id = db.Column(db.Integer, db.ForeignKey('customer.id'))

    def __init__(self, path, cust_id):
        self.path = path
        self.cust_id = cust_id