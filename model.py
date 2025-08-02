import streamlit as st
from google import generativeai as genai
from config import MODEL_ID

class ChatModel:
    def __init__(self, api_key: str):
        try:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel(MODEL_ID)
        except Exception as e:
            st.error(f"Failed to initialize Gemini model: {e}")
            self.model = None

    def generate_response(self, prompt: str) -> str:
        if not self.model:
            return "Gemini model is not initialized."

        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error generating response: {e}"
