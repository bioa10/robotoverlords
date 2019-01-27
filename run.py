from flask import Flask, flash, render_template, request, redirect
from flask_migrate import Migrate

from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import tensorflow.keras as keras
import sys
sys.path.append('./')

from tf_train_validate import *
from p2_tf_train_validate import *

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
@app.route("/p1/data", methods=["GET"])
def p1_data():
	return render_template("p1/data.html",
		datasets=get_data()
	)

#--- Project 2: CCFraud ---
@app.route("/p2", methods=["GET"])
def p2_index():
    return render_template("p2/index.html")

@app.route("/p2/train", methods=["GET"])
def p2_train(): #Still needs to be done
	return

#--- Project 3: Flappy Bird---
@app.route("/p3", methods=["GET"])
def p3_index():
    return render_template("p3/index.html")

@app.route("/p3/play", methods=["GET"])
def p3_play():
	return render_template("p3/play.html")

if __name__ == "__main__":
    app.run(debug=True)