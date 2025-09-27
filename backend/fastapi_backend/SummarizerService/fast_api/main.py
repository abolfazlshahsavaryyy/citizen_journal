# app/main.py
from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline

# Load a lighter summarizer model once at startup
# comment following code to not download it after each build
# summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
summarizer=None
app = FastAPI()

class TextInput(BaseModel):
    text: str

@app.post("/summarize")
def summarize_text(input_data: TextInput):
    result = summarizer(
        input_data.text,
        max_length=130,   # can tune for lighter/faster inference
        min_length=30,
        do_sample=False
    )
    return {"summary": result[0]["summary_text"]}
