import streamlit as st
from dotenv import load_dotenv
import os
from google.generativeai import generativeai
from PyPDF2 import PdfReader
from PIL import Image

# Load environment variables
load_dotenv()
API_KEY = os.getenv('GOOGLE_API_KEY')

# Initialize the Gemini API
generativeai.initialize(api_key=API_KEY)

# Streamlit UI Setup
st.set_page_config(page_title="CareerCraft", layout="wide")
st.title("CareerCraft: ATS-Optimized Resume Analyzer")
st.image("images/career_icon.png", width=200)

# Function to get response from the Gemini model
def get_gemini_response(prompt):
    response = generativeai.generate_content(prompt)
    return response['text']

# Function to read and extract text from PDF
def input_pdf_text(uploaded_pdf):
    reader = PdfReader(uploaded_pdf)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# Input for Job Description and Resume Upload
st.header("Resume ATS Tracking Application")
job_description = st.text_area("Paste the Job Description Here:")
uploaded_resume = st.file_uploader("Upload Your Resume (PDF)", type=["pdf"])

# Processing Resume and Displaying Results
if st.button("Analyze Resume"):
    if job_description and uploaded_resume:
        resume_text = input_pdf_text(uploaded_resume)
        
        # Construct the prompt for the Gemini model
        prompt = f"""
        As an ATS system, analyze the following resume text against this job description. Provide a:
        1. Percentage match score,
        2. List of missing keywords, and
        3. Profile summary.
        
        Job Description: {job_description}
        Resume Text: {resume_text}
        """
        
        # Get response from Gemini Model
        analysis = get_gemini_response(prompt)
        
        # Display Results
        st.subheader("Analysis Result")
        st.write(analysis)
    else:
        st.warning("Please provide both a job description and a resume.")

# FAQ Section
with st.expander("FAQ"):
    st.write("""
    **1. How does CareerCraft work?**  
    CareerCraft uses the Gemini model to analyze your resume for ATS compatibility.

    **2. What is ATS?**  
    An ATS, or Applicant Tracking System, is software used by companies to screen resumes.
    """)

st.write("© 2024 CareerCraft")

