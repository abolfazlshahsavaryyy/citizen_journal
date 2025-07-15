from sklearn.linear_model import LogisticRegression
import pandas as pd
import joblib
import os

class News:
    def __init__(self, title, text):
        self.title = title
        self.text = text

    def predict_logistic_regression(self, model: LogisticRegression):
        BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 
        tfidf_path = os.path.join(BASE_DIR, "models", "tfidf_vectorizer.pkl")

        # Load the saved TF-IDF vectorizer
        tfidf = joblib.load(tfidf_path)

        # Convert the input text to TF-IDF format
        X = tfidf.transform([self.text])  # ← FIX: wrap in list

        # Get predicted class
        predicted_class = model.predict(X)[0]

        # Get predicted probabilities
        probabilities = model.predict_proba(X)

        # Get confidence
        confidence = probabilities[0][predicted_class]

        return {
            "predicted_class": int(predicted_class),
            "confidence": round(float(confidence), 4),
            "message": f"The model is {round(confidence * 100)}% confident that this news belongs to class {predicted_class}"
        }
