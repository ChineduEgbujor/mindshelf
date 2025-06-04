from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY)

def summarize_content(text):
    prompt = f"""You are an AI study assistant. Summarize the following text into Cornell-style notes with clear headers and bullet points.

    Text:
    {text[:3000] }  # Keep token limit safe
    """

   
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[prompt])
        return response.text.strip()
    except Exception as e:
        return f"Failed to summarize: {e}"

def generate_flashcards(text):
    prompt = f"""Extract 5 flashcard-style questions and answers from the following content:
    
    Text:
    {text[:3000]}
    
    Format: 
    Q: ...
    A: ...
    """

    
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[prompt])
        return response.text.strip()
    except Exception as e:
        return f"Failed to generate flashcards: {e}"
