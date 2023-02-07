import random
import json
import pickle
import numpy as np

import nltk
nltk.data.path.append('nltk_data/')
from nltk.stem import WordNetLemmatizer

# from tensorflow.python.keras.models import load_model
from tensorflow import keras

lemmatizer = WordNetLemmatizer()


intents = json.loads(open("intents_en.json").read())


with open("words.pkl", 'rb') as pickle_file: words = pickle.load(pickle_file)
with open("classes.pkl", 'rb') as pickle_file: classes = pickle.load(pickle_file)

# words = pickle.load(open("words.pkl", 'rb').read())
# classes = pickle.load(open("classes.pkl", 'rb').read())

model = keras.models.load_model("chatbotmodel.h5")
# model = load_model("chatbotmodel.h5")

def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]
    return sentence_words


def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
    return np.array(bag)

def predict_class(sentence):
    bow = bag_of_words(sentence)
    print(np.array(bow).shape)
    
    # bow = np.expand_dims(bow, axis=0)
    # bow = np.expand_dims(bow, axis=1)
    # res = model.predict(np.array(bow))[0]
    model_input = np.expand_dims(np.array(bow), axis=0)
    model_input = np.expand_dims(model_input, axis=1)
    res = model.predict(model_input)[0]
    ERROR_THRESHOLD = 0.25
    result = [[i, r] for i, r in enumerate(res) if r.all() > ERROR_THRESHOLD]
    
    print(enumerate(res))
    for i, r in enumerate(res):
        if r.all() > ERROR_THRESHOLD:
            print(i)
            print(r)
    result.sort(key=lambda x: x[1], reverse=True)
    # print(result)
    return_list = []
    for r in result:
        return_list.append({'intent': classes[r[0]], 'probability': str(r[1])})
    return return_list

def get_response(intent_list, intents_json):
    # print(intent_list[0])
    tag = intent_list[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if i['tag'] == tag:
            result = random.choice(i['responses'])
            break
    return result

print("Bot is running")

while True:
    message = input("")
    print(message)
    ints = predict_class(message)
    res = get_response(intent_list=ints, intents_json=intents)
    print(res)