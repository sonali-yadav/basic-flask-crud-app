from flask import Flask, render_template, url_for, request, session, flash, redirect
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from models import db
import models
import hashlib

# settings


# creating the application object and config
app = Flask(__name__)
app.secret_key = "bulbasaur"
app.permanent_session_lifetime = timedelta(minutes=20)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///monarklims.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# creating instance of database object
db.init_app(app)

with app.app_context():
    db.create_all()


# mapping for main index page
@app.route("/")
def index():
    return render_template("index.html")

# mapping for login page
@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True # session will last as long as set in setting above
        user = request.form["username"]
        password = request.form["password"]


        # validate the user details
        h = hashlib.md5(password.encode())
        pw = h.hexdigest()
        user = models.User.query.filter_by(username=user, password=pw).first()
        if user is not None and user.is_active:
            session["user"] = { "name": user.name, "email": user.email,
                "is_admin": user.is_admin,
                "phone": user.phone, "username": user.username }
            flash("Login Successful!")
            return redirect(url_for("user"))
        else:
            flash("Login Unsuccessful! Please try again!")
            return redirect(url_for("login"))
    else:
        if "user" in session:
            flash("Already Logged In!")
        return render_template("login.html")

# mapping for user dashboard
@app.route("/user")
def user():
    if "user" in session:
        user = session['user']
        if user['is_admin']:
            return render_template("admin.html")
        return render_template("user.html")
    else:
        flash("You are not logged in!")
        return redirect(url_for("login"))

# mapping for admin dashboard
@app.route("/admin")
def admin():
    return render_template("admin.html")

# mapping for logout
@app.route("/logout")
def logout():
    if "user" in session:
        user = session["user"]
        flash(f"You have been logged out, {user['username']}!", "info")
    session.pop("user", None)
    session.pop("username", None)
    return redirect(url_for("login"))

# API: create user
@app.route("/user/new", methods=["POST", "GET"])
def create_user():
    if request.method == "POST":
        user = models.User(
            request.form["name"], request.form["email"],
            request.form["phone"], request.form["username"], request.form["password"])
        db.session.add(user)
        db.session.commit()
        db.session.close()
        flash(f"New user {request.form['name']} added successfully!")
        return redirect(url_for("admin"))
    else:
        return render_template("create_user.html")


# API: create customer
@app.route("/customer/new", methods=["POST", "GET"])
def add_customer():
    if request.method == "POST":
        customer = models.Customer(
            request.form["name"], request.form["email"],
            request.form["phone"])
        db.session.add(customer)
        db.session.commit()
        db.session.close()
        flash(f"New customer {request.form['name']} added successfully!")
        return redirect(url_for("admin"))
    else:
        return render_template("customer_form.html")

# API: delete customer (soft delete)
@app.route("/customer/delete", methods=["POST"])
def deactivate_customer():
    customer = models.Customer.query.filter_by(id=request.get("cust_id")).first()
    customer.is_active = False
    db.session.add(customer)
    db.session.commit()
    db.session.close()
    flash(f"Customer {request.form['name']} deactivated successfully!")
    return redirect(url_for("admin"))

# API: update customer
@app.route("/customer/edit", methods=["POST", "GET"])
def edit_customer():
    if request.method == "POST":
        customer = models.Customer.query.filter_by(id=request.args.get("cust_id")).first()
        customer.name = request.form["name"]
        customer.email = request.form["email"]
        customer.phone = request.form["phone"]
        db.session.commit()
        db.session.close()
        flash(f"Customer {request.form['name']} updated successfully!")
        return redirect(url_for("admin"))
    else:
        customer = models.Customer.query.filter_by(id=request.args.get("cust_id")).first()
        return render_template("customer_form.html", customer=customer)

# API: get all customers
@app.route("/customer/all", methods=["GET"])
def get_customers():
    customers = models.Customer.query.all()
    return render_template("customers_list.html", customers=customers)

# API: retrieve customer
@app.route("/customer/<cust_id>", methods=["GET"])
def get_customer(cust_id):
    customer = models.Customer.query.filter_by(id=request.args.get(cust_id)).first()
    return render_template("customer_form.html", customer=customer)

# API: upload file
# API: get uploaded files


# initializer
if __name__ == "__main__":
    app.run(debug=True)