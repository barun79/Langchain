import streamlit as st
import sys
import os

# Add parent directory to the module search path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from model import generate_restaurant_data

st.title("🍽️ Restaurant Brand Generator")

cuisine = st.text_input("Enter Cuisine (e.g., Nepali, Italian, Indian):")
tone = st.selectbox("Pick a tone for the brand:", ["Funny", "Elegant", "Bold", "Traditional", "Modern"])

if st.button("Generate"):
    if cuisine and tone:
        with st.spinner("Generating..."):
            result = generate_restaurant_data(cuisine, tone)

        st.subheader("📛 Name")
        st.write(result["restaurant_name"])

        st.subheader("📝 Description")
        st.write(result["description"])

        st.subheader("🥘 Menu")
        st.text(result["menu"])

        st.subheader("🎯 Slogan")
        st.write(result["slogan"])
    else:
        st.warning("Please enter both a cuisine and select a tone.")
