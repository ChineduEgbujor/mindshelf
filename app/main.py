from collections import defaultdict
from datetime import datetime, timedelta
from fastapi import File, UploadFile, FastAPI, HTTPException, Request, Header, Form
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel
from app.model import analyze_emotions
import motor.motor_asyncio
import os
import io
from dotenv import load_dotenv
from app.gemini import generate_empathetic_reply
from app.firebase_admin import verify_token
from app.vision import detect_clutter

load_dotenv()

app = FastAPI()

# MongoDB setup
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")

#print("Mongo URI:", MONGO_URI)
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
db = client.moodmate



class JournalEntry(BaseModel):
    text: str

@app.post("/analyze")
def analyze(entry: JournalEntry):
    emotions = analyze_emotions(entry.text)
    return {"emotions": emotions}

@app.post("/journal")
async def save_journal(entry: JournalEntry, authorization: str = Header(None)):
    # Verify Firebase token
    uid = verify_token(authorization)
    if not uid:
        raise HTTPException(status_code=401, detail="Invalid or missing token")
    
    try:
        # Check if exact entry exists already
        existing = await db.entries.find_one({"text": entry.text})
        if existing:
            return {
                "message": "Journal already exists",
                "id": str(existing["_id"]),
                "emotions": existing["emotions"],
                "reply": existing["reply"]  
            }
        
        #Analyze emotions and generate a reply
        emotions = analyze_emotions(entry.text)
        reply = generate_empathetic_reply(entry.text)
        
        # Save the journal entry with emotions and reply
        doc = {
            "user_id": uid,
            "text": entry.text,
            "emotions": emotions,
            "reply": reply,
            "timestamp": datetime.utcnow()
        }
        result = await db.entries.insert_one(doc)
        return {
            "message": "Journal saved",
            "id": str(result.inserted_id),
            "reply": reply,
            "emotions": emotions
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
async def get_mood_trends(authorization: str = Header(None)):
    uid = verify_token(authorization)
    if not uid:
        raise HTTPException(status_code=401, detail="Invalid or missing token")
    cursor = db.entries.find({"user_id": uid})
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

@app.get("/streak")
async def get_streak(authorization: str = Header(None)):
    uid = verify_token(authorization)
    if not uid:
        raise HTTPException(status_code=401, detail="Invalid or missing token")

    cursor = db.entries.find({"user_id": uid}).sort("timestamp", -1)
    dates = []
    async for doc in cursor:
        dates.append(doc["timestamp"].date())

    if not dates:
        return {"streak": 0, "journaled_today": False}

    # Remove duplicates
    dates = sorted(set(dates), reverse=True)

    # Calculate streak
    streak = 0
    today = datetime.utcnow().date()
    expected = today

    for date in dates:
        if date == expected:
            streak += 1
            expected -= timedelta(days=1)
        elif date < expected:
            break  # streak broken

    journaled_today = (dates[0] == today)

    return {
        "streak": streak,
        "journaled_today": journaled_today
    }

@app.post("/detect-clutter")
async def detect_clutter_endpoint(
    image: UploadFile = File(...),
    authorization: str = Header(None)
):
    try:
        # Uncomment when ready to implement auth
        # uid = verify_token(authorization)
        # if not uid:
        #     raise HTTPException(status_code=401, detail="Invalid or missing token")

        # Read uploaded file into bytes
        img_bytes = await image.read()

        # Run detection and await the result
        result = await detect_clutter(img_bytes)

        # Convert result to base64 for JSON response
        import base64
        encoded_image = base64.b64encode(result["annotated_image"]).decode('utf-8')

        return JSONResponse(content={
            "counts": result["counts"],
            "annotated_image": encoded_image,
            "success": True,
            "message": "Clutter detection completed successfully"
        })
    except Exception as e:
        import traceback
        print(f"Error in detect_clutter_endpoint: {str(e)}")
        print(traceback.format_exc())
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": str(e),
                "message": "Failed to process image"
            }
        )
