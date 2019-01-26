import tensorflow as tf
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

def train_validate():
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

  #  "Training Accuracy"
  # Plotting the Results
  plt.plot(epoch, epoch_loss, label ='Loss/Error')
  plt.title('Training Results')
  plt.ylabel('loss/error')
  plt.xlabel('training epoch')
  plt.legend()
  results_path = 'static/images/graphs/results/p1_results.png'
  plt.savefig(results_path)
  #plt.show()

  testing_loss = model.evaluate(x_test,y_test)
  c = np.random.choice(len(x_test),10)
  sample = x_test[c]
  y_test = model.predict(sample)
  for pic,label in zip(sample,y_test):
    label = np.argmax(label)
    pic = pic.reshape(28,28)*255
    pic = Image.fromarray(np.uint8(pic))
    pic = pic.resize((512,512))
    pic.save("./static/images/graphs/results/"+str(label)+".jpg")
  return [testing_loss[0], testing_loss[1], results_path]