# MindShelf

**MindShelf** is an AI-powered mental wellness and productivity companion that integrates three core modules:

- **Emotional Journaling & Mood Tracking**
- **Study Assistant (PDF Summarization & Flashcards)**
- **Vision-Based Clutter Detection (Workspace Scanner)**

This full-stack application demonstrates a seamless blend of NLP, computer vision, and secure user management. Users can journal their thoughts, get AI-generated emotional insights, upload study materials for automated note-taking and flashcard generation, and even scan their physical workspace for clutter.

---

## 🚀 Features

### 1. Emotional Journaling & Mood Tracking

- **Secure Sign-In (Firebase Auth)**  
  Each user logs in with email/password (or Google) and receives a Firebase ID token.
- **AI-Powered Emotion Classification**  
  DistilBERT (fine-tuned on GoEmotions) analyzes journal entries to identify core emotions (joy, sadness, anger, fear, surprise, love, etc.).
- **Empathetic AI Responses (Gemini)**  
  Google Gemini generates tailored, supportive replies in under 500 ms for every journal entry.
- **Mood Trend Dashboard**  
  Streamlit UI visualizes daily emotion averages, weekly summaries, and historical trends.
- **Streak Tracking & Daily Goal**  
  Users see their consecutive-day journaling streak and receive a “journaled today?” reminder.

### 2. Study Assistant

- **PDF Upload & Text Extraction**  
  Users can upload lecture slides or textbooks (PDF), which are parsed using PyMuPDF.
- **AI-Generated Summaries (Gemini)**  
  Cornell-style notes are automatically generated for each uploaded document.
- **Flashcard Creation (Gemini)**  
  Extracted text is converted into quiz-style Q&A flashcards for self-testing.
- **Interactive Streamlit Interface**  
  Simple buttons let users trigger summarization or flashcard generation and view results inline.

### 3. Vision-Based Clutter Detection

- **Workspace Photo Upload**  
  Users upload a photo (JPG/PNG) of their desk or any workspace.
- **Object Detection (YOLOv5)**  
  A pretrained YOLOv5s model identifies common desk items (books, cups, laptops, etc.) and returns a clutter count.
- **Annotated Image & Clutter Score**  
  The app draws bounding boxes around detected objects, displays counts per class, and can compute a simple “clutter score” or offer basic organization tips.
- **Streamlit UI for Clutter Scanner**  
  Users see the original image, an annotated version, and a summary of detected items.

---

## 📂 Project Structure

```
mindshelf/
├── app/                      # Core backend application
│   ├── main.py              # FastAPI application & routes
│   ├── model.py             # Emotion analysis model
│   ├── gemini.py            # Gemini API integration
│   ├── study.py             # Study assistant functions
│   ├── vision.py            # YOLOv5 detection logic
│   └── firebase_admin.py    # Firebase authentication
├── dashboard/               # Streamlit frontend
│   ├── dashboard.py         # Main dashboard UI
│   ├── study_assistant.py   # Study tools interface
│   └── vision_scanner.py    # Clutter detection UI
├── .streamlit/              # Streamlit configuration
├── .env                     # Environment variables
└── requirements.txt         # Project dependencies
```

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- MongoDB
- Firebase account
- Gemini API key

### Installation

1. Clone the repository

```bash
git clone https://github.com/ChineduEgbujor/mindshelf.git
cd mindshelf
```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Configure environment variables in `.env`:

```
MONGO_URI=your_mongodb_uri
GEMINI_API_KEY=your_gemini_api_key
FIREBASE_CREDENTIALS_PATH=path_to_firebase_credentials.json
```

4. The YOLOv5 model file (yolov5su.pt) will be automatically downloaded on first run, or you can manually download it:

```bash
# Optional manual download
wget https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov5su.pt
```

### Running the Application

1. Start the FastAPI backend:

```bash
uvicorn app.main:app --reload
```

2. Launch the Streamlit dashboard:

```bash
streamlit run streamlit_app.py
```

## 🔑 API Routes

- `POST /journal` - Save a new journal entry
- `POST /analyze` - Analyze emotions in text
- `GET /history` - Retrieve journal history
- `POST /study/summarize` - Generate study notes
- `POST /vision/detect` - Analyze workspace clutter

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License.

## 👥 Authors

- Chinedu Egbujor

## 🙏 Acknowledgments

- Google Gemini for AI text generation
- Ultralytics for YOLOv5
- Hugging Face for DistilBERT
