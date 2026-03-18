from dotenv import load_dotenv
load_dotenv()

import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space as avs

from components.hero import render_hero, render_offerings
from components.job_search import render_job_search
from components.analyzer import render_analyzer
from components.faq import render_faq

st.set_page_config(page_title="CareerCraft | ATS Resume Analyzer", layout="wide", page_icon="🚀")

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
</style>
""", unsafe_allow_html=True)

avs(2)
render_hero()
render_offerings()
render_job_search()
render_analyzer()
avs(5)
render_faq()

st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#6b7280;'>© 2025 CareerCraft · Built to help you land your dream job 🚀</p>", unsafe_allow_html=True)
