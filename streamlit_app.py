import streamlit as st

# import your “page” modules
from dashboard.dashboard import show_journaling_dashboard
from dashboard.study_assistant import show_study_assistant
from dashboard.vision_scanner import show_vision_scanner

st.set_page_config(page_title="MindShelf", layout="wide")

# Sidebar navigation
st.sidebar.title("📚 MindShelf")
page = st.sidebar.radio(
    "Go to",
    ["Journaling & Mood", "Study Assistant", "Clutter Scanner"]
)

if page == "Journaling & Mood":
    show_journaling_dashboard()

elif page == "Study Assistant":
    show_study_assistant()

else:
    show_vision_scanner()
