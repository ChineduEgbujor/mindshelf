# MoodMate API

This is the backend API for MoodMate, an AI-powered mental health journaling assistant.

## Features

- Accepts journal text input
- Returns emotion scores using a HuggingFace model

## Run Locally

```bash
python3 -m venv venv
source venv/bin/activate  # or .\venv\Scripts\activate on Windows

pip install -r requirements.txt
uvicorn app.main:app --reload
```

## MongoDB Setup

Create a `.env` file in the root with:

```
MONGO_URI=mongodb+srv://<your-cluster-uri>
```

Or use `mongodb://localhost:27017` if running locally.

Visit `http://127.0.0.1:8000/docs` to test the API via Swagger UI.
