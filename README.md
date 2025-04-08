# MoodMate API - Phase 1

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

Visit `http://127.0.0.1:8000/docs` to test the API via Swagger UI.
