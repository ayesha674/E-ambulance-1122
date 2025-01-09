# 🚑 **E-Ambulance-1122**

This project is an **AI-powered chatbot** designed to assist users with the **E-Ambulance system** by providing instant responses to their queries. The chatbot supports both **text-based** and **voice-based interactions** (when run locally) to enhance the user experience.

---

## 📝 **Project Information**
- **Project Title:** E-Ambulance-1122  
- **Course:** Final Year Semester Project  
- **Group Members:**  
  - 👩‍💻 **Ayesha Saleem** – Registration Number: **21PWBCS0844**  
  - 👩‍💻 **Palwasha** – Registration Number: **21PWBCS0840**

---

## 🌟 **Key Features**
1. **💬 Text-Based Interaction:** Type queries and receive instant chatbot responses related to the E-Ambulance system.  
2. **🎙️ Voice Input (Local Only):** Speak your queries using a microphone (works only when the app runs locally).  
3. **🖥️ User-Friendly Interface:** An intuitive and interactive design for smooth communication.  
4. **📝 Dummy Data:** The chatbot uses **dummy data** (`data.json`) to simulate real-world system information.  
5. **🌐 Cloud Deployment:** The app is deployed on **Streamlit Cloud** for easy online access.  

---

## ⚠️ **Important Notes**
- **Voice Input Limitation:** The voice input feature works only when the app runs **locally**. It does **not work** on **Streamlit Cloud** due to platform limitations (no audio input/output support).  
- **Dummy Data:** The `data.json` file contains sample data for demonstration purposes and can be replaced with real-time system data for production.

---

## 💻 **How to Run the Project Locally**

### **Step 1: Clone the Repository**
To download the project files, run the following commands:
```bash
git clone <repository-link>
cd e-ambulance-1122
---
### 🌐 **Step 2: Set Up a Virtual Environment**
Setting up a virtual environment ensures that all dependencies are installed in an isolated environment:

```bash
🐍 python -m venv env  # Create a virtual environment
💻 source env/bin/activate  # For Linux/macOS
🖥️ .\env\Scripts\activate  # For Windows
---
### 📦 **Step 3: Install Dependencies**
To install the required Python libraries for the project, run the following command:

```
📥 pip install -r requirements.txt
---
### 🔐 **Step 4: Create a `.env` File**
To securely store your **OpenAI API key**, create a `.env` file in the root directory and add your API key:

```
🔑 API_KEY=your-openai-api-key
---
### 🚀 **Step 5: Run the App**
To start the Streamlit application, run the following command:

```
▶️ streamlit run chatbot_ui.py
---
### 🌍 **Step 6: Access the App**
- **🌐 URL:** After running the app, Streamlit will provide a URL (usually `http://localhost:8501`).
- **🖥️ Open in Browser:** Copy the URL and open it in your browser.
- **🤖 Ready to Use:** You can now interact with the chatbot and test its features!
---
### ⚙️ **Step 7: Project Configuration**
---
#### **1. 🔐 Environment Variables**
Make sure your `.env` file contains the correct API key:

API_KEY=your-openai-api-key
---
## 📝 **Usage Instructions**
- **💬 Text Interaction:** Type your query in the input field and press **Enter** or click the **Send** button.
- **🎙️ Voice Input:** Click the **microphone icon** to speak your query (works only in local deployment).
- **🗑️ Clear Chat History:** Restart the app to clear the conversation history.

---

## 📁 **File Structure**
Here's an overview of the project's file structure:


📦 E-Ambulance-1122
├── 🤖 chatbot_ui.py      # Main application file
├── 📝 data.json          # JSON file containing system dummy data
├── 📦 requirements.txt   # Python dependencies
└── 📚 README.md          # Project documentation

## 🔨 **Dependencies**
The following libraries are required for the project:

- **🖥️ `streamlit`** – For creating the web-based user interface.
- **🎙️ `speechrecognition`** – For converting voice input to text.
- **🧠 `langchain`** – For OpenAI-powered chatbot responses.
- **🔐 `python-dotenv`** – For securely loading environment variables (API keys).

---

### 📦 **Install Dependencies**
To install all dependencies, run:

pip install -r requirements.txt


---
## 🌐 **Deployment Details**
- The project is deployed using **Streamlit Cloud** for online access.
- **🎙️ Voice Input Limitation:**  
  The voice input feature is unavailable on **Streamlit Cloud** due to platform limitations (no access to local audio hardware).  
  However, the text-based chat works seamlessly.
 --- 
### **Run Locally if Voice Input is Needed:**
To use the voice input feature, make sure to run the project locally as explained in the setup steps.

---

## 🎯 **Future Enhancements**
Here are some suggested improvements for future versions of the project:

- **🌐 Real-Time Data:** Replace dummy data with real-time system data for live responses.
- **🌍 Multilingual Support:** Add support for multiple languages to make the chatbot accessible to a wider audience.
- **🔊 Improved Voice Support:** Explore alternative deployment platforms that support voice input in cloud environments.
- **📱 Mobile-Friendly UI:** Optimize the user interface for mobile devices to provide a seamless experience.
- **💡 Additional Features:** Add interactive buttons for FAQs and emergency information to improve user engagement.

---
## 📧 **Contact Information**
For any questions, feedback, or suggestions, feel free to reach out to us:

- **👩‍💻 Ayesha Saleem** – ayeshasaleem2529@gmail.com
- **👩‍💻 Palwasha** – palwashajaved96@gmail.com.







