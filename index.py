#for BGSCET hackathon by team codesmith...Had a wonderfull experiencespo
import streamlit as st
from phe import paillier
import time
import matplotlib.pyplot as plt
import numpy as np
import psutil
from cryptography.fernet import Fernet  # For file-based encryption
import google.generativeai as genai
from gtts import gTTS
import streamlit.components.v1 as components


GOOGLE_API_KEY = "AIzaSyAFpPYDM2ynL6r7KfFQyQnIzYfIsxtiZ4I"
genai.configure(api_key=GOOGLE_API_KEY)

# Model configuration
generation_config = {
    "temperature": 0,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

# Science-focused model setup
science_model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config=generation_config,
    safety_settings=safety_settings,
    system_instruction=(
        "You are an expert at teaching science to kids. Your task is to engage in conversations "
        "about science and answer questions. Explain scientific concepts so that they are easily "
        "understandable. Use analogies and examples that are relatable. Use humor and make the "
        "conversation both educational and interesting. Ask questions so that you can better "
        "understand the user and improve the educational experience. Suggest ways that these concepts "
        "can be related to the real world with observations and experiments."
    )
)

def play_audio(letter):
    audio_html = f"""
    <audio id="{letter}_audio" src="audio/{letter.lower()}.mp3"></audio>
    <script>
        const button = document.getElementById("{letter}_button");
        if (button) {{
            button.onclick = () => {{
                const audio = document.getElementById("{letter}_audio");
                audio.play();
            }};
        }}
    </script>
    <button id="{letter}_button" style="font-size:24px;">🔊 {letter}</button>
    """
    components.html(audio_html, height=100)





# 🧠 Generic educational model for category-based advice
def get_gemini_response(prompt, category=None):
    generic_model = genai.GenerativeModel("gemini-1.5-pro")
    full_prompt = f"You are an educational advisor. {f'Focus on {category} education.' if category else ''} Answer this: {prompt}"
    try:
        response = generic_model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

# Streamlit UI Setup
st.set_page_config(page_title="SAHAYOGI", page_icon="🧠", layout="wide")


# Mode selector
mode = st.radio("Language / ಭಾಷೆ", ["English", "ಕನ್ನಡ"], horizontal=True)
nav_labels = {
    "English": {
        "Primary": "Primary",
        "Higher Studies": "Higher Studies",
        "Home": "Finance",
        "FAQ's": "FAQ's",
        "Support": "Support",
        "Settings": "Settings",
        "Graph Chart": "Graph Chart",
        "Spending Analysis": "Spending Analysis",
        "Encrypted Data": "Encrypted Data",
        "Wallet": "Wallet",
        "Credential Encryption": "Credential Encryption",
        "Withdraw": "Withdraw",
        "Logout": "Logout"
    },
    "ಕನ್ನಡ": {
        "Primary": "ಪ್ರಾಥಮಿಕ",
        "Higher Studies": "ಉನ್ನತ ಅಧ್ಯಯನ",
        "Home": "ಹಣಕಾಸು",
        "FAQ's": "ಸಮಸ್ಯೆಗಳು",
        "Support": "ಬೆಂಬಲ",
        "Settings": "ಸೆಟ್ಟಿಂಗ್‌ಗಳು",
        "Graph Chart": "ಗ್ರಾಫ್ ಚಾರ್ಟ್",
        "Spending Analysis": "ಖರ್ಚು ವಿಶ್ಲೇಷಣೆ",
        "Encrypted Data": "ಎನ್ಕ್ರಿಪ್ಟ್ ಡೇಟಾ",
        "Wallet": "ವಾಲೆಟ್",
        "Credential Encryption": "ಪ್ರಮಾಣಪತ್ರ ಎನ್ಕ್ರಿಪ್ಷನ್",
        "Withdraw": "ಹಿಂತೆಗೆದುಕೊಳ್ಳಿ",
        "Logout": "ಲಾಗ್ ಔಟ್"
    }
}
