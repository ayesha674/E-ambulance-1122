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

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful e-Ambulance chatbot."},
        {"role": "assistant", "content": "Hello! How can I assist you today? 😊"}
    ]

# Custom CSS for improved UI
st.markdown("""
    <style>
        body {
            font-family: 'Arial', sans-serif;
            background-color: #fef7f7;
        }
        .title-container {
            text-align: center;
            padding: 10px 0px;
            border-radius: 10px;
            background-color: #ffc0cb;
            color: black;
            font-size: 26px;
            font-weight: bold;
            margin-bottom: 10px;
        }
        .description {
            text-align: center;
            font-size: 14px;
            color: #333;
            margin: 0;
            padding: 5px 0;
        }
        .chat-container {
            max-width: 700px;
            margin: 0 auto;
            border-radius: 15px;
            box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
            height: calc(100vh - 200px);  /* Fill most of the height dynamically */
            overflow-y: auto;
            background-color: #fff;
            padding: 10px;
        }
        .message {
            display: flex;
            align-items: flex-start;
            margin-bottom: 10px;
        }
        .user-message {
            justify-content: flex-end;
            margin-left: auto;
        }
        .assistant-message {
            justify-content: flex-start;
            margin-right: auto;
        }
        .bubble {
            padding: 12px 15px;
            border-radius: 15px;
            font-size: 14px;
            max-width: 60%;
            box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.1);
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
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            padding: 10px 15px;
            background-color: white;
            display: flex;
            align-items: center;
            box-shadow: 0px -1px 5px rgba(0, 0, 0, 0.1);
        }
        .input-container input {
            flex: 1;
            border: none;
            padding: 12px;
            border-radius: 20px;
            margin-right: 10px;
            background-color: #fff5f5;
        }
        .input-container button {
            background-color: #ff8ba7;
            color: white;
            border: none;
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
st.markdown("<div class='title-container'>E-Ambulance 1122</div>", unsafe_allow_html=True)
st.markdown("<div class='description'>This chatbot is for your convenience. Feel free to ask anything.</div>", unsafe_allow_html=True)

# Sidebar for chat history
with st.sidebar:
    st.markdown("### Chat History")
    for i, message in enumerate(st.session_state.messages):
        if message["role"] == "user":
            if st.button(message["content"][:20] + "...", key=f"history_{i}"):
                st.session_state.selected_message = message["content"]

# Chat interface container
st.markdown("<div class='chat-container'>", unsafe_allow_html=True)

# Display chat messages
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(
            f"<div class='message user-message'><div class='bubble'>{message['content']}</div></div>",
            unsafe_allow_html=True,
        )
    elif message["role"] == "assistant":
        st.markdown(
            f"<div class='message assistant-message'><div class='bubble'>{message['content']}</div></div>",
            unsafe_allow_html=True,
        )

st.markdown("</div>", unsafe_allow_html=True)

# Function to convert voice to text
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
            st.toast("Sorry, I couldn't understand the audio.")
            return None
        except sr.RequestError as e:
            st.toast(f"Error: {e}")
            return None

# Handle text input
def handle_input():
    user_input = st.session_state.get("user_input", "").strip()
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Intelligent responses based on keywords
        if "name" in user_input.lower():
            response = f"Hello {user_input.split()[-1]}! How can I help you? 😊"
        elif "help" in user_input.lower():
            response = "I'm here to help! Please tell me more so I can assist you better. 😊"
        elif "hello" in user_input.lower():
            response = "Hi there! How can I assist you today? 😊"
        else:
            response = "I am sorry, I can only answer questions related to the e-Ambulance system."

        st.session_state.messages.append({"role": "assistant", "content": response})
        st.session_state.user_input = ""  # Clear the input field

# Input container at the bottom
st.markdown("<div class='input-container'>", unsafe_allow_html=True)
col1, col2, col3 = st.columns([8, 1, 1])

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


