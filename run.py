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

@app.route("/p1", methods=["GET"])
def p1_index():
    return render_template("p1/index.html")

@app.route("/p1/train", methods=["GET"])
def p1_train():
	results = train_validate()
	flash('Model Trained & Validated: Loss - '+str(results[0])+' | Accuracy - '+str(results[1]))
	return redirect("/")

def createModel():
	model = keras.models.Sequential()
	model.add(keras.layers.Dense(4))
	model.add(keras.layers.Dense(5))
	model.add(keras.layers.Dense(3))
	model.add(keras.layers.Dense(3,activation='softmax'))
	model.compile(optimizer='adam',loss='categorical_crossentropy',metrics=['accuracy'])
	return model

@app.route("/p1/validate", methods=["GET"])
def p1_validate():
	data = pd.read_csv("datasets/p1_dataset.csv")
	x = data.iloc[:,1:-1].values
	y = data.iloc[:,-1].values
	from sklearn.preprocessing import LabelEncoder,OneHotEncoder
	lb = LabelEncoder()
	y=lb.fit_transform(y)
	y = y.reshape((len(y),1))
	ohc = OneHotEncoder(categorical_features=[0],sparse=False)
	y=ohc.fit_transform(y)

	model = createModel()
	model.load_weights("./checkpoint1")
	accuracy = model.evaluate(x,y)[1]
	flash('Model Trained: '+ str(accuracy))
	return redirect("/")

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