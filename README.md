# MoodMate API

This is the backend API for MoodMate, an AI-powered mental health journaling assistant.

## Features

- Accepts journal text input
- Returns emotion scores using a HuggingFace model
- Saves journal entries to MongoDB
- Provides history endpoint to retrieve past entries
- Generates empathetic replies using Gemini Pro
- Display a visual trend chart of emotions

## Run Locally

```bash
python3 -m venv venv
source venv/bin/activate  # or .\venv\Scripts\activate on Windows

pip install -r requirements.txt
uvicorn app.main:app --reload
```

To run the visual frontend chart to visualize mood trends in the root directory:

```
streamlit run dashboard.py
```

## Environment Variables

Create a `.env` file in the root with:

```
MONGO_URI=mongodb+srv://<your-cluster-uri>
GEMINI_API_KEY=your_gemini_api_key
```

Or use `mongodb://localhost:27017` if running locally.

Visit `http://127.0.0.1:8000/docs` to test the API via Swagger UI.
