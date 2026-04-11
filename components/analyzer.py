import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space as avs
from utils.pdf_utils import extract_text_from_pdf
from utils.ai_utils import analyze_resume

def render_analyzer():
    st.markdown("<h1 style='text-align:center;'>Analyze Your Resume</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#94a3b8;'>Upload your resume and paste a job description to get your ATS score instantly.</p>", unsafe_allow_html=True)
    avs(2)

    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.markdown("""<div style='background:rgba(124,58,237,0.1); border:1px solid rgba(167,139,250,0.3); 
                        border-radius:16px; padding:1.5rem; margin-bottom:0.5rem;'>
            <h3 style='color:#a78bfa !important; margin-top:0;'>📋 Job Description</h3>
            <p style='color:#94a3b8; font-size:0.85rem; margin:0;'>Paste a JD or use the Job Search above to auto-fill.</p>
        </div>""", unsafe_allow_html=True)

        # Show banner if JD was auto-filled from job search
        if st.session_state.get("jd_loaded"):
            st.markdown("""<div style='background:rgba(16,185,129,0.1); border:1px solid rgba(110,231,183,0.3);
                            border-radius:10px; padding:0.6rem 1rem; margin-bottom:0.5rem; font-size:0.85rem;'>
                ✅ <span style='color:#6ee7b7;'>Job description auto-filled from search.</span>
            </div>""", unsafe_allow_html=True)
            st.session_state["jd_loaded"] = False

        default_jd = st.session_state.get("selected_jd", "")
        jd = st.text_area(
            "Paste the job description here",
            value=default_jd,
            height=280,
            label_visibility="collapsed",
            placeholder="Paste the job description here, or use Job Search above to auto-fill..."
        )

    with col2:
        st.markdown("""<div style='background:rgba(37,99,235,0.1); border:1px solid rgba(147,197,253,0.3); 
                        border-radius:16px; padding:1.5rem; margin-bottom:0.5rem;'>
            <h3 style='color:#93c5fd !important; margin-top:0;'>📄 Your Resume</h3>
            <p style='color:#94a3b8; font-size:0.85rem; margin:0;'>Supported formats: PDF, DOCX</p>
        </div>""", unsafe_allow_html=True)

        uploaded_file = st.file_uploader(
            "Upload your resume",
            type=["pdf", "docx"],
            help="Supported formats: PDF and DOCX",
            label_visibility="collapsed"
        )

        if uploaded_file:
            # Show file info
            file_size_kb = round(uploaded_file.size / 1024, 1)
            file_ext = uploaded_file.name.split(".")[-1].upper()
            st.markdown(f"""<div style='background:rgba(16,185,129,0.1); border:1px solid rgba(110,231,183,0.3);
                            border-radius:10px; padding:0.8rem; margin-top:0.5rem;'>
                ✅ <span style='color:#6ee7b7; font-weight:600;'>{uploaded_file.name}</span><br>
                <span style='color:#94a3b8; font-size:0.8rem;'>{file_ext} · {file_size_kb} KB</span>
            </div>""", unsafe_allow_html=True)

    avs(2)
    col_btn = st.columns([1, 2, 1])
    with col_btn[1]:
        submit = st.button("🚀 Analyze My Resume", use_container_width=True)

    if submit:
        if uploaded_file is None:
            st.error("⚠️ Please upload your resume (PDF or DOCX).")
        elif jd.strip() == "":
            st.error("⚠️ Please provide a Job Description — paste one or use Job Search above.")
        else:
            with st.spinner("🤖 AI is analyzing your resume..."):
                text = extract_text_from_pdf(uploaded_file)
                if not text.strip():
                    st.error("⚠️ Could not extract text from your resume. Make sure it's not a scanned image PDF.")
                    return
                response = analyze_resume(text, jd)

            st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
            st.markdown("<h2 style='text-align:center; color:#a78bfa !important;'>📊 ATS Analysis Result</h2>", unsafe_allow_html=True)
            avs(1)

            # Parse and display result in structured sections
            _render_result(response)

def _render_result(response: str):
    """Split AI response into visual sections for score, keywords, and summary."""
    lines = response.strip().split("\n")
    sections = {"score": [], "keywords": [], "summary": []}
    current = None

    for line in lines:
        lower = line.lower()
        if any(k in lower for k in ["match", "percentage", "ats score", "% match"]):
            current = "score"
        elif any(k in lower for k in ["missing keyword", "keyword"]):
            current = "keywords"
        elif any(k in lower for k in ["profile summary", "summary", "profile"]):
            current = "summary"
        if current:
            sections[current].append(line)

    # Fallback: if parsing fails, just show raw
    if not any(sections.values()):
        st.markdown(f"<div style='padding:1rem; color:#e2e8f0; line-height:1.8; white-space:pre-wrap;'>{response}</div>", unsafe_allow_html=True)
        return

    if sections["score"]:
        st.markdown(f"""<div class='result-score'>
            <div style='font-size:1.1rem; font-weight:700; color:#a78bfa; margin-bottom:0.5rem;'>🎯 ATS Match Score</div>
            <div style='color:#e2e8f0; line-height:1.8; white-space:pre-wrap;'>{"".join(sections["score"])}</div>
        </div>""", unsafe_allow_html=True)

    if sections["keywords"]:
        st.markdown(f"""<div class='result-keywords'>
            <div style='font-size:1.1rem; font-weight:700; color:#f87171; margin-bottom:0.5rem;'>🔍 Missing Keywords</div>
            <div style='color:#e2e8f0; line-height:1.8; white-space:pre-wrap;'>{chr(10).join(sections["keywords"])}</div>
        </div>""", unsafe_allow_html=True)

    if sections["summary"]:
        st.markdown(f"""<div class='result-summary'>
            <div style='font-size:1.1rem; font-weight:700; color:#6ee7b7; margin-bottom:0.5rem;'>📝 Profile Summary</div>
            <div style='color:#e2e8f0; line-height:1.8; white-space:pre-wrap;'>{chr(10).join(sections["summary"])}</div>
        </div>""", unsafe_allow_html=True)
