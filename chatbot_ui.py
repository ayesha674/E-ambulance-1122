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
                "You can only answer questions based on the following JSON data: "
                f"{personal_data}. If a question is not related to the JSON data, respond with: "
                "'I am sorry, I can only answer questions related to the e-Ambulance system.'"
            ),
        },
        {
            "role": "assistant",
            "content": "Hello! How can I assist you?"
        }
    ]


# Custom CSS for the UI
st.markdown("""
    <style>
        body {
            font-family: 'Arial', sans-serif;
            background-color: #fef7f7;
            margin: 0;
            padding: 0;
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
            height: auto;
            padding: 0;
            background: none;
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
            padding: 10px 15px;
            display: flex;
            align-items: center;
        }
        .input-container input {
            flex: 1;
            border: none;
            padding: 10px;
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
st.markdown("<div class='title-container'> E-Ambulance 1122</div>", unsafe_allow_html=True)
st.markdown("<div class='description'>This chatbot is for your convenience. Feel free to ask anything.</div>", unsafe_allow_html=True)

# Sidebar for chat history
with st.sidebar:
    st.markdown("### Chat History")
    for i, message in enumerate(st.session_state.messages):
        if message["role"] == "user":
            if st.button(message["content"][:20] + "...", key=f"history_{i}"):
                st.session_state.selected_message = message["content"]

# Chat Interface
st.markdown("<div class='chat-container'>", unsafe_allow_html=True)

# Display messages
for message in st.session_state.messages[1:]:  # Skip system message
    if message["role"] == "user":
        st.markdown(
            f"<div class='message user-message'><div class='bubble'>{message['content']}</div><img src='https://img.icons8.com/color/48/000000/ambulance.png' class='icon'></div>",
            unsafe_allow_html=True,
        )
    elif message["role"] == "assistant":
        st.markdown(
            f"<div class='message assistant-message'><img src='https://img.icons8.com/color/48/000000/robot.png' class='icon'><div class='bubble'>{message['content']}</div></div>",
            unsafe_allow_html=True,
        )

st.markdown("</div>", unsafe_allow_html=True)

# Voice-to-text functionality
def voice_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.toast("Listening... Speak now!")
        try:
            recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
            audio = recognizer.listen(source, timeout=5)  # Wait for up to 5 seconds
            text = recognizer.recognize_google(audio)
            return text
        except sr.WaitTimeoutError:
            st.toast("Timeout: No speech detected.")
            return None
        except sr.UnknownValueError:
            st.toast("Sorry, I could not understand the audio.")
            return None
        except sr.RequestError as e:
            st.toast(f"Error with the speech recognition service: {e}")
            return None

# Input handler for restricting responses to JSON-related questions
def handle_input():
    user_input = st.session_state.get("user_input", "").strip()
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Check if the user's query matches any part of the JSON data
        if any(user_input.lower() in str(value).lower() for value in personal_data.values()):
            # If the query matches the JSON data, invoke the AI to generate a response
            response = llm.invoke(st.session_state.messages).content
        else:
            # Otherwise, return a predefined response
            response = "I am sorry, I can only answer questions related to the e-Ambulance system."

        # Add the response to the chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.session_state.user_input = ""  # Clear the input field

# Input container
st.markdown("<div class='input-container'>", unsafe_allow_html=True)

def handle_input():
    user_input = st.session_state.get("user_input", "")
    if user_input.strip():  # Check if input is not empty
        st.session_state.messages.append({"role": "user", "content": user_input})
        response = llm.invoke(st.session_state.messages).content
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.session_state.user_input = ""  # Clear the input field

col1, col2, col3 = st.columns([8, 1, 1])

with col1:
    st.text_input(
        "",
        placeholder="Type your message here...",
        key="user_input",
        label_visibility="collapsed",
        on_change=handle_input,  # Trigger input handling when Enter is pressed
    )

with col2:
    if st.button("🎙️"):
        user_input = voice_to_text()
        if user_input:
            st.session_state.messages.append({"role": "user", "content": user_input})
            response = llm.invoke(st.session_state.messages).content
            st.session_state.messages.append({"role": "assistant", "content": response})

with col3:
    if st.button("🩺"):  # Replace the arrow icon with an ambulance-themed icon
        handle_input()

st.markdown("</div>", unsafe_allow_html=True)
