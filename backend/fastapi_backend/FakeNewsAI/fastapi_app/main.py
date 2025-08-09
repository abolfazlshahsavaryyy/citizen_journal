from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from domain_models.model import News
import joblib
import os

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # /app

lr_model_path = os.path.join(BASE_DIR, "models", "LogisticRegression(C=10, max_iter=1000).pkl")


lr_model = joblib.load(lr_model_path)

# Request schema
class NewsRequest(BaseModel):
    title: str
    text: str

# Logistic Regression endpoint
@app.post("/predict/logistic-regression")
def predict_logistic(news: NewsRequest):
    news_instance = News(news.title, news.text)
    prediction = news_instance.predict_logistic_regression(lr_model)
    return prediction


