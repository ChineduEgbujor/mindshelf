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
