import streamlit as st
import json
from dotenv import load_dotenv
import os
import random
import speech_recognition as sr

# Load environment variables
load_dotenv()
api_key = os.getenv("API_KEY")

# Load personal data from JSON
with open("data.json") as f:
    personal_data = json.load(f)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "user_name" not in st.session_state:
    st.session_state.user_name = None

if "handled_once" not in st.session_state:
    st.session_state.handled_once = False

# Custom CSS for styling
st.markdown("""
    <style>
        .title-container { text-align: center; padding: 15px; background-color: #ffc0cb; color: black; font-size: 26px; border-radius: 10px; }
        .description { text-align: center; font-size: 16px; color: #333; margin-bottom: 15px; }
        .chat-container { max-width: 700px; margin: 0 auto; padding: 10px; border-radius: 15px; box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1); }
        .message { display: flex; align-items: flex-start; margin-bottom: 10px; }
        .user-message { justify-content: flex-end; text-align: right; }
        .assistant-message { justify-content: flex-start; text-align: left; }
        .bubble { padding: 12px 15px; border-radius: 20px; font-size: 14px; max-width: 70%; box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.1); }
        .user-message .bubble { background-color: #fff5f5; color: black; }
        .assistant-message .bubble { background-color: #ffc0cb; color: black; }
        .input-container { position: fixed; bottom: 0; left: 0; right: 0; padding: 10px 15px; display: flex; align-items: center; background-color: white; }
    </style>
""", unsafe_allow_html=True)

# Title and description
st.markdown("<div class='title-container'>E-Ambulance 1122</div>", unsafe_allow_html=True)
st.markdown("<div class='description'>This chatbot is for your convenience. Feel free to ask anything about the E-Ambulance service.</div>", unsafe_allow_html=True)

# Sidebar for chat history
with st.sidebar:
    st.markdown("## Chat History")
    if st.session_state.messages:
        for message in st.session_state.messages:
            role = "User" if message["role"] == "user" else "Bot"
            st.write(f"{role}: {message['content']}")

# Function to fetch contact information from JSON
def fetch_contact_info():
    contact_details = personal_data.get("contact_details", {})
    phone_number = contact_details.get("phone", "Phone number not available")
    email = contact_details.get("email", "Email not available")
    address = contact_details.get("address", "Address not available")
    return f"📞 {phone_number}, 📧 {email}, 🏠 {address}."

# Function to handle user input
def handle_input():
    if st.session_state.handled_once:
        st.session_state.handled_once = False
        return

    user_input = st.session_state.get("user_input", "").strip().lower()
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.session_state.handled_once = True

        if user_input in ["hello", "hi", "hey"]:
            response = "Hi! How can I assist you today? 😊"

        elif "my name is" in user_input:
            user_name = user_input.split("my name is")[-1].strip().capitalize()
            st.session_state.user_name = user_name
            response = f"Hello {user_name}! It's nice to meet you. How can I assist you today?"

        elif "remember my name" in user_input:
            if st.session_state.user_name:
                response = f"Yes, your name is {st.session_state.user_name}. 😊"
            else:
                response = "I don't know your name yet. Please tell me your name."

        elif "detail" in user_input or "describe" in user_input:
            response = "I cannot take that action, but here are the contact details: " + fetch_contact_info()

        elif "accident" in user_input or "injured" in user_input:
            response = "I'm really sorry to hear that! Please stay calm and dial 1122 immediately. An ambulance will reach you shortly. 🙏"

        elif "free" in user_input:
            response = "Yes, the E-Ambulance service is free for all emergencies. You can call 1122 anytime you need assistance."

        else:
            response = "I'm here to help! Can you rephrase your question, or ask me about the E-Ambulance services? 😊"

        st.session_state.messages.append({"role": "assistant", "content": response})
        st.session_state["user_input"] = ""

# Function for voice-to-text input
def voice_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.toast("Listening... Speak now!")
        try:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio)
            return text
        except Exception:
            return None

# Display chat messages
st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
for message in st.session_state.messages:
    role_class = "user-message" if message["role"] == "user" else "assistant-message"
    icon = "https://img.icons8.com/color/48/000000/ambulance.png" if message["role"] == "user" else "https://img.icons8.com/color/48/000000/robot.png"
    st.markdown(
        f"<div class='message {role_class}'><div class='bubble'>{message['content']}</div><img src='{icon}'></div>" if role_class == "user-message" else
        f"<div class='message {role_class}'><img src='{icon}'><div class='bubble'>{message['content']}</div></div>",
        unsafe_allow_html=True,
    )
st.markdown("</div>", unsafe_allow_html=True)

# Input field
st.markdown("<div class='input-container'>", unsafe_allow_html=True)
col1, col2, col3 = st.columns([8, 1, 1])

with col1:
    st.text_input(
        "",
        placeholder="Type your message here...",
        key="user_input",
        label_visibility="collapsed",
        on_change=handle_input
    )

with col2:
    if st.button("🎙️"):
        user_input = voice_to_text()
        if user_input:
            st.session_state.messages.append({"role": "user", "content": user_input})
            handle_input()

with col3:
    if st.button("➤"):
        handle_input()

st.markdown("</div>", unsafe_allow_html=True)



