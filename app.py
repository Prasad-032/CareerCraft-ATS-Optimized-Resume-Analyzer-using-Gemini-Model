from dotenv import load_dotenv
load_dotenv()

import os
import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space as avs

from components.hero import render_hero, render_offerings
from components.job_search import render_job_search
from components.analyzer import render_analyzer
from components.faq import render_faq

st.set_page_config(page_title="CareerCraft | ATS Resume Analyzer", layout="wide", page_icon="🚀")

# API key check
if not os.getenv("NVIDIA_API_KEY"):
    st.error("⚠️ NVIDIA_API_KEY is not set. Please add it to your .env file to use the AI analysis feature.")

st.markdown("""
<style>
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        color: #ffffff;
    }
    [data-testid="stHeader"] { background: transparent; }
    [data-testid="stSidebar"] { background: #1a1a2e; }
    h1 { 
        font-size: 3rem !important; 
        background: linear-gradient(90deg, #a78bfa, #60a5fa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800 !important;
    }
    h2, h3 { color: #c4b5fd !important; }
    p, li, label { color: #e2e8f0 !important; }
    .stButton > button {
        background: linear-gradient(90deg, #7c3aed, #2563eb);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.6rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(124, 58, 237, 0.4);
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(124, 58, 237, 0.6);
    }
    .stTextArea textarea, .stTextInput input {
        background: rgba(255,255,255,0.05) !important;
        border: 1px solid rgba(167, 139, 250, 0.3) !important;
        border-radius: 12px !important;
        color: #ffffff !important;
    }
    [data-testid="stFileUploader"] {
        background: rgba(255,255,255,0.03);
        border: 2px dashed rgba(167, 139, 250, 0.4);
        border-radius: 12px;
        padding: 1rem;
    }
    .streamlit-expanderHeader {
        background: rgba(255,255,255,0.05) !important;
        border-radius: 10px !important;
        color: #c4b5fd !important;
    }
    .card {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(167,139,250,0.2);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 0.5rem 0;
        backdrop-filter: blur(10px);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 30px rgba(124,58,237,0.3);
    }
    .section-divider {
        height: 2px;
        background: linear-gradient(90deg, transparent, #7c3aed, #2563eb, transparent);
        margin: 2rem 0;
        border: none;
    }
    .stSpinner > div { border-top-color: #7c3aed !important; }
    /* Sticky nav */
    .sticky-nav {
        position: sticky;
        top: 0;
        z-index: 999;
        background: rgba(15,12,41,0.92);
        backdrop-filter: blur(12px);
        border-bottom: 1px solid rgba(167,139,250,0.2);
        padding: 0.6rem 2rem;
        display: flex;
        gap: 2rem;
        align-items: center;
    }
    .sticky-nav a {
        color: #c4b5fd !important;
        text-decoration: none;
        font-size: 0.9rem;
        font-weight: 500;
        transition: color 0.2s;
    }
    .sticky-nav a:hover { color: #a78bfa !important; }
    /* Step guide */
    .step-guide {
        display: flex;
        justify-content: center;
        gap: 1rem;
        margin: 1.5rem 0;
        flex-wrap: wrap;
    }
    .step-item {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(167,139,250,0.2);
        border-radius: 30px;
        padding: 0.4rem 1rem;
        font-size: 0.85rem;
        color: #c4b5fd;
    }
    .step-arrow { color: #6b7280; font-size: 1.2rem; }
    /* Result sections */
    .result-score {
        background: linear-gradient(135deg, rgba(124,58,237,0.2), rgba(37,99,235,0.2));
        border: 1px solid rgba(167,139,250,0.4);
        border-radius: 16px;
        padding: 1.5rem 2rem;
        margin-bottom: 1rem;
    }
    .result-keywords {
        background: rgba(239,68,68,0.1);
        border: 1px solid rgba(239,68,68,0.3);
        border-radius: 16px;
        padding: 1.5rem 2rem;
        margin-bottom: 1rem;
    }
    .result-summary {
        background: rgba(16,185,129,0.1);
        border: 1px solid rgba(16,185,129,0.3);
        border-radius: 16px;
        padding: 1.5rem 2rem;
        margin-bottom: 1rem;
    }
    /* Mobile responsive */
    @media (max-width: 768px) {
        h1 { font-size: 2rem !important; }
        .step-guide { flex-direction: column; align-items: center; }
    }
</style>
""", unsafe_allow_html=True)

# Sticky navigation
st.markdown("""
<div class='sticky-nav'>
    <span style='font-weight:700; color:#a78bfa; font-size:1rem;'>🚀 CareerCraft</span>
    <a href='#home'>Home</a>
    <a href='#job-search'>Job Search</a>
    <a href='#analyzer'>Analyzer</a>
    <a href='#faq'>FAQ</a>
</div>
""", unsafe_allow_html=True)

# Step guide
st.markdown("""
<div class='step-guide'>
    <div class='step-item'>① Search a Job</div>
    <span class='step-arrow'>→</span>
    <div class='step-item'>② Select Job Description</div>
    <span class='step-arrow'>→</span>
    <div class='step-item'>③ Upload Your Resume</div>
    <span class='step-arrow'>→</span>
    <div class='step-item'>④ Get ATS Score</div>
</div>
""", unsafe_allow_html=True)

avs(1)
st.markdown("<div id='home'></div>", unsafe_allow_html=True)
render_hero()
render_offerings()
st.markdown("<div id='job-search'></div>", unsafe_allow_html=True)
render_job_search()
st.markdown("<div id='analyzer'></div>", unsafe_allow_html=True)
render_analyzer()
avs(3)
st.markdown("<div id='faq'></div>", unsafe_allow_html=True)
render_faq()

st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#6b7280;'>© 2025 CareerCraft · Built to help you land your dream job 🚀</p>", unsafe_allow_html=True)
