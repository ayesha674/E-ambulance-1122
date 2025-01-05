import streamlit as st
import json
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
import random  # For varied responses
import speech_recognition as sr  # For voice-to-text

# Load environment variables
load_dotenv()
api_key = os.getenv("API_KEY")

# Load personal data from JSON
with open("data.json") as f:
    personal_data = json.load(f)

# Initialize OpenAI model
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, api_key=api_key)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = [
       
        {"role": "assistant", "content": "Hello! Welcome to the E-Ambulance 1122 chatbot. How can I assist you today? 😊"}
    ]
if "user_name" not in st.session_state:
    st.session_state.user_name = None

# Custom CSS for styling
st.markdown("""
    <style>
        body { font-family: 'Arial', sans-serif; background-color: #fef7f7; margin: 0; padding: 0; }
        .title-container { text-align: center; padding: 15px; background-color: #ffc0cb; color: black; font-size: 26px; border-radius: 10px; margin-bottom: 10px; }
        .description { text-align: center; font-size: 16px; color: #333; margin-bottom: 15px; }
        .chat-container { max-width: 700px; margin: 0 auto; padding: 10px; border-radius: 15px; box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1); background-color: none; }
        .message { display: flex; align-items: flex-start; margin-bottom: 10px; }
        .user-message { justify-content: flex-end; }
        .assistant-message { justify-content: flex-start; }
        .bubble { padding: 12px 15px; border-radius: 20px; font-size: 14px; max-width: 70%; box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.1); }
        .user-message .bubble { background-color: #fff5f5; color: black; }
        .assistant-message .bubble { background-color: #ffc0cb; color: black; }
        .input-container { position: fixed; bottom: 0; left: 0; right: 0; padding: 10px 15px; display: flex; align-items: center; background-color: white; }
        .input-container input { flex: 1; padding: 10px; border-radius: 20px; border: 1px solid #ddd; }
        .input-container button { background-color: #ff8ba7; color: white; border: none; border-radius: 50%; width: 40px; height: 40px; display: flex; align-items: center; justify-content: center; cursor: pointer; }
    </style>
""", unsafe_allow_html=True)

# Title and description
st.markdown("<div class='title-container'>E-Ambulance 1122</div>", unsafe_allow_html=True)
st.markdown("<div class='description'>This chatbot is for your convenience. Feel free to ask anything about the E-Ambulance service.</div>", unsafe_allow_html=True)

# Varied greeting messages
greetings = [
    "Hi there! How can I assist you today? 😊",
    "Hello! I'm here to guide you. How can I help?",
    "Welcome! What can I do for you today?",
    "Hey! How's it going? Let me know how I can assist you. 😊"
]

# Handle user input
def handle_input():
    user_input = st.session_state.get("user_input", "").strip().lower()
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Handle greetings
        if user_input in ["hello", "hi", "hey"]:
            response = random.choice(greetings)

        # Handle "my name is" and remember user name
        elif "my name is" in user_input:
            user_name = user_input.split("my name is")[-1].strip().capitalize()
            st.session_state.user_name = user_name
            response = f"Hello {user_name}! How can I assist you today? 😊"

        # Handle "do you remember my name"
        elif "remember my name" in user_input:
            if st.session_state.user_name:
                response = f"Of course! Your name is {st.session_state.user_name}. I'm happy to assist you!"
            else:
                response = "I don't seem to remember your name. Can you tell me again?"

        # Handle "details about e-ambulance"
        elif "details" in user_input or "e-ambulance" in user_input or "what is e-ambulance" in user_input:
            response = "The E-Ambulance 1122 service provides emergency medical assistance 24/7, ensuring quick and efficient response during medical emergencies. It’s free and available to everyone in need."

        # Handle "is the service free"
        elif "free" in user_input:
            response = "Yes, the E-Ambulance service is free for emergencies. You can call 1122 any time for immediate help."

        # Handle emergency-related phrases
        elif "road accident" in user_input or "injured" in user_input:
            response = "I’m really sorry to hear that. Please stay calm. Our team is ready to assist you immediately. 🙏 Let me know if you need further information."

        # Check JSON-related queries
        elif any(user_input in str(value).lower() for value in personal_data.values()):
            for key, value in personal_data.items():
                if user_input in str(value).lower():
                    response = f"Here's the information you requested: {value}"
                    break

        # Default fallback
        else:
            response = "I didn't quite understand that. Could you please rephrase or ask something else?"

        # Add assistant response
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.session_state.user_input = ""

# Chat display
st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
for message in st.session_state.messages:
    role_class = "user-message" if message["role"] == "user" else "assistant-message"
    icon = "https://img.icons8.com/color/48/000000/ambulance.png" if message["role"] == "user" else "https://img.icons8.com/color/48/000000/robot.png"
    st.markdown(
        f"<div class='message {role_class}'><img src='{icon}' class='icon'><div class='bubble'>{message['content']}</div></div>",
        unsafe_allow_html=True,
    )
st.markdown("</div>", unsafe_allow_html=True)

# Voice-to-text
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

# Input box and buttons
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
