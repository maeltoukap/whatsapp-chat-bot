import nltk
import numpy as np
import random
import json
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
nltk.data.path.append('nltk_data/')

import tensorflow as tf

lemmatizer = WordNetLemmatizer()

# Charger le fichier intents
with open("intents_en.json") as file:
    data = json.load(file)

# Extraire les mots clés et les catégories
words = []
classes = []
documents = []
ignore_words = ['?']

for intent in data["intents"]:
    for pattern in intent["patterns"]:
        # Tokenize les mots
        w = nltk.word_tokenize(pattern)
        # Ajouter les mots aux mots clés
        words.extend(w)
        # Ajouter les documents à la liste de documents
        documents.append((w, intent["tag"]))
        # Ajouter la catégorie à la liste des catégories
        if intent["tag"] not in classes:
            classes.append(intent["tag"])

# Lématiser les mots clés
words = [lemmatizer.lemmatize(w.lower()) for w in words if w not in ignore_words]
words = sorted(list(set(words)))

# Organiser les catégories
classes = sorted(list(set(classes)))

# Créer des vecteurs pour les documents
training = []
output = []

output_empty = [0] * len(classes)

for doc in documents:
    # Initialiser les vecteurs de mots clés
    bag = []
    pattern_words = doc[0]
    pattern_words = [lemmatizer.lemmatize(word.lower()) for word in pattern_words]
    for w in words:
        bag.append(1) if w in pattern_words else bag.append(0)

    # Codage de la sortie pour la catégorie correspondante
    output_row = list(output_empty)
    output_row[classes.index(doc[1])] = 1

    training.append([bag, output_row])

# Mélanger les données d'entraînement
random.shuffle(training)

# def padding(training, max_length):
#     padded_training = np.zeros((len(training), max_length))
#     for i, sequence in enumerate(training):
#         length = len(sequence)
#         padded_training[i, :length] = np.array(sequence).tolist()
#     return padded_training

# training = padding(training, 20)

# training = np.expand_dims(np.array(training), axis=1)
training = np.array(training, dtype=object)
# Créer les listes pour les entrées et les sorties
train_x = list(training[:,0])
train_y = list(training[:,1])

# Créer le modèle
model = tf.keras.Sequential([
    tf.keras.layers.Dense(128, input_shape=(len(train_x[0]),), activation='relu'),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(len(train_y[0]), activation='softmax')
])

# Compiler le modèle
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# Entraîner le modèle
model.fit(np.array(train_x), np.array(train_y), epochs=100, batch_size=8, verbose=1)

# Sauvegarder le modèle
model.save("model.h5")

# Charger le modèle
model = tf.keras.models.load_model("model.h5")

def bow(sentence, words, show_details=True):
    stemmer = nltk.PorterStemmer()
    # Convertir la phrase en sac de mots
    sentence_words = nltk.word_tokenize(sentence)
    # Porter les mots
    sentence_words = [stemmer.stem(word.lower()) for word in sentence_words]
    bag = [0]*len(words)  
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s: 
                bag[i] = 1
                if show_details:
                    print("found in bag: %s" % w)

    return(np.array(bag))



def predict_class(sentence, model):
    # Prédire la classe pour une entrée donnée
    p = bow(sentence, words)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list

def getResponse(ints, intents_json):
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if(i['tag']== tag):
            result = random.choice(i['responses'])
            break
    return result

def chatbot_response(text):
    ints = predict_class(text, model)
    res = getResponse(ints, data)
    return res


while True:
    message = input("")
    print(message)
    # ints = predict_class(message, model=model)
    res = chatbot_response(message)
    print(res)
# def initBot():
#     message = input("")
#     print(message)
#     ints = predict_class(message, model=model)
#     res = chatbot_response(message)
#     print(res)