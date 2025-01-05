import streamlit as st
import json
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
import speech_recognition as sr

# Load environment variables
load_dotenv()
api_key = os.getenv("API_KEY")

# Load JSON data
with open("data.json") as f:
    personal_data = json.load(f)

# Initialize OpenAI model
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, api_key=api_key)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = [
        
        {"role": "assistant", "content": "Hello! How can I assist you today? 😊"}
    ]
if "user_name" not in st.session_state:
    st.session_state.user_name = None

# Custom CSS for styling
st.markdown("""
    <style>
        .title-container {
            text-align: center;
            padding: 20px;
            background-color: #ffc0cb;
            color: black;
            font-size: 30px;
            font-weight: bold;
            border-radius: 10px;
        }
        .description {
            text-align: center;
            font-size: 16px;
            color: #333;
            margin-bottom: 10px;
        }
        .chat-container {
            max-width: 700px;
            margin: 0 auto;
            padding: 10px;
        }
        .message {
            display: flex;
            margin-bottom: 10px;
        }
        .user-message {
            justify-content: flex-end;
        }
        .assistant-message {
            justify-content: flex-start;
        }
        .bubble {
            padding: 12px 15px;
            border-radius: 20px;
            font-size: 14px;
            max-width: 70%;
            box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.1);
        }
        .user-message .bubble {
            background-color: #fff5f5;
            color: black;
        }
        .assistant-message .bubble {
            background-color: #ffc0cb;
            color: black;
        }
        .icon {
            width: 30px;
            height: 30px;
            margin: 5px;
        }
        .input-container {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            padding: 15px;
            background-color: #ffffff;
            display: flex;
            align-items: center;
            justify-content: space-between;
            box-shadow: 0px -2px 8px rgba(0, 0, 0, 0.1);
        }
        .input-container input {
            flex: 1;
            border: none;
            padding: 15px;
            border-radius: 30px;
            margin-right: 10px;
        }
        .input-container button {
            background-color: #ff8ba7;
            color: white;
            border: none;
            border-radius: 50%;
            width: 50px;
            height: 50px;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
        }
    </style>
""", unsafe_allow_html=True)

# Title and description
st.markdown("<div class='title-container'>E-Ambulance 1122</div>", unsafe_allow_html=True)
st.markdown("<div class='description'>This chatbot is for your convenience. Feel free to ask anything.</div>", unsafe_allow_html=True)

# Voice-to-text function
def voice_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.toast("Listening... Speak now!")
        try:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio)
            return text
        except sr.WaitTimeoutError:
            return "Sorry, I couldn't hear you. Please try again!"
        except sr.UnknownValueError:
            return "Sorry, I didn't understand that."
        except sr.RequestError:
            return "There was an issue with the service. Please try again later."

# Handle user input
def handle_input():
    user_input = st.session_state.get("user_input", "").strip()
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input.lower()})

        # Name recognition and intelligent response
        if "my name is" in user_input:
            user_name = user_input.split("my name is")[-1].strip().capitalize()
            st.session_state.user_name = user_name
            response = f"Hello {user_name}! How can I assist you today? 😊"

        elif "need your help" in user_input:
            if st.session_state.user_name:
                response = f"Hi {st.session_state.user_name}, I’m here to assist you! Please tell me more so I can guide you better. 😊"
            else:
                response = "I'm here to help! Can you please tell me your name so I can assist you better?"

        elif "remember my name" in user_input:
            if st.session_state.user_name:
                response = f"Of course! Your name is {st.session_state.user_name}. Let me know how I can help you further."
            else:
                response = "I’m sorry, I don’t seem to remember your name. Can you remind me?"

        # Emergency-related phrases
        elif "road accident" in user_input or "injured" in user_input:
            response = "I’m so sorry to hear that. Please stay calm. Our team is ready to assist you. 🙏"

        # Service-related questions
        elif "free" in user_input:
            response = "Yes, the e-Ambulance service is free for emergency cases."

        # JSON data check
        elif any(user_input in str(value).lower() for value in personal_data.values()):
            for key, value in personal_data.items():
                if user_input in str(value).lower():
                    response = f"Based on our records: {value}"
                    break

        # Default response
        else:
            response = "I'm sorry, I can only answer questions related to the e-Ambulance system."

        st.session_state.messages.append({"role": "assistant", "content": response})
        st.session_state.user_input = ""

# Display chat history
with st.sidebar:
    st.markdown("### Chat History")
    for i, message in enumerate(st.session_state.messages):
        if message["role"] == "user":
            st.button(message["content"][:20] + "...", key=f"history_{i}")

# Chat Interface
st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
for message in st.session_state.messages:
    role_class = "user-message" if message["role"] == "user" else "assistant-message"
    icon = "https://img.icons8.com/color/48/000000/ambulance.png" if message["role"] == "user" else "https://img.icons8.com/color/48/000000/robot.png"
    st.markdown(
        f"<div class='message {role_class}'><img src='{icon}' class='icon'><div class='bubble'>{message['content']}</div></div>",
        unsafe_allow_html=True,
    )
st.markdown("</div>", unsafe_allow_html=True)

# Input container
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
        voice_input = voice_to_text()
        if voice_input:
            st.session_state.messages.append({"role": "user", "content": voice_input})
            handle_input()

with col3:
    if st.button("➤"):
        handle_input()

st.markdown("</div>", unsafe_allow_html=True)
