import joblib
import os

MODEL_FILE = "sentiment_model.pkl"
VECTORIZER_FILE = "vectorizer.pkl"

# Chargement des fichiers entraînés
model = joblib.load(MODEL_FILE)
vectorizer = joblib.load(VECTORIZER_FILE)

def handle_negation(text):
    negation_words = {'pas', 'ne', 'n', 'jamais', 'rien', 'aucun', 'ni'}
    words = text.split()
    if any(word in negation_words for word in words):
        return "NEG_" + text
    return text

def prediction(phrase):
    phrase = handle_negation(phrase)
    vec = vectorizer.transform([phrase])
    pred = model.predict(vec)
    if "NEG_" in phrase and pred[0] == 1:
        pred = [0]
    return pred[0]
