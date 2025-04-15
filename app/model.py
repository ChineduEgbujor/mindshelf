from transformers import pipeline

# Load once at startup
emotion_classifier = pipeline("text-classification", model="bhadresh-savani/distilbert-base-uncased-emotion", top_k=None)

def analyze_emotions(text: str):
    results = emotion_classifier(text)[0]
    return sorted(results, key=lambda x: -x['score'])