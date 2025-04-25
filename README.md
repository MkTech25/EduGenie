📘 Askademy - AI-Powered Educational Assistant

Askademy is a user-friendly, AI-powered educational assistant built with Streamlit. It’s designed to help students simplify learning by providing instant academic support across multiple areas.
🔍 Features

    💬 Ask Questions
    Students can ask academic questions and receive instant, intelligent answers using LLM-based response generation.

    📘 Explain Concepts
    Get detailed explanations for tough concepts in an easy-to-understand manner.

    📄 Summarize Textbooks
    Upload textbook files (PDF or image format), and EduMentor will provide a concise and clear summary.

    📅 Personalized Study Plan
    Input your subjects and available daily study time, and generate a customized study schedule.

    🔊 Text-to-Speech Support
    All answers are also available in audio format using Google Text-to-Speech (gTTS).

    💾 Save Chat History
    Download your chat session as a PDF for offline review or sharing.

🛠 Requirements
Update  -  GOOGLE_API_KEY
To run the application, you need:

    Python 3.8+
    Streamlit
    PyPDF2
    gTTS
    FPDF

You can install dependencies using:

pip install -r requirements.txt

Example requirements.txt:
streamlit
PyPDF2
gTTS
fpdf

🚀 How to Run

streamlit run interface.py

Make sure llm.py is present and contains the Model class with a method get_response(prompt, file=None) that returns the model's answer.
👤 Developer

Built with ❤️ by Murali Kumar
