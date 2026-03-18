import streamlit as st
from utils.pdf_utils import extract_text_from_pdf
from utils.ai_utils import analyze_resume

def render_analyzer():
    st.markdown("<h1 style='text-align:center;'>Analyze Your Resume</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#94a3b8;'>Upload your resume and paste a job description to get your ATS score instantly.</p>", unsafe_allow_html=True)

    from streamlit_extras.add_vertical_space import add_vertical_space as avs
    avs(2)

    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.markdown("""<div style='background:rgba(124,58,237,0.1); border:1px solid rgba(167,139,250,0.3); 
                        border-radius:16px; padding:1.5rem;'>
            <h3 style='color:#a78bfa !important; margin-top:0;'>📋 Job Description</h3>
        </div>""", unsafe_allow_html=True)
        default_jd = st.session_state.get("selected_jd", "")
        jd = st.text_area("Paste the job description here", value=default_jd, height=250, label_visibility="collapsed", placeholder="Paste the job description here...")

    with col2:
        st.markdown("""<div style='background:rgba(37,99,235,0.1); border:1px solid rgba(147,197,253,0.3); 
                        border-radius:16px; padding:1.5rem;'>
            <h3 style='color:#93c5fd !important; margin-top:0;'>📄 Your Resume</h3>
        </div>""", unsafe_allow_html=True)
        uploaded_file = st.file_uploader("Upload your resume (PDF)", type="pdf", help="Only PDF files are supported", label_visibility="collapsed")
        if uploaded_file:
            st.markdown(f"""<div style='background:rgba(16,185,129,0.1); border:1px solid rgba(110,231,183,0.3);
                            border-radius:10px; padding:0.8rem; margin-top:0.5rem;'>
                ✅ <span style='color:#6ee7b7;'>{uploaded_file.name}</span> uploaded successfully
            </div>""", unsafe_allow_html=True)

    avs(2)
    col_btn = st.columns([1, 2, 1])
    with col_btn[1]:
        submit = st.button("🚀 Analyze My Resume", use_container_width=True)

    if submit:
        if uploaded_file is None:
            st.error("⚠️ Please upload a PDF resume file.")
        elif jd.strip() == "":
            st.error("⚠️ Please provide a Job Description.")
        else:
            with st.spinner("🤖 AI is analyzing your resume..."):
                text = extract_text_from_pdf(uploaded_file)
                response = analyze_resume(text, jd)

            st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
            st.markdown("""<div style='background:linear-gradient(135deg,rgba(124,58,237,0.15),rgba(37,99,235,0.15));
                            border:1px solid rgba(167,139,250,0.3); border-radius:16px; padding:2rem; margin-top:1rem;'>
                <h2 style='color:#a78bfa !important; margin-top:0;'>📊 ATS Analysis Result</h2>
            </div>""", unsafe_allow_html=True)
            st.markdown(f"<div style='padding:1rem; color:#e2e8f0; line-height:1.8; white-space:pre-wrap;'>{response}</div>", unsafe_allow_html=True)
