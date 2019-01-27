from __future__ import print_function
from keras.callbacks import LambdaCallback
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.optimizers import RMSprop
from keras.utils.data_utils import get_file
from keras.models import model_from_json
from keras import backend as k
import numpy as np
import random
import sys
import io

def gen_shake(diversity,ver):
    k.clear_session()
    out = ""

    path = get_file(
        'shakespeare.txt',
        origin='https://storage.googleapis.com/download.tensorflow.org/data/shakespeare.txt')
    with io.open(path, encoding='utf-8') as f:
        text = f.read().lower()

    maxlen = 40
    chars = sorted(list(set(text)))
    char_indices = dict((c, i) for i, c in enumerate(chars))
    indices_char = dict((i, c) for i, c in enumerate(chars))

    # load json and create model
    json_file = open('ShakeModels/model'+str(ver-1)+'.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    # load weights into new model
    loaded_model.load_weights("ShakeModels/model"+str(ver-1)+".h5")
    print("Loaded model from disk")

    def sample(preds, temperature=1.0):
        # helper function to sample an index from a probability array
        preds = np.asarray(preds).astype('float64')
        preds = np.log(preds) / temperature
        exp_preds = np.exp(preds)
        preds = exp_preds / np.sum(exp_preds)
        probas = np.random.multinomial(1, preds, 1)
        return np.argmax(probas)

    # evaluate loaded model on test data
    loaded_model.compile(loss='categorical_crossentropy', optimizer=RMSprop(lr=0.01))
    start_index = random.randint(0, len(text) - maxlen - 1)

    out += '----- diversity:' + "" + str(diversity) + "\n"

    generated = ''
    sentence = text[start_index: start_index + maxlen]
    generated += sentence
    out += '----- Generating with seed: "' + sentence + '"' + "\n"
    out += generated + " "

    for i in range(400):
        x_pred = np.zeros((1, maxlen, len(chars)))
        for t, char in enumerate(sentence):
            x_pred[0, t, char_indices[char]] = 1.

        preds = loaded_model.predict(x_pred, verbose=0)[0]
        next_index = sample(preds, diversity)
        next_char = indices_char[next_index]

        generated += next_char
        sentence = sentence[1:] + next_char

        out += next_char
    results = out.splitlines()
    print(out.splitlines())
    return results