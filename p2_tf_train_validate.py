import pandas as pd
import tensorflow as tf
import tensorflow.keras as keras
from sklearn.utils import shuffle
import matplotlib.pyplot as plt
import numpy as np


def p2_train_validate:
    # Read in file with data from credit card records
    data = pd.read_csv("datasets/ccfraud_dataset.csv")

    # Finding all the frauds due to under 1% of records being frauds
    fraudIndex = []
    cnt = 0
    for index, row in data.iterrows():
        if (row['Class'] != 0):
            cnt += 1
            fraudIndex.append(index)  # Keep track of where the fraud is in the data set

    # using 95% for training, 5% for testing(roughly)
    testNum = round((len(fraudIndex) * .95))
    fraudData = data.iloc[fraudIndex[:], :]  # Loading in the fraudulent transcations into a DataFrame
    testingNegData = fraudData.iloc[testNum:]  # Loading a certain amount into testing file
    fraudData = fraudData.iloc[:testNum]  # loading the rest into a training file

    # finding all the legitimate transactions
    legitIndex = []
    numLegit = 0
    shufdata = shuffle(data)  # shuffling the data so that we get a variation
    for index, row in shufdata.iterrows():
        if (numLegit == cnt):  # after we get the same amount of legitimate transactions we stop going through
            break;
        elif (row['Class'] == 0):  # we find the legitimate indexes
            numLegit += 1
            legitIndex.append(index)

    legitData = data.iloc[legitIndex[:], :]  # Populating a DF with all our legitimate transactions
    testingPosData = legitData.iloc[testNum:]  # Populating the testing file with positive transactions
    legitData = legitData.iloc[:testNum]

    trainingData = legitData.append(fraudData)  # Combining legitimate transactions with fraudulent to make our training
    testingData = testingPosData.append(testingNegData)  # combining to make our testing data

    trainingData = trainingData.drop(columns=["Time"])  # the time is irrelivant for our purposes
    testingData = testingData.drop(columns=["Time"])

    trainingClass = trainingData.copy()  # copying all data to our class DF
    testingClass = testingData.copy()

    trainingClass = trainingClass.drop(
        columns=["V1", "V2", "V3", "V4", "V5", "V6", "V7", "V8", "V9", "V10", "V11", "V12", "V13", "V14", "V15", "V16",
                 "V17", "V18", "V19", "V20", "V21", "V22", "V23", "V24", "V25", "V26", "V27", "V28", "Amount"])
    testingClass = testingClass.drop(
        columns=["V1", "V2", "V3", "V4", "V5", "V6", "V7", "V8", "V9", "V10", "V11", "V12", "V13", "V14", "V15", "V16",
                 "V17", "V18", "V19", "V20", "V21", "V22", "V23", "V24", "V25", "V26", "V27", "V28", "Amount"])

    # Converting our data into an array for tensor flow
    trainingData = trainingData.values
    testingData = testingData.values
    trainingClass = trainingClass.values
    testingClass = testingClass.values

    # Creating the model
    model = keras.Sequential([
        keras.layers.Flatten(),
        keras.layers.Dense(128, activation=tf.nn.relu),  # neurons
        keras.layers.Dense(2, activation=tf.nn.softmax)  # 2 nodes that they can possibly fall into
    ])

    # Comiling our model
    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',  # These are algorithms that could possibly be changed in the
                  metrics=['accuracy'])  # Future for better performance

    test = model.fit(trainingData, trainingClass, epochs=5)  # Training our model

    model.test_on_batch(testingData, testingClass)
    model.metrics_names

    test_loss, test_acc = model.evaluate(testingData, testingClass)  # Testing our test data

    epoch = []
    epoch_loss = []
    for x in range(1, 10):  # Creating data to plot
        history = model.fit(trainingData, trainingClass, epochs=1)
        model.test_on_batch(testingData, testingClass)
        model.metrics_names
        epoch.append(x)
        epoch_loss.append(history.history['loss'])

    # "Training Accuracy"
    # Plotting the Results
    plt.plot(epoch, epoch_loss, label='Loss/Error')
    plt.title('Training Results')
    plt.ylabel('loss/error')
    plt.xlabel('training epoch')
    plt.legend()
    results_path = 'images/results/p2/p2_results.png'
    plt.savefig("static/" + results_path)  # Comment this if it doesnt run

    testing_loss = model.evaluate(testingData, testingClass)
    c = np.random.choice(len(testingData), 2)
    sample = testingData[c]
    y_test = model.predict(sample)
    return [testing_loss[1], testing_loss[0], results_path]