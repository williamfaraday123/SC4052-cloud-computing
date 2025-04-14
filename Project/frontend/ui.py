import streamlit as st
import requests
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

# Retrieve the backend URL from the environment variables
BACKEND_URL = os.getenv("BACKEND_URL")

st.title("Coding-as-a-Service Demo")
prompt = st.text_area("Enter your code prompt: (for Python code)")

if st.button("Generate Code"):
    if not prompt.strip():
        st.error("Prompt cannot be empty")
    elif BACKEND_URL:  # Ensure BACKEND_URL is available
        try:
            response = requests.post(f"{BACKEND_URL}/generate", json={"prompt": prompt})
            if response.status_code == 200:
                st.code(response.json().get("generated_code", "Error: Unable to generate code."))
            else:
                st.error(f"Error {response.status_code}: {response.text}")
        except requests.exceptions.RequestException as e:
            st.error(f"Error connecting to backend: {e}")
    else:
        st.error("Backend URL is not set. Check your .env file.")