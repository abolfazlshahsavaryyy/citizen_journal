# app/main.py
from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline

# Load summarizer model once at startup
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

app = FastAPI()

class TextInput(BaseModel):
    text: str

@app.post("/summarize")
def summarize_text(input_data: TextInput):
    result = summarizer(
        input_data.text,
        max_length=130,  # you can tune these
        min_length=30,
        do_sample=False
    )
    return {"summary": result[0]["summary_text"]}
