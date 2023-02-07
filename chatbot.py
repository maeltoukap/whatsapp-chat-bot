import random
import json
import pickle
import numpy as np

import nltk
from nltk.stem import WordNetLemmatizer

from tensorflow.python.keras.models import load_model


lemmatizer = WordNetLemmatizer()

intent = json.loads(open("intents_en.json").read())

words = pickle.load(open("words.plkl", 'rb').read())
classes = pickle.load(open("classes.plkl", 'rb').read())
model = load_model("chatbotmodel.h5")