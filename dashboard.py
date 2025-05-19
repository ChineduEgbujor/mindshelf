import streamlit as st
import requests
import pandas as pd
import pyrebase

# Set page config
st.set_page_config(page_title="MoodMate Dashboard", layout="wide")

firebase_config = {
  "apiKey": "AIzaSyDL2GeCXo5BRoLzQ0r4aKLl0eoF0Q-yhB0",
  "authDomain": "moodmate-d9029.firebaseapp.com",
  "projectId": "moodmate-d9029",
  "storageBucket": "moodmate-d9029.firebasestorage.app",
  "messagingSenderId": "300158858256",
  "appId": "1:300158858256:web:797bd70b534c0a75a0c695",
  "measurementId": "G-3LLJ4RW9MG",
  "databaseURL": "https://moodmate-d9029-default-rtdb.firebaseio.com/"
}


firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()

# Session state for user and auth UI
if "user" not in st.session_state:
    st.session_state.user = None
if "show_auth_ui" not in st.session_state:
    st.session_state.show_auth_ui = True

# Only show Auth UI if not logged in
if st.session_state.show_auth_ui:
    st.sidebar.title("🔐 Login / Sign Up")
    auth_mode = st.sidebar.radio("Select mode", ["Login", "Sign Up"])
    
    email = st.sidebar.text_input("Email")
    password = st.sidebar.text_input("Password", type="password")

    if auth_mode == "Login":
        if st.sidebar.button("Login"):
            try:
                user = auth.sign_in_with_email_and_password(email, password)
                st.session_state.user = user
                st.session_state.token = user['idToken']
                st.session_state.show_auth_ui = False  # Hide auth UI after login
                st.success("Logged in!")
                st.rerun()  # Refresh the page
            except:
                st.error("Login failed")
    else:
        if st.sidebar.button("Sign Up"):
            try:
                user = auth.create_user_with_email_and_password(email, password)
                st.success("Account created! You can now log in.")
            except:
                st.error("Signup failed")

# Add logout button when logged in
if st.session_state.user and not st.session_state.show_auth_ui:
    if st.sidebar.button("Logout"):
        st.session_state.user = None
        st.session_state.token = None
        st.session_state.show_auth_ui = True
        st.rerun()

# Only show app after login
if not st.session_state.user:
    st.stop()



# Modified API calls with authentication
def fetch_authenticated(endpoint, method="GET", json=None):
    if not st.session_state.user:
        raise Exception("Not authenticated")
        
    headers = {
        "Authorization": st.session_state.token
    }
    
    url = f"{API_URL.replace('/mood-trends', '')}/{endpoint}"
    
    if method == "GET":
        return requests.get(url, headers=headers)
    elif method == "POST":
        return requests.post(url, headers=headers, json=json)

# Sidebar
st.sidebar.title("📘 MoodMate")
st.sidebar.markdown("Welcome back! Here’s how your emotions have been trending.")

# Fetch mood trend data
# API_URL = "http://localhost:8000/mood-trends" # For local testing
API_URL = "https://moodmate-api-g9e0.onrender.com/mood-trends"

try:
    response = fetch_authenticated('mood-trends')
    if response.status_code == 401:
        st.error("Session expired. Please log in again.")
        st.session_state.user = None
        st.stop()
    elif response.status_code != 200:
        st.error("Failed to fetch mood data from API.")
        st.stop()
        
    data = response.json()
    has_mood_data = bool(data)
    
    if has_mood_data:
        # Handle the case where dates might be missing
        if "dates" in data:
            dates = data.pop("dates")
            df = pd.DataFrame(data, index=dates)
        else:
            df = pd.DataFrame(data)
    else:
        st.info("No mood data available yet. Try adding some journal entries!")
        df = pd.DataFrame()  # Empty DataFrame
        print(df)
    
except Exception as e:
    st.error(f"Error processing mood data: {str(e)}")
    st.write("Response content:", response.content if 'response' in locals() else "No response")
    df = pd.DataFrame()  # Empty DataFrame

# Show journal entry section regardless of mood data
st.markdown("### 📝 Add a New Journal Entry")
journal_text = st.text_area("Write what's on your mind...", height=150)

if st.button("Analyze and Save Entry"):
    if not journal_text.strip():
        st.warning("Please enter some text first.")
    else:
        try:
            result = fetch_authenticated(
                'journal',
                method="POST",
                json={"text": journal_text}
            )

            if result.status_code == 200:
                res_data = result.json()
                st.success("Journal saved!")
                st.markdown(f"**Emotions Detected:**")
                for emo in res_data["emotions"]:
                    st.markdown(f"- {emo['label']}: {round(emo['score'], 2)}")

                st.markdown("**MoodMate's Response:**")
                st.info(res_data["reply"])
                st.rerun() # Refresh the page to show new data
            else:
                st.error("Something went wrong while saving.")
        except Exception as e:
            st.error(f"Error: {str(e)}")

# Only show visualizations if we have data
if not df.empty:
    # Allow emotion selection
    st.sidebar.markdown("### Select Emotions")
    selected_emotions = st.sidebar.multiselect(
        "Which emotions do you want to track?",
        options=df.columns.tolist(),
        default=df.columns.tolist()
    )

    # Filtered chart data
    filtered_df = df[selected_emotions]

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

headers = {"Authorization": st.session_state.token}
streak_res = requests.get(f"{API_URL.replace('/mood-trends', '')}/streak", headers=headers).json()

st.sidebar.markdown("### 🔥 Your Streak")
st.sidebar.metric("Days in a row", streak_res["streak"])
if not streak_res["journaled_today"]:
    st.sidebar.warning("You haven't journaled yet today!")
else:
    st.sidebar.success("✅ Journaled today!")

