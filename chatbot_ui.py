import streamlit as st
import random
import speech_recognition as sr

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "👋 Hello! Welcome to the E-Ambulance 1122 service. How can I assist you today? 😊"}]
if "user_name" not in st.session_state:
    st.session_state.user_name = None

# Custom CSS for chat interface
st.markdown("""
    <style>
        .chat-container { max-width: 700px; margin: 0 auto; padding: 10px; }
        .message { margin: 10px 0; padding: 10px 15px; border-radius: 12px; max-width: 70%; }
        .user-message { background-color: #e0f7fa; text-align: right; }
        .assistant-message { background-color: #ffc0cb; }
        .input-container { display: flex; padding: 10px; }
        .menu-button { background-color: #007bff; border: none; color: white; padding: 8px 16px; margin: 5px; border-radius: 5px; cursor: pointer; }
    </style>
""", unsafe_allow_html=True)

# Function to handle user input
def handle_input():
    user_input = st.session_state.get("user_input", "").strip()
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        response = generate_response(user_input)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.session_state.user_input = ""  # Reset user input

# Function to generate chatbot responses
def generate_response(user_input):
    user_input = user_input.lower()
    
    # Greeting response
    if user_input in ["hello", "hi", "hey"]:
        return "Welcome back! How can I assist you further? 😊"
    
    # Remember user name
    elif "my name is" in user_input:
        st.session_state.user_name = user_input.split("my name is")[-1].strip().capitalize()
        return f"Pleasure to meet you, {st.session_state.user_name}! How can I assist you today? 😊"
    
    # Name recall
    elif "do you remember my name" in user_input:
        if st.session_state.user_name:
            return f"Of course! Your name is {st.session_state.user_name}. 😊"
        else:
            return "I don't seem to remember your name yet. Could you tell me your name?"
    
    # Emergency-related response
    elif "help" in user_input or "emergency" in user_input:
        return "Stay calm. Please call 1122 immediately if this is an emergency. Let me know how I can assist further. 🙏"
    
    # Information about the service
    elif "e-ambulance" in user_input or "details" in user_input:
        return "The E-Ambulance 1122 service provides 24/7 emergency assistance free of cost. We ensure fast response times for all medical emergencies."
    
    # Custom options (like the buttons you showed)
    elif "track order" in user_input:
        return "Unfortunately, I cannot track orders, but for more details, call 1122 or use the service app if available."
    
    # Fallback
    else:
        return "I'm here to help! Could you rephrase your question, or ask me about the E-Ambulance services? 😊"

# Display chat messages
st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
for message in st.session_state.messages:
    role_class = "user-message" if message["role"] == "user" else "assistant-message"
    st.markdown(f"<div class='message {role_class}'>{message['content']}</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# Input and menu buttons
st.markdown("<div class='input-container'>", unsafe_allow_html=True)
col1, col2, col3 = st.columns([6, 1, 1])

with col1:
    st.text_input("", placeholder="Type your message...", key="user_input", label_visibility="collapsed", on_change=handle_input)

# Pre-defined button options
st.markdown("<h4>Main Menu Options</h4>", unsafe_allow_html=True)
st.button("📦 Track Order", key="track_order", on_click=lambda: st.session_state.messages.append({"role": "user", "content": "track order"}))
st.button("🚑 Emergency Details", key="emergency_details", on_click=lambda: st.session_state.messages.append({"role": "user", "content": "details"}))
st.button("ℹ️ Service Info", key="service_info", on_click=lambda: st.session_state.messages.append({"role": "user", "content": "e-ambulance"}))

st.markdown("</div>", unsafe_allow_html=True)
