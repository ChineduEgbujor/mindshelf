from google import genai
import os
from dotenv import load_dotenv
import logging

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY)

logger = logging.getLogger(__name__)

def generate_empathetic_reply(journal_text: str) -> str:
    prompt = f"""You are an empathetic mental health companion named MoodMate. 
    A user wrote this journal entry:

    "{journal_text}"

    Please respond kindly and supportively, offering comfort or advice if appropriate."""
    
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[prompt])
        return response.text.strip()
    except Exception as e:
        logger.error(f"[Gemini Error] {e}")
        return "I'm here for you. I'm having trouble formulating a thoughtful reply right now, but you're not alone."
