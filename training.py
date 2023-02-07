import random
import json
import pickle
import numpy as np
import pandas as pd

import nltk
nltk.data.path.append('nltk_data/')
from nltk.stem import WordNetLemmatizer

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Dropout
from tensorflow.keras.optimizers import SGD
import tensorflow as tf

lemmatizer = WordNetLemmatizer()


intent = json.loads(open("intents_en.json").read())

words = []
classes = []
documents = []
ignore_letters = ['?', '_', '!', '.', ',']

for intent in intent["intents"]:
    for pattern in intent["patterns"]:
        word_list = nltk.word_tokenize(pattern)
        words.extend(word_list)
        documents.append((word_list, intent['tag']))
        if(intent["tag"] not in classes):
            classes.append(intent["tag"])
            
            
# print(documents)

words = [lemmatizer.lemmatize(word) for word in words if word not in ignore_letters]
words = sorted(set(words))

# print(words)


classes = sorted(set(classes))

pickle.dump(words, open('words.pkl', 'wb'))
pickle.dump(classes, open('classes.pkl', 'wb'))

training = []
output_empty = [0] * len(classes)

for document in documents:
    bag = []
    word_patterns = document[0]
    word_patterns = [lemmatizer.lemmatize(word.lower()) for word in word_patterns]
    for word in words:
        bag.append(1) if word in word_patterns else bag.append(0)
        
    output_row = list(output_empty)
    output_row[classes.index(document[1])] = 1
    training.append([bag, output_row])
    
# print((pd.DataFrame(training)))
# training = random.uniform(training)
random.shuffle(training)
training = np.array(training, dtype=object)

train_x = list(training[:, 0])
train_y = list(training[:, 1])

train_x = np.expand_dims(train_x, axis=1)
train_y = np.expand_dims(train_y, axis=1)

# train_x = tf.expand_dims(train_x, axis=0)
# train_y = tf.expand_dims(train_y, axis=0)

print(len(train_x))
model = Sequential()
# model.add(Dense(128, input_shape=113, activation='relu'))
model.add(Dense(128, input_shape=train_x[0].shape, activation='relu'))
# model.add(Dense(128, input_shape=(len(train_x[0])), activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(54, activation='relu'))
model.add(Dropout(0.5))
# model.add(Dense(113, activation='softmax'))
model.add(Dense(30, activation='softmax'))


sgd =  SGD(learning_rate=0.01, momentum=0.9, nesterov=True)
model.compile(optimizer=sgd, loss='categorical_crossentropy', metrics=['accuracy'])



hist = model.fit(np.array(train_x), np.array(train_y), epochs=200, batch_size=5, verbose=1)
# ev = model.evaluate(np.array(train_x), np.array(train_y), verbose=1)

# print(ev)
model.save("chatbotmodel.h5", hist)
print("done")
