from collections import defaultdict
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from app.model import analyze_emotions
import motor.motor_asyncio
import os
from dotenv import load_dotenv
from app.gemini import generate_empathetic_reply


load_dotenv()

app = FastAPI()

# MongoDB setup
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")

print("Mongo URI:", MONGO_URI)
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
    try:
        # Check if exact entry exists already
        existing = await db.entries.find_one({"text": entry.text})
        if existing:
            return {
                "message": "Journal already exists",
                "id": str(existing["_id"]),
                "emotions": existing["emotions"],
                "reply": existing["reply"]  # Corrected key from "response" to "reply"
            }
        
        #Analyze emotions and generate a reply
        emotions = analyze_emotions(entry.text)
        reply = generate_empathetic_reply(entry.text)
        
        # Save the journal entry with emotions and reply
        doc = {
            "text": entry.text,
            "emotions": emotions,
            "reply": reply,
            "timestamp": datetime.utcnow()
        }
        result = await db.entries.insert_one(doc)
        return {
            "message": "Journal saved",
            "id": str(result.inserted_id),
            "reply": reply
        }
    except Exception as e:
        print(f"[ERROR] Failed to save journal: {e}")
        raise HTTPException(status_code=500, detail="Something went wrong while processing your journal.")

@app.get("/history")
async def get_history():
    cursor = db.entries.find().sort("timestamp", -1)
    history = []
    async for doc in cursor:
        doc["id"] = str(doc.pop("_id"))
        history.append(doc)
    return {"entries": history}

@app.get("/mood-trends")
async def get_mood_trends():
    cursor = db.entries.find()
    emotion_data = defaultdict(lambda: defaultdict(list))  # {date: {emotion: [scores]}}

    async for doc in cursor:
        date_str = doc["timestamp"].strftime("%Y-%m-%d")
        for emotion in doc["emotions"]:
            emotion_data[date_str][emotion["label"]].append(emotion["score"])

    # Aggregate by average per day
    trends = defaultdict(list)
    sorted_dates = sorted(emotion_data.keys())

    all_emotions = set()
    for day_emotions in emotion_data.values():
        all_emotions.update(day_emotions.keys())

    for date in sorted_dates:
        trends["dates"].append(date)
        for emotion in all_emotions:
            scores = emotion_data[date].get(emotion, [])
            avg_score = sum(scores) / len(scores) if scores else 0.0
            trends[emotion].append(round(avg_score, 3))

    return JSONResponse(content=trends)