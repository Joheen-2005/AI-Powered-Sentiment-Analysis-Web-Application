import streamlit as st
from textblob import TextBlob
import fitz  # PyMuPDF
import docx
import os

def analyze_sentiment(text):
    analysis = TextBlob(text)
    return analysis.sentiment.polarity

def extract_text_from_pdf(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def extract_text_from_docx(file):
    doc = docx.Document(file)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text

st.markdown(
    """
    <style>
    .stButton>button {
        background-color: #4CAF50;
        color: white;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title('Sentiment Analysis App')

input_method = st.radio("Choose input method:", ("Type text", "Upload a file"))

input_text = ""

if input_method == "Upload a file":
    uploaded_file = st.file_uploader("Upload a file for analysis:", type=None)
    if uploaded_file is not None:
        file_name = uploaded_file.name.lower()
        try:
            if file_name.endswith(".pdf"):
                input_text = extract_text_from_pdf(uploaded_file)
            elif file_name.endswith(".docx"):
                input_text = extract_text_from_docx(uploaded_file)
            else:
                input_text = uploaded_file.read().decode("utf-8")
        except Exception as e:
            st.error(f"Error reading the file: {e}")
else:
    input_text = st.text_area("Enter text for analysis:")

if st.button("Analyze"):
    if input_text:
        sentiment_score = analyze_sentiment(input_text)
        if sentiment_score > 0:
            sentiment = "Positive sentiment detected! 😊"
            score_message = f"Score: {sentiment_score:.2f}"
            st.success(f"{sentiment} {score_message}")
        elif sentiment_score < 0:
            sentiment = "Negative sentiment detected! 😞"
            score_message = f"Score: {sentiment_score:.2f}"
            st.error(f"{sentiment} {score_message}")
        else:
            sentiment = "Neutral sentiment detected! 😐"
            score_message = "Score: 0.00"
            st.warning(f"{sentiment} {score_message}")
    else:
        st.warning("Please enter some text for analysis or upload a file.")
