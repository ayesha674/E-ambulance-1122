import streamlit as st
import random
import speech_recognition as sr

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "🚑 Hello! Welcome to the E-Ambulance 1122 service. How can I assist you today? 😊"}]
if "user_name" not in st.session_state:
    st.session_state.user_name = None

# Custom CSS for your chatbot interface
st.markdown("""
    <style>
        .chat-container { max-width: 700px; margin: 0 auto; padding: 10px; border-radius: 15px; box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1); }
        .message { display: flex; align-items: center; margin-bottom: 10px; }
        .user-message { justify-content: flex-end; text-align: right; }
        .assistant-message { justify-content: flex-start; text-align: left; }
        .bubble { padding: 12px 15px; border-radius: 20px; font-size: 16px; max-width: 70%; box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.1); }
        .user-message .bubble { background-color: #fff5f5; color: black; }
        .assistant-message .bubble { background-color: #ffc0cb; color: black; }
        .input-container { padding: 10px; display: flex; justify-content: space-between; }
        .menu-button { background-color: #007bff; border: none; color: white; padding: 10px 15px; border-radius: 5px; cursor: pointer; margin-right: 10px; }
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

    # Greeting responses
    if user_input in ["hello", "hi", "hey"]:
        return "🚑 Welcome back! How can I assist you further? 😊"

    # Remembering user's name
    elif "my name is" in user_input:
        st.session_state.user_name = user_input.split("my name is")[-1].strip().capitalize()
        return f"Pleasure to meet you, {st.session_state.user_name}! 😊 How can I assist you today?"

    # Name recall
    elif "do you remember my name" in user_input:
        if st.session_state.user_name:
            return f"Yes, I remember your name! It's {st.session_state.user_name}. 😊"
        else:
            return "I don't seem to remember your name yet. Can you please tell me your name?"

    # Emergency response
    elif "help" in user_input or "emergency" in user_input:
        return "Stay calm! If you need immediate assistance, call 1122 now. Let me know if I can guide you further. 🙏"

    # Service information
    elif "details" in user_input or "e-ambulance" in user_input:
        return "The E-Ambulance 1122 service provides 24/7 free emergency medical assistance. You can call 1122 anytime, and help will arrive quickly."

    # For "Is the service free?"
    elif "free" in user_input:
        return "Yes, the E-Ambulance 1122 service is completely free for all emergencies."

    # Fallback for unrecognized input
    else:
        return "I'm here to help! Could you rephrase your question, or ask about the E-Ambulance services? 😊"

# Display chat messages
st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
for message in st.session_state.messages:
    role_class = "user-message" if message["role"] == "user" else "assistant-message"
    icon = "https://img.icons8.com/color/48/000000/ambulance.png" if message["role"] == "user" else "https://img.icons8.com/color/48/000000/robot.png"
    st.markdown(
        f"<div class='message {role_class}'><img src='{icon}' style='width: 24px; margin-right: 10px;'><div class='bubble'>{message['content']}</div></div>",
        unsafe_allow_html=True,
    )
st.markdown("</div>", unsafe_allow_html=True)

# Input container for user to type their message
st.markdown("<div class='input-container'>", unsafe_allow_html=True)
st.text_input("Your message", placeholder="Type your message here...", key="user_input", label_visibility="collapsed", on_change=handle_input)
st.markdown("</div>", unsafe_allow_html=True)

# Additional menu buttons for user convenience
st.markdown("<h4 style='text-align:center;'>Main Menu Options</h4>", unsafe_allow_html=True)
st.button("📢 Emergency Info", on_click=lambda: st.session_state.messages.append({"role": "user", "content": "details"}))
st.button("ℹ️ Service Information", on_click=lambda: st.session_state.messages.append({"role": "user", "content": "e-ambulance"}))
st.button("📞 Contact Emergency Line", on_click=lambda: st.session_state.messages.append({"role": "assistant", "content": "You can contact emergency services at 1122 directly. 🚑"}))

