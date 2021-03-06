import tensorflow as tf
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image


mnist = tf.keras.datasets.mnist

(x_train, y_train),(x_test, y_test) = mnist.load_data()
x_train, x_test = x_train / 255.0, x_test / 255.0

model = tf.keras.models.Sequential([
tf.keras.layers.Flatten(),
tf.keras.layers.Dense(512, activation=tf.nn.relu),
tf.keras.layers.Dropout(0.2),
tf.keras.layers.Dense(10, activation=tf.nn.softmax)
])
model.compile(optimizer='adam',
			loss='sparse_categorical_crossentropy',
			metrics=['accuracy'])

epoch = []
epoch_loss = []
for x in range(1,3):
	history = model.fit(x_train, y_train, epochs=1)
	model.test_on_batch(x_test, y_test)
	model.metrics_names
	epoch.append(x)
	epoch_loss.append(history.history['loss'])
	
model.save_weights("model.h5")
print("Saved model to disk")
	
# load weights into new model
model.load_weights("model.h5")
print("Loaded model from disk")

testing_loss = model.evaluate(x_test,y_test)

