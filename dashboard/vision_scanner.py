# dashboard/vision_scanner.py
import streamlit as st
import requests
import base64
from PIL import Image
import io

API_URL_BASE = "http://localhost:8000"  # Adjust this URL according to your backend API

def show_vision_scanner():
    st.title("📷 MindShelf — Clutter Scanner")

    uploaded_file = st.file_uploader("Upload a photo of your workspace", type=["jpg", "jpeg", "png"])
    if not uploaded_file:
        st.info("Please upload an image to analyze.")
        return

    # Display preview
    st.image(uploaded_file, caption="Original Image", use_container_width=True)

    if st.button("Analyze Clutter"):
        with st.spinner("Detecting objects..."):
            # Call backend API
            files = {"image": uploaded_file.getvalue()}
            response = requests.post(
                f"{API_URL_BASE}/detect-clutter",
                files={"image": ("workspace.jpg", uploaded_file.getvalue(), uploaded_file.type)}
            )

            if response.status_code != 200:
                st.error("Failed to analyze image.")
                return

            data = response.json()
            counts = data["counts"]
            encoded_img = data["annotated_image"]

            st.markdown("### 🗂️ Detected Items")
            if counts:
                for item, cnt in counts.items():
                    st.markdown(f"- **{item.capitalize()}**: {cnt}")
            else:
                st.markdown("No desk items detected. Try a different angle or better lighting.")

            # Decode and display annotated image
            annotated_bytes = base64.b64decode(encoded_img)
            annotated_img = Image.open(io.BytesIO(annotated_bytes))
            st.image(annotated_img, caption="Annotated Image", use_container_width=True)
