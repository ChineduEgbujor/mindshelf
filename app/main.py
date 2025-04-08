from datetime import datetime
from fastapi import FastAPI
from pydantic import BaseModel
from app.model import analyze_emotions
import motor.motor_asyncio
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# MongoDB setup
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
db = client.moodmate

class JournalEntry(BaseModel):
    text: str

@app.post("/analyze")
def analyze(entry: JournalEntry):
    emotions = analyze_emotions(entry.text)
    return {"emotions": emotions}

@app.post("/journal")
async def save_journal(entry: JournalEntry):
    emotions = analyze_emotions(entry.text)
    doc = {
        "text": entry.text,
        "emotions": emotions,
        "timestamp": datetime.utcnow()
    }
    result = await db.entries.insert_one(doc)
    return {"message": "Journal saved", "id": str(result.inserted_id)}

@app.get("/history")
async def get_history():
    cursor = db.entries.find().sort("timestamp", -1)
    history = []
    async for doc in cursor:
        doc["id"] = str(doc.pop("_id"))
        history.append(doc)
    return {"entries": history}