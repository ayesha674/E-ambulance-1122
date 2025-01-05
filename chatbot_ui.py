import streamlit as st
import json
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

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
       
        {"role": "assistant", "content": "Hello! How can I assist you today? 😊"}
    ]
if "user_name" not in st.session_state:
    st.session_state.user_name = None

# CSS styling
st.markdown("""
    <style>
        .title-container {
            text-align: center;
            padding: 10px;
            background-color: #ffc0cb;
            color: black;
            font-size: 24px;
            font-weight: bold;
        }
        .description {
            text-align: center;
            font-size: 14px;
            color: #333;
        }
        .chat-container {
            margin: 10px auto;
        }
        .message {
            margin-bottom: 10px;
            border-radius: 15px;
            padding: 10px 15px;
            font-size: 14px;
        }
        .user-message {
            background-color: #fff5f5;
            color: black;
            text-align: left;
        }
        .assistant-message {
            background-color: #ffc0cb;
            color: black;
            text-align: left;
        }
        .input-container {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            padding: 10px;
            background-color: white;
            display: flex;
        }
    </style>
""", unsafe_allow_html=True)

# Title and description
st.markdown("<div class='title-container'>E-Ambulance 1122</div>", unsafe_allow_html=True)
st.markdown("<div class='description'>This chatbot is for your convenience. Feel free to ask anything.</div>", unsafe_allow_html=True)

# Function to handle input
def handle_input():
    user_input = st.session_state.get("user_input", "").strip()
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input.lower()})

        # Handle name input
        if "my name is" in user_input:
            user_name = user_input.split("my name is")[-1].strip().capitalize()
            st.session_state.user_name = user_name
            response = f"Hello {user_name}! How can I assist you today? 😊"

        # Check for name recall
        elif "do you remember my name" in user_input or "what's my name" in user_input:
            if st.session_state.user_name:
                response = f"Of course! Your name is {st.session_state.user_name}. I'm here to assist you anytime!"
            else:
                response = "I’m sorry, I don’t seem to have your name. Can you tell me again?"

        # Handle greeting
        elif user_input in ["hi", "hello", "hey"]:
            if st.session_state.user_name:
                response = f"Hi {st.session_state.user_name}! How can I assist you today? 😊"
            else:
                response = "Hello! How can I assist you today? 😊"

        # Check for emergency-related phrases
        elif "road accident" in user_input or "injured" in user_input:
            response = "I’m so sorry to hear that. Please stay calm. Our team is ready to assist you. 🙏"

        # Service-related questions
        elif "free" in user_input:
            response = "Yes, the e-Ambulance service is free for emergency cases."

        # Check JSON data
        elif any(user_input in str(value).lower() for value in personal_data.values()):
            for key, value in personal_data.items():
                if user_input in str(value).lower():
                    response = f"Based on our records: {value}"
                    break

        # Default response
        else:
            response = "I'm sorry, I can only answer questions related to the e-Ambulance system."

        st.session_state.messages.append({"role": "assistant", "content": response})
        st.session_state.user_input = ""  # Clear the input field

# Display messages
for message in st.session_state.messages:
    role_class = "user-message" if message["role"] == "user" else "assistant-message"
    st.markdown(f"<div class='message {role_class}'>{message['content']}</div>", unsafe_allow_html=True)

# Input box for user
st.text_input(
    "",
    placeholder="Type your message here...",
    key="user_input",
    label_visibility="collapsed",
    on_change=handle_input,
)

