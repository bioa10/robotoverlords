from flask import Flask, flash, render_template, request, redirect
from flask_migrate import Migrate

from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import tensorflow.keras as keras
import sys
sys.path.append('./')

from tf_train_validate import *

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

#--- Project 1 ---
@app.route("/p1", methods=["GET"])
def p1_index():
    return render_template("p1/index.html")

@app.route("/p1/train", methods=["GET"])
def p1_train():
	results = train_validate()
	return render_template("p1/results.html",
		accuracy=results[0],
		error=results[1],
		results_path=results[2],
		predictions=results[3]
	)

#--- Project 3: Flappy Bird---
@app.route("/p3", methods=["GET"])
def p3_index():
    return render_template("p3/index.html")

@app.route("/p3/watch", methods=["GET"])
def p3_watch():
	return render_template("p3/watch.html")

if __name__ == "__main__":
    app.run(debug=True)