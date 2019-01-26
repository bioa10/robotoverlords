from flask import Flask, flash, render_template, request, redirect
from flask_migrate import Migrate

from flask_sqlalchemy import SQLAlchemy

import sys
sys.path.append('./')

#--- app configuration ---
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///book.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)
migrate = Migrate(app, db)

def get_db():
	return db

#--- models ---
from models import *

#--- controller & view logic ---
@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/p1", methods=["GET"])
def p1_index():
    return render_template("p1/index.html")

@app.route("/p1/input", methods=["GET"])
def p1_input():
    return render_template("p1/input.html")

@app.route("/p1/input_post", methods=["POST"])
def p1_input_post():
    return redirect("/p1")

# @app.route("/update/<book_id>", methods=["GET"])
# def update(book_id):
# 	book = Book.query.filter_by(id=book_id).first()
# 	return render_template("book/update.html", book=book)
# @app.route("/update_post", methods=["POST"])
# def update_post():
# 		book = Book.query.filter_by(id=int(request.form.get("id"))).first()
# 		book.title = request.form.get("title")
# 		db.session.commit()
# 		flash('Book updated.')
# 		return redirect("/")
# @app.route("/delete/<book_id>", methods=["GET"])
# def delete(book_id):
#     book = Book.query.filter_by(id=book_id).first()
#     db.session.delete(book)
#     db.session.commit()
#     flash('Book deleted.')
#     return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)