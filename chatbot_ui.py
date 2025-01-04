import streamlit as st
import json
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
import re

# Load environment variables
load_dotenv()

# Retrieve the API key from the .env file
api_key = os.getenv("API_KEY")

# Load personal data from a JSON file
with open("data.json") as f:
    personal_data = json.load(f)

# Initialize the OpenAI model
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, api_key=api_key)

# Initialize chat history and user name in session state
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
            "content": "Hello! How can I assist you today? 😊"
        }
    ]
if "user_name" not in st.session_state:
    st.session_state.user_name = None

# Custom CSS for better styling
st.markdown("""
    <style>
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
            padding: 10px;
            background-color: #fffafc;
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
        }
        .user-message .bubble {
            background-color: #fff5f5;
            color: black;
        }
        .assistant-message .bubble {
            background-color: #ffc0cb;
            color: black;
        }
        .input-container {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            padding: 10px;
            display: flex;
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
        }
    </style>
""", unsafe_allow_html=True)

# Title and description
st.markdown("<div class='title-container'>E-Ambulance 1122</div>", unsafe_allow_html=True)
st.markdown("<div class='description'>This chatbot is for your convenience. Feel free to ask anything.</div>", unsafe_allow_html=True)

# Function to extract the user's name
def extract_name(user_input):
    name_match = re.search(r"\bmy name is (\w+)", user_input, re.IGNORECASE)
    if name_match:
        return name_match.group(1)
    return None

# Function to handle user input
def handle_input():
    user_input = st.session_state.get("user_input", "").strip()

    if user_input:
        # Add user input to session state
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Check if the user's input contains their name
        if not st.session_state.user_name:
            user_name = extract_name(user_input)
            if user_name:
                st.session_state.user_name = user_name.capitalize()
                response = f"Hello {st.session_state.user_name}, I'm here to guide you. How can I assist you? 😊"
        elif "remember" in user_input.lower() and "name" in user_input.lower():
            if st.session_state.user_name:
                response = f"Yes, your name is {st.session_state.user_name}! 😊"
            else:
                response = "I don't know your name yet. Can you please tell me your name?"
        elif "help" in user_input.lower():
            response = "I'm here to help! Please tell me more so I can assist you better. 😊"
        elif "hello" in user_input.lower():
            response = f"Hello {st.session_state.user_name or 'there'}! How can I assist you today? 😊"
        else:
            # Default handling by OpenAI API if input doesn't match predefined phrases
            if any(user_input.lower() in str(value).lower() for value in personal_data.values()):
                response = llm.invoke(st.session_state.messages).content
            else:
                response = "I am sorry, I can only answer questions related to the e-Ambulance system."

        # Add assistant's response to the chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.session_state.user_input = ""  # Clear the input field

# Input and button layout
col1, col2, col3 = st.columns([10, 1, 1])

with col1:
    st.text_input("", placeholder="Type your message here...", key="user_input", label_visibility="collapsed", on_change=handle_input)

with col2:
    if st.button("🎙️"):
        # Placeholder for voice input (You can implement speech-to-text logic)
        pass

with col3:
    if st.button("🩺"):
        handle_input()

# Display chat history
st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
for message in st.session_state.messages[1:]:  # Skip the system message
    if message["role"] == "user":
        st.markdown(f"<div class='message user-message'><div class='bubble'>{message['content']}</div></div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='message assistant-message'><div class='bubble'>{message['content']}</div></div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)




