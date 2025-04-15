import streamlit as st
import requests
import pandas as pd
#import matplotlib.pyplot as plt

# Set page config
st.set_page_config(page_title="MoodMate Dashboard", layout="wide")

# Sidebar
st.sidebar.title("📘 MoodMate")
st.sidebar.markdown("Welcome back! Here’s how your emotions have been trending.")

# Fetch mood trend data
API_URL = "https://moodmate-api-g9e0.onrender.com/mood-trends" 
response = requests.get(API_URL)

if response.status_code != 200:
    st.error("Failed to fetch mood data from API.")
    st.stop()

data = response.json()
dates = data.pop("dates")
df = pd.DataFrame(data, index=dates)

# Allow emotion selection
st.sidebar.markdown("### Select Emotions")
selected_emotions = st.sidebar.multiselect(
    "Which emotions do you want to track?",
    options=df.columns.tolist(),
    default=df.columns.tolist()
)

# Filtered chart data
filtered_df = df[selected_emotions]

st.markdown("### 📝 Add a New Journal Entry")
journal_text = st.text_area("Write what's on your mind...", height=150)

if st.button("Analyze and Save Entry"):
    if not journal_text.strip():
        st.warning("Please enter some text first.")
    else:
        result = requests.post(
            f"{API_URL.replace('/mood-trends', '')}/journal",
            json={"text": journal_text}
        )

        if result.status_code == 200:
            res_data = result.json()
            st.success("Journal saved!")
            st.markdown(f"**Emotions Detected:**")
            st.json(res_data)  # Show the raw API response
            for emo in res_data["emotions"]:
                st.markdown(f"- {emo['label']}: {round(emo['score'], 2)}")

            st.markdown("**MoodMate’s Response:**")
            st.info(res_data["reply"])
        else:
            st.error("Something went wrong while saving.")


# Line chart
st.title("📈 Mood Trends Over Time")
st.line_chart(filtered_df)

# Data Summary
st.markdown("---")
st.markdown("### 📊 Summary Stats")

summary = df.describe().transpose()[["mean", "max", "min"]].round(2)
st.dataframe(summary.rename(columns={
    "mean": "Average",
    "max": "Peak",
    "min": "Lowest"
}))

st.markdown("### 📅 Weekly Mood Highlights")

# Get latest 7 days
recent_df = df.tail(7)

# Most felt emotion (highest average)
most_felt = recent_df.mean().idxmax()
happiest_day = recent_df["joy"].idxmax() if "joy" in recent_df.columns else "N/A"

col1, col2 = st.columns(2)
col1.metric("Most Felt Emotion (7d)", most_felt.capitalize())
col2.metric("Happiest Day", happiest_day)

