# Importing libraries
from dotenv import load_dotenv
import streamlit as st
from streamlit_extras import add_vertical_space as avs
import google.generativeai as genai
import os
import PyPDF2
from PIL import Image

# Load environment variables
load_dotenv()

# Configure Google API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize Generative Model
model = genai.GenerativeModel('gemini-pro')

# Function to get Gemini response
def get_gemini_response(input):
    response = model.generate_content(input)
    return response.text

# Function to extract text from PDF
def input_pdf_text(uploaded_file):
    reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]
        text += str(page.extract_text())
    return text

# Input prompt for Gemini model
input_prompt = """
As an experienced ATS (Applicant Tracking System), proficient in the technical domain encompassing Software Engineering, Data Science, Data Analysis, Big Data Engineering, Web Developer, Mobile App Developer, DevOps Engineer, Machine Learning Engineer, Cybersecurity Analyst, Cloud Solutions Architect, Database Administrator, Network Engineer, AI Engineer, Systems Analyst, Full Stack Developer, UI/UX Designer, IT Project Manager, and additional specialized areas, your objective is to meticulously assess resumes against provided job descriptions. In a fiercely competitive job market, your expertise is crucial in offering top-notch guidance for resume enhancement. Assign precise matching percentages based on the JD (Job Description) and meticulously identify any missing keywords with utmost accuracy.
resume: {text}
description: {jd}
I want the response in the following structure:
The first line indicates the percentage match with the job description (JD).
The second line presents a list of missing keywords.
The third section provides a profile summary.
Mention the title for all the three sections.
While generating the response put some space to separate all the three sections.
"""

# Streamlit UI configuration
st.set_page_config(page_title="Resume ATS Tracker", layout="wide")
avs.add_vertical_space(4)

# UI components
col1, col2 = st.columns([3, 2])
with col1:
    st.title("CareerCraft")
    st.header("Navigate the Job Market with Confidence!")
    st.markdown("""<p style='text-align: justify;'> Introducing CareerCraft, an ATS-Optimized Resume Analyzer your ultimate solution for optimizing job applications and accelerating career growth. Our innovative platform leverages advanced ATS technology to provide job seekers with valuable insights into their resumes' compatibility with job descriptions. From resume optimization and skill enhancement to career progression guidance, CareerCraft empowers users to stand out in today's competitive job market. Streamline your job application process, enhance your skills, and navigate your career path with confidence. Join CareerCraft today and unlock new opportunities for professional success! </p>""", unsafe_allow_html=True)

with col2:
    try:
        st.image("images/hero_image.png", use_column_width=True)
    except FileNotFoundError:
        st.warning("Hero image not found.")
avs.add_vertical_space(10)

# Additional UI components
col1, col2 = st.columns([3, 2])
with col2:
    st.header("Wide Range of Offerings")
    offerings = [
        'ATS-Optimized Resume Analysis', 'Resume Optimization', 'Skill Enhancement',
        'Career Progression Guidance', 'Tailored Profile Summaries', 'Streamlined Application Process',
        'Personalized Recommendations', 'Efficient Career Navigation'
    ]
    for offering in offerings:
        st.write(offering)

with col1:
    try:
        img1 = Image.open("images/icon1.png")
        st.image(img1, use_column_width=True)
    except FileNotFoundError:
        st.warning("Icon image icon1.png not found.")
avs.add_vertical_space(10)

# Input fields and submission button
col1, col2 = st.columns([3, 2])
with col1:
    st.markdown("<h1 style='text-align: center;'>Embark on Your Career Adventure</h1>", unsafe_allow_html=True)
    jd = st.text_area("Paste the Job Description")
    uploaded_file = st.file_uploader("Upload Your Resume", type="pdf", help="Please upload the pdf")
    submit = st.button("Submit")

# Processing submission with error handling
if submit:
    if uploaded_file is None:
        st.error("Please upload a PDF resume file.")
    elif jd.strip() == "":
        st.error("Please provide a Job Description.")
    else:
        with col2:
            # Extract text from the uploaded resume PDF
            text = input_pdf_text(uploaded_file)
            # Format the prompt for Gemini model
            formatted_prompt = input_prompt.format(text=text, jd=jd)
            response = get_gemini_response(formatted_prompt)
            st.subheader("ATS Analysis Result")
            st.write(response)  # Display the model's response
            # Placeholder image or icon display
            try:
                img2 = Image.open("images/icon2.png")
                st.image(img2, use_column_width=True)
            except FileNotFoundError:
                st.warning("Image icon2.png not found.")
avs.add_vertical_space(10)

# FAQ section
col1, col2 = st.columns([2, 3])
with col2:
    st.markdown("<h1 style='text-align: center;'>Frequently Asked Questions</h1>", unsafe_allow_html=True)
    faq_data = [
        ("How does CareerCraft analyze resumes and job descriptions?",
         "CareerCraft uses advanced algorithms to analyze resumes and job descriptions, identifying key keywords and assessing compatibility between the two."),
        ("Can CareerCraft suggest improvements for my resume?",
         "Yes, CareerCraft provides personalized recommendations to optimize your resume for specific job openings, including suggestions for missing keywords and alignment with desired job roles."),
        ("Is CareerCraft suitable for both entry-level and experienced professionals?",
         "Absolutely! CareerCraft caters to job seekers at all career stages, offering tailored insights and guidance to enhance their resumes and advance their careers.")
    ]
    for question, answer in faq_data:
        st.write(f"**Question:** {question}")
        st.write(f"**Answer:** {answer}")
        avs.add_vertical_space(3)

with col1:
    try:
        img3 = Image.open("images/icon3.png")
        st.image(img3, use_column_width=True)
    except FileNotFoundError:
        st.warning("Image icon3.png not found.")
