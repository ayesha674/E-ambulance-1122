import streamlit as st
import json
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
import speech_recognition as sr  # For voice-to-text

# Load environment variables
load_dotenv()

# Retrieve the API key from the .env file
api_key = os.getenv("API_KEY")

# Load personal data from a JSON file
with open("data.json") as f:
    personal_data = json.load(f)

# Initialize the OpenAI model
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, api_key=api_key)

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": (
                "You are an AI chatbot designed to assist users with the e-Ambulance system. "
                "You can answer questions based on the following JSON data: "
                f"{personal_data}. If a question is not related to the JSON data, respond with: "
                "'I am sorry, I can only answer questions related to the e-Ambulance system.'"
            ),
        },
        {
            "role": "assistant",
            "content": "Hello! How can I assist you today?"
        }
    ]

# Custom CSS for the UI
st.markdown("""
    <style>
        body {
            font-family: 'Arial', sans-serif;
        }
        .title-container {
            text-align: center;
            padding: 15px;
            border-radius: 10px;
            background-color: #ffc0cb;
            color: black;
            font-size: 22px;
            font-weight: bold;
            margin-bottom: 10px;
        }
        .description {
            text-align: center;
            font-size: 14px;
            margin-bottom: 10px;
            color: #333;
        }
        .chat-container {
            max-width: 700px;
            margin: 0 auto;
            border-radius: 15px;
            box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
            padding: 20px;
            background-color: white;
        }
        .message {
            display: flex;
            align-items: flex-start;
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
            border-radius: 15px;
            font-size: 14px;
            max-width: 60%;
            margin: 5px 0;
        }
        .user-message .bubble {
            background-color: #fff5f5;
            color: black;
            text-align: left;
        }
        .assistant-message .bubble {
            background-color: #ffc0cb;
            color: black;
            text-align: left;
        }
        .input-container {
            display: flex;
            gap: 10px;
            padding: 15px;
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            background-color: #fff5f5;
        }
        .input-container input {
            flex: 1;
            padding: 10px;
            border-radius: 20px;
            border: 1px solid #ddd;
        }
        .input-container button {
            border: none;
            background-color: #ff8ba7;
            color: white;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
        }
    </style>
""", unsafe_allow_html=True)

# Title and description
st.markdown("<div class='title-container'> E-Ambulance 1122 Chatbot</div>", unsafe_allow_html=True)
st.markdown("<div class='description'>This chatbot is designed to assist you. Feel free to ask anything!</div>", unsafe_allow_html=True)

# Chat Interface
st.markdown("<div class='chat-container'>", unsafe_allow_html=True)

# Display chat history
for message in st.session_state.messages[1:]:
    if message["role"] == "user":
        st.markdown(f"<div class='message user-message'><div class='bubble'>{message['content']}</div></div>", unsafe_allow_html=True)
    elif message["role"] == "assistant":
        st.markdown(f"<div class='message assistant-message'><div class='bubble'>{message['content']}</div></div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# Voice-to-text functionality
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
            st.toast("Timeout: No speech detected.")
            return None
        except sr.UnknownValueError:
            st.toast("Sorry, I could not understand the audio.")
            return None
        except sr.RequestError as e:
            st.toast(f"Error: {e}")
            return None

# Input handler for custom responses
def handle_input():
    user_input = st.session_state.get("user_input", "").strip().lower()
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Custom greeting response
        greetings = ["hello", "hi", "hey", "good morning", "good afternoon", "good evening"]
        if any(greet in user_input for greet in greetings):
            response = "Hello! How can I assist you today? 😊"

        # Name introduction handling
        elif "my name is" in user_input:
            name = user_input.split("my name is")[-1].strip().capitalize()
            response = f"Hello {name}! I’m here to guide you. How can I assist you? 😊"

        # General help request
        elif "help" in user_input or "i need your help" in user_input:
            response = "I’m here to help you! Please let me know how I can assist. 🚑"

        # JSON-based query handling
        elif any(user_input in str(value).lower() for value in personal_data.values()):
            response = llm.invoke(st.session_state.messages).content

        # Default response for unrecognized queries
        else:
            response = "I’m sorry, I can only answer questions related to the e-Ambulance system."

        # Add the response to the chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.session_state.user_input = ""  # Clear input field

# Input container
st.markdown("<div class='input-container'>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([10, 1, 1])

with col1:
    st.text_input(
        "",
        placeholder="Type your message here...",
        key="user_input",
        label_visibility="collapsed",
        on_change=handle_input,
    )

with col2:
    if st.button("🎙️"):
        user_input = voice_to_text()
        if user_input:
            st.session_state.messages.append({"role": "user", "content": user_input})
            handle_input()

with col3:
    if st.button("🩺"):
        handle_input()

st.markdown("</div>", unsafe_allow_html=True)


