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
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! Welcome to the E-Ambulance 1122 chatbot. How can I assist you today? 😊"}
    ]
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

# Pre-defined responses
greetings = ["Hi! How can I assist you today? 😊", "Hello! How can I help you today?", "Welcome! What can I do for you today?"]
help_responses = ["Of course, I'm here for you. Let me know what you need!", "I'm ready to assist! Please tell me more.", "I'm here to help you! 😊"]

# Function to handle user input
def handle_input():
    # Avoid duplicate processing
    if st.session_state.handled_once:
        st.session_state.handled_once = False
        return

    user_input = st.session_state.get("user_input", "").strip().lower()
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.session_state.handled_once = True

        # Handle greetings
        if user_input in ["hello", "hi", "hey"]:
            response = random.choice(greetings)

        # Handle "my name is" and remember user name
        elif "my name is" in user_input:
            user_name = user_input.split("my name is")[-1].strip().capitalize()
            st.session_state.user_name = user_name
            response = f"Hello {user_name}! It's nice to meet you. How can I assist you today? 😊"

        # Handle name-related queries
        elif "do you remember my name" in user_input or "did you remember my name" in user_input:
            if st.session_state.user_name:
                response = f"Yes, I remember your name! Your name is {st.session_state.user_name}. 😊"
            else:
                response = "I don't seem to remember your name yet. Could you remind me?"

        # Handle emergency-related requests
        elif "blind" in user_input or "need help" in user_input:
            response = "I'm so sorry to hear that. Please stay calm. If you need immediate help, call 1122 or ask someone nearby to assist you. Let me know if I can provide more information. 🙏"

        elif "road accident" in user_input or "injured" in user_input:
            response = "I'm really sorry to hear that! Please stay calm. An ambulance is on its way when you call 1122. Can I help you with anything else in the meantime? 🙏"

        # Handle details about the E-Ambulance service
        elif "details" in user_input or "e-ambulance" in user_input or "what is e-ambulance" in user_input:
            response = "The E-Ambulance 1122 service provides 24/7 emergency medical assistance. It’s free and ensures quick response during medical emergencies. You can call 1122 anytime."

        # Handle "is the service free"
        elif "free" in user_input:
            response = "Yes, the E-Ambulance service is completely free for all emergencies. You can call 1122 anytime you need medical assistance."

        # Handle fallback queries
        else:
            response = "I didn't quite understand that. Can you rephrase your question? Or ask about the E-Ambulance 1122 services. 😊"

        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.session_state["user_input"] = ""  # Reset user input field
        st.session_state.handled_once = False

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
        except Exception as e:
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

# Input and buttons for sending messages
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
