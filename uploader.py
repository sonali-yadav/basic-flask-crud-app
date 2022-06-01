from flask import Flask, render_template, url_for, request, session, flash, redirect
import models
from flask_sqlalchemy import SQLAlchemy
from models import db
from datetime import timedelta
from werkzeug.utils import secure_filename
import os

UPLOADS_FOLDER = 'uploads/documents/'

uploader = Flask(__name__)
uploader.secret_key = "pikachu"
uploader.permanent_session_lifetime = timedelta(minutes=20)
uploader.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///monarklims.sqlite3'
uploader.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
uploader.config['UPLOADS_FOLDER'] = UPLOADS_FOLDER


# creating instance of database object
db.init_app(uploader)

# API: to upload a file for any customer
@uploader.route("/", methods=["GET", "POST"])
def upload_file_for_customer():
    customers = models.Customer.query.filter_by(is_active=1).all()
    if request.method == "POST":
        if not 'file' in request.files:
            uploader.logger.info(request.files)
            flash("No file part in request!")
            return render_template("uploader.html", customers=customers)
        file = request.files.get('file')
        
        if file.filename == '':
            flash("No file part in request!")
            return render_template("uploader.html", customers=customers)
        
        filename = secure_filename(file.filename)
        path = os.path.join(uploader.config['UPLOADS_FOLDER'], filename)
        uploader.logger.info(path)
        file.save(path)
        document = models.Document(path, request.form["customer"])
        db.session.add(document)
        db.session.commit()
        flash("File uploaded successfully!")
        return render_template("uploader.html", customers=customers)
    else:
        return render_template("uploader.html", customers=customers)


# initializer
if __name__ == "__main__":
    uploader.run(debug=True, port=5001)