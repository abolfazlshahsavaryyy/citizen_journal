from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import numpy as np
import tensorflow as tf
from sklearn.feature_extraction.text import TfidfVectorizer
import os

# ----------------------------------------------------
# 1. Define paths for saved models
# ----------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VECTORIZER_PATH = os.path.join(BASE_DIR, "tfidf_vectorizer_4000.pkl")
MODEL_PATH = os.path.join(BASE_DIR, "hate_speech_model.keras")

# ----------------------------------------------------
# 2. Initialize FastAPI app
# ----------------------------------------------------
app = FastAPI(title="Hate Speech Detection API")

# ----------------------------------------------------
# 3. Load vectorizer and model ONCE (at startup)
# ----------------------------------------------------
try:
    vectorizer: TfidfVectorizer = joblib.load(VECTORIZER_PATH)
except Exception as e:
    raise RuntimeError(f"Failed to load TF-IDF vectorizer: {e}")

try:
    model: tf.keras.Model = tf.keras.models.load_model(MODEL_PATH)
except Exception as e:
    raise RuntimeError(f"Failed to load Keras model: {e}")

# ----------------------------------------------------
# 4. Define request schema
# ----------------------------------------------------
class TextInput(BaseModel):
    content: str

# ----------------------------------------------------
# 5. POST endpoint for predictions
# ----------------------------------------------------
@app.post("/predict")
async def predict(input_data: TextInput):
    try:
        # Step 1: Transform input using loaded TF-IDF vectorizer
        transformed_input = vectorizer.transform([input_data.content])

        # Step 2: Convert sparse matrix to dense numpy array
        dense_input = transformed_input.toarray()

        # Step 3: Predict with Keras model
        prediction = model.predict(dense_input)

        # Step 4: Convert prediction to label (0 or 1)
        label = int((prediction[0] > 0.5))  # binary classification threshold

        return {
            "prediction": label,
            "probability": float(prediction[0])  # optional: raw probability
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ----------------------------------------------------
# 6. Root endpoint (optional health check)
# ----------------------------------------------------
@app.get("/")
async def root():
    return {"message": "Hate Speech Detection API is running"}
