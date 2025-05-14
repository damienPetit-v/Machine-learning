import pandas as pd
import os
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
import nltk
from nltk.corpus import stopwords

# nltk.download('stopwords')  # à faire une seule fois

french_stopwords = stopwords.words('french')
negations = {'pas', 'ne', 'n', 'jamais', 'rien', 'aucun', 'ni'}
custom_stopwords = [word for word in french_stopwords if word not in negations]

def handle_negation(text):
    negation_words = {'pas', 'ne', 'n', 'jamais', 'rien', 'aucun', 'ni'}
    words = text.split()
    if any(word in negation_words for word in words):
        return "NEG_" + text
    return text

# 📁 Fichiers de sauvegarde
MODEL_FILE = "sentiment_model.pkl"
VECTORIZER_FILE = "vectorizer.pkl"

# 📌 Vérifie si les fichiers existent
if os.path.exists(MODEL_FILE) and os.path.exists(VECTORIZER_FILE):
    print("🔁 Chargement du modèle et du vectorizer...")
    model = joblib.load(MODEL_FILE)
    vectorizer = joblib.load(VECTORIZER_FILE)
else:
    print("🧠 Entraînement du modèle...")

    # 1. Charger les données
    df = pd.read_csv('french_tweets.csv', encoding='utf-8', delimiter=',')
    df.columns = ['label', 'tweet']

    # 2. Split
    X = df['tweet']
    y = df['label']
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y)

    # 3. Appliquer gestion de la négation
    X_train = X_train.apply(handle_negation)
    X_test = X_test.apply(handle_negation)

    # 4. Vectorisation
    vectorizer = TfidfVectorizer(stop_words=custom_stopwords, max_features=5000)
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)

    # 5. Entraînement
    model = LogisticRegression()
    model.fit(X_train_vec, y_train)

    # 6. Évaluation
    y_pred = model.predict(X_test_vec)
    print("Rapport de classification :")
    print(classification_report(y_test, y_pred))

    # 7. Sauvegarde
    joblib.dump(model, MODEL_FILE)
    joblib.dump(vectorizer, VECTORIZER_FILE)
    print("💾 Modèle et vectorizer sauvegardés.")


def prediction(phrase):
    phrase = handle_negation(phrase)
    vec = vectorizer.transform([phrase])
    pred = model.predict(vec)
    if "NEG_" in phrase and pred == 1:
        pred = 1 - pred
    return pred[0]

# Boucle de test
while True:
    phrase = input("Écris un tweet ('q' pour quitter) : ")
    if phrase.lower() == 'q':
        break
    result = prediction(phrase)
    print("🟢 Positif" if result == 1 else "🔴 Négatif")
