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
#adding labels
labels = {
    "English": {
        "edu_advice": "📚 Get advice in specific education categories",
        "choose_category": "Choose a Category:",
        "ask_question": "Ask your question:",
        "get_answer": "Get Answer",
        "warning": "Please enter a question.",
        "generating": "Generating response...",
        "answer": "Answer:"
    },
    "ಕನ್ನಡ": {
        "edu_advice": "📚 ನಿರ್ದಿಷ್ಟ ಶಿಕ್ಷಣ ವರ್ಗಗಳಲ್ಲಿ ಸಲಹೆ ಪಡೆಯಿರಿ",
        "choose_category": "ವರ್ಗವನ್ನು ಆಯ್ಕೆಮಾಡಿ:",
        "ask_question": "ನಿಮ್ಮ ಪ್ರಶ್ನೆಯನ್ನು ಕೇಳಿ:",
        "get_answer": "ಉತ್ತರವನ್ನು ಪಡೆಯಿರಿ",
        "warning": "ದಯವಿಟ್ಟು ಪ್ರಶ್ನೆಯನ್ನು ನಮೂದಿಸಿ.",
        "generating": "ಉತ್ತರವನ್ನು ರಚಿಸಲಾಗುತ್ತಿದೆ...",
        "answer": "ಉತ್ತರ:"
    }
}

if mode == "Science Chatbot for Kids":
    if "science_chat" not in st.session_state:
        st.session_state.science_chat = science_model.start_chat(history=[])

   

    # Show chat history
    for msg in st.session_state.science_chat.history:
        with st.chat_message("user" if msg.role == "user" else "assistant"):
            st.markdown(msg.parts[0].text)

    # Chat input
    user_input = st.chat_input("Ask me anything science-y!")

    if user_input:
        with st.chat_message("user"):
            st.markdown(user_input)

        response = st.session_state.science_chat.send_message(user_input)

        with st.chat_message("assistant"):
            st.markdown(response.text)
#added chats
else:
    st.subheader(labels[mode]["edu_advice"])

    category = st.selectbox(labels[mode]["choose_category"], ["", "Primary", "High School", "PUC", "Engineering", "Finance", "MBBS"])
    user_prompt = st.text_area(labels[mode]["ask_question"])

    if st.button(labels[mode]["get_answer"]):
        if not user_prompt.strip():
            st.warning(labels[mode]["warning"])
        else:
            with st.spinner(labels[mode]["generating"]):
                reply = get_gemini_response(user_prompt, category)
                st.success(labels[mode]["answer"])
                st.markdown(reply)


if "public_key" not in st.session_state:
    public_key, private_key = paillier.generate_paillier_keypair()
    st.session_state.public_key = public_key
    st.session_state.private_key = private_key

if "encrypted_transactions" not in st.session_state:
    st.session_state.encrypted_transactions = {}

if "transaction_history" not in st.session_state:
    st.session_state.transaction_history = []

if "wallet" not in st.session_state:
    st.session_state.wallet = []
if "last_passkey_change_time" not in st.session_state:
    st.session_state.last_passkey_change_time = time.time()

if "encryption_method" not in st.session_state:
    st.session_state.encryption_method = "HE"

if "user_authenticated" not in st.session_state:
    st.session_state.user_authenticated = False

if "user_id" not in st.session_state:
    st.session_state.user_id = ""

if "pan_no" not in st.session_state:
    st.session_state.pan_no = ""


def encrypt_data(data):
    if st.session_state.encryption_method == "HE":
        encrypted_data = st.session_state.public_key.encrypt(float(data))
    elif st.session_state.encryption_method == "FFHE":
        encrypted_data = encrypt_data_fhe(data)
    return encrypted_data

#added to states
def decrypt_data(encrypted_data):
    if st.session_state.encryption_method == "HE":
        return st.session_state.private_key.decrypt(encrypted_data)
    elif st.session_state.encryption_method == "FFHE":
        return decrypt_data_fhe(encrypted_data)


def encrypt_data_fhe(data):
    return data


def decrypt_data_fhe(encrypted_data):
    return encrypted_data


def get_current_passkey():
    elapsed_time = time.time() - st.session_state.last_passkey_change_time
    if elapsed_time > 300:
        st.session_state.last_passkey_change_time = time.time()
        return "sit4321" if (int(elapsed_time / 300) % 2 == 1) else "sit1234"
    else:
        return "sit1234" if (int(elapsed_time / 300) % 2 == 0) else "sit4321"


def display_countdown():
    elapsed_time = time.time() - st.session_state.last_passkey_change_time
    remaining_time = 300 - elapsed_time
    if remaining_time > 0:
        st.write(f"Time until next passkey change: {int(remaining_time)} seconds")
    else:
        st.write("Passkey has been updated!")


def check_network_traffic():
    network_stats = psutil.net_io_counters()
    bytes_sent = network_stats.bytes_sent / (1024 * 1024)
    bytes_recv = network_stats.bytes_recv / (1024 * 1024)
    total_network_traffic = bytes_sent + bytes_recv
    return total_network_traffic

