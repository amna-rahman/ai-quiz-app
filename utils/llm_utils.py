import os
from dotenv import load_dotenv
import google.generativeai as genai
from google.generativeai import GenerativeModel

# Load .env variables
load_dotenv()

# ✅ Configure Gemini using API key from .env
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])


def get_gemini_response(prompt: str) -> str:
    model = GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text
