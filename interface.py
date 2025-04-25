import streamlit as st
from llm import Model
from gtts import gTTS
import base64
import tempfile
import time
import json
from PyPDF2 import PdfReader
from fpdf import FPDF

# Initialize model
model = Model()

# Page Config
st.set_page_config(page_title="Askademy - AI Assistant", page_icon="📖", layout="centered")

# Style
st.markdown("""
    <style>
    .justified-text { text-align: justify; }
    .block-container { padding-top: 2rem; padding-bottom: 2rem; }
    .stButton > button { border-radius: 8px; padding: 0.5em 2em; font-size: 1rem; }
    </style>
    """, unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title("🧠 About Askademy")
    st.caption("""
        <div class="justified-text">
           Askademy is an AI-powered educational assistant designed to help students by:
           <ul>
               <li><strong>Answering Questions:</strong> Get quick and accurate answers to your academic queries.</li>
               <li><strong>Explaining Concepts:</strong> Receive detailed explanations of complex subjects.</li>
               <li><strong>Summarizing Textbook Content:</strong> Upload and summarize textbooks, whether in PDF or image format.</li>
               <li><strong>Generating Personalized Study Plans:</strong> Create custom study schedules based on your subjects and available time.</li>
           </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Menu options
    menu = ["❓ Ask a Question", "📘 Explain a Concept", "📷 Summarize Textbook", "📅 Personalized Study Plan"]
    choice = st.selectbox("Choose an Option", menu)

    st.markdown("---")
    st.subheader("👤 Developer")
    st.markdown("Murali Kumar")
    st.markdown("📧 [Email](mailto:muralikumar.n@yahoo.com)")
    st.markdown("---")

# TTS
def play_audio(text):
    tts = gTTS(text)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        tts.save(fp.name)
        audio_path = fp.name
    with open(audio_path, "rb") as audio_file:
        b64 = base64.b64encode(audio_file.read()).decode()
    st.markdown(f"""<audio autoplay><source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>""", unsafe_allow_html=True)

# PDF Extraction
def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# Chat Mode
if choice == "❓ Ask a Question":
    st.subheader("💬 Chat with Askademy")
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    question = st.text_input("Type your question:")

    if st.button("Send") and question:
        st.session_state.chat_history.append(("user", question))
        prompt = f"You are a helpful educational assistant. Question: {question}"
        with st.spinner("🤔 Thinking..."):
            response = model.get_response(prompt)
            st.session_state.chat_history.append(("bot", response))
            play_audio(response)

    for role, msg in st.session_state.chat_history:
        icon = "🧑" if role == "user" else "🤖"
        st.markdown(f"{icon} **{role.capitalize()}:** {msg}")
        time.sleep(0.2)

    if st.session_state.chat_history:
        if st.button("💾 Download Chat History as PDF"):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.set_font("Arial", size=12)

            pdf.set_title("Askademy Chat History")
            pdf.cell(200, 10, txt="Askademy Chat History", ln=True, align="C")
            pdf.ln(10)

            for role, msg in st.session_state.chat_history:
                role_label = "You" if role == "user" else "Askademy"
                pdf.multi_cell(0, 10, f"{role_label}: {msg}", align='L')
                pdf.ln(1)

            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                pdf.output(tmp_file.name)
                with open(tmp_file.name, "rb") as file:
                    st.download_button(
                        label="📥 Download PDF",
                        data=file,
                        file_name="Askademy_chat_history.pdf",
                        mime="application/pdf"
                    )

# Concept Explanation
elif choice == "📘 Explain a Concept":
    st.subheader("📘 Explain a Concept")
    concept = st.text_input("Enter a concept:")
    if st.button("Explain"):
        prompt = f"Explain the following concept in detail: {concept}"
        with st.spinner("📖 Generating explanation..."):
            response = model.get_response(prompt)
        st.success("Explanation:")
        st.write(response)

# Summarize Image or PDF
elif choice == "📷 Summarize Textbook":
    st.subheader("📷📄 Summarize Textbook (Image or PDF)")
    file = st.file_uploader("Upload a textbook image or PDF", type=["jpg", "jpeg", "png", "pdf"])
    if file:
        if file.type == "application/pdf":
            with st.spinner("📄 Reading PDF..."):
                text = extract_text_from_pdf(file)
                prompt = f"Summarize this textbook content:\n{text[:2000]}"
                response = model.get_response(prompt)
                st.success("Summary:")
                st.write(response)
        else:
            st.image(file, caption="Uploaded Image", use_column_width=True)
            if st.button("Summarize"):
                prompt = "Summarize this textbook content"
                with st.spinner("📝 Summarizing image content..."):
                    response = model.get_response(prompt, file)
                st.success("Summary:")
                st.write(response)

# Study Plan
elif choice == "📅 Personalized Study Plan":
    st.subheader("📅 Create Personalized Study Plan")
    subjects = st.text_input("Subjects (comma-separated):")
    study_time = st.slider("Study hours/day:", 1, 8, 2)
    if st.button("Generate Plan"):
        prompt = f"Create a study plan for: {subjects}. Available time: {study_time} hours/day."
        with st.spinner("🧠 Generating study plan..."):
            response = model.get_response(prompt)
        st.success("Study Plan:")
        st.write(response)
