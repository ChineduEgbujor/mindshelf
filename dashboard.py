import streamlit as st
import requests
import pandas as pd
#import matplotlib.pyplot as plt

st.set_page_config(page_title="MoodMate Dashboard", layout="centered")

st.title("📈 Mood Trends")
st.markdown("Track how your emotions have changed over time.")

# Call the backend
API_URL = "https://moodmate-api-g9e0.onrender.com/mood-trends"
response = requests.get(API_URL)

if response.status_code == 200:
    data = response.json()
    dates = data.pop("dates")
    df = pd.DataFrame(data, index=dates)

    st.line_chart(df)
else:
    st.error("Failed to fetch mood data. Make sure your backend is running.")
