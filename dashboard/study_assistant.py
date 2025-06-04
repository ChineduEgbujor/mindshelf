import fitz  # PyMuPDF
import streamlit as st
from app.study import summarize_content, generate_flashcards

def show_study_assistant():
    st.title("📚 MindShelf — Study Assistant")

    uploaded_pdf = st.file_uploader("Upload PDF (slides, textbook, etc.)", type="pdf")
    if uploaded_pdf:
        doc = fitz.open(stream=uploaded_pdf.read(), filetype="pdf")
        raw_text = "".join(page.get_text() for page in doc)
        
        st.success("Document loaded!")
        st.text_area("📄 Text Preview", raw_text[:1000] + "...", height=200)

        if st.button("Generate Summary Notes"):
            with st.spinner("Summarizing..."):
                notes = summarize_content(raw_text)
                st.markdown("### 📝 AI-Generated Notes")
                st.markdown(notes)

        if st.button("Generate Flashcards"):
            with st.spinner("Generating flashcards..."):
                cards = generate_flashcards(raw_text)
                st.markdown("### 🧠 AI-Generated Flashcards")
                st.text_area("Flashcards", cards, height=300)

# def extract_text_from_pdf(file):
#     doc = fitz.open(stream=file.read(), filetype="pdf")
#     text = ""
#     for page in doc:
#         text += page.get_text()
#     return text

# st.title("📚 Study Assistant")

# uploaded_pdf = st.file_uploader("Upload lecture slides or textbook (PDF)", type="pdf")

# if uploaded_pdf:
#     doc = fitz.open(stream=uploaded_pdf.read(), filetype="pdf")
#     raw_text = "".join(page.get_text() for page in doc)
    
#     st.success("Document loaded!")
#     st.text_area("📄 Text Preview", raw_text[:1000] + "...", height=200)

#     if st.button("Generate Summary Notes"):
#         with st.spinner("Summarizing..."):
#             notes = summarize_content(raw_text)
#             st.markdown("### 📝 AI-Generated Notes")
#             st.markdown(notes)

#     if st.button("Generate Flashcards"):
#         with st.spinner("Generating flashcards..."):
#             flashcards = generate_flashcards(raw_text)
#             st.markdown("### 🧠 AI-Generated Flashcards")
#             st.text_area("Flashcards", flashcards, height=300)
