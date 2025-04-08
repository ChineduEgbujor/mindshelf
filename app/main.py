from fastapi import FastAPI
from pydantic import BaseModel
from app.model import analyze_emotions

app = FastAPI()

class JournalEntry(BaseModel):
    text: str

@app.post("/analyze")
def analyze(entry: JournalEntry):
    emotions = analyze_emotions(entry.text)
    return {"emotions": emotions}