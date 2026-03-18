import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space as avs

def render_hero():
    col1, col2 = st.columns([3, 2])
    with col1:
        st.markdown("""
        <div style='padding: 2rem 0;'>
            <div style='display:inline-block; background:linear-gradient(90deg,#7c3aed,#2563eb); 
                        padding:0.3rem 1rem; border-radius:20px; font-size:0.85rem; 
                        font-weight:600; margin-bottom:1rem;'>
                ✨ AI-Powered Career Tool
            </div>
            <h1 style='font-size:3.5rem; font-weight:900; line-height:1.1; margin-bottom:1rem;'>
                CareerCraft
            </h1>
            <h2 style='font-size:1.5rem; font-weight:500; color:#c4b5fd !important; margin-bottom:1.5rem;'>
                Navigate the Job Market with Confidence
            </h2>
            <p style='font-size:1.05rem; line-height:1.8; color:#cbd5e1 !important; text-align:justify;'>
                CareerCraft is your ultimate ATS-Optimized Resume Analyzer. Leverage advanced AI to get 
                deep insights into your resume's compatibility with job descriptions, identify skill gaps, 
                and accelerate your career growth in today's competitive market.
            </p>
        </div>
        """, unsafe_allow_html=True)

        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.markdown("""<div class='card' style='text-align:center;'>
                <div style='font-size:2rem;'>🎯</div>
                <div style='font-weight:700; color:#a78bfa;'>ATS Score</div>
                <div style='font-size:0.85rem; color:#94a3b8;'>Instant match %</div>
            </div>""", unsafe_allow_html=True)
        with col_b:
            st.markdown("""<div class='card' style='text-align:center;'>
                <div style='font-size:2rem;'>🔍</div>
                <div style='font-weight:700; color:#a78bfa;'>Gap Analysis</div>
                <div style='font-size:0.85rem; color:#94a3b8;'>Missing keywords</div>
            </div>""", unsafe_allow_html=True)
        with col_c:
            st.markdown("""<div class='card' style='text-align:center;'>
                <div style='font-size:2rem;'>📈</div>
                <div style='font-weight:700; color:#a78bfa;'>Career Tips</div>
                <div style='font-size:0.85rem; color:#94a3b8;'>AI suggestions</div>
            </div>""", unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style='display:flex; align-items:center; justify-content:center; height:100%;'>
            <div style='background: linear-gradient(135deg, rgba(124,58,237,0.2), rgba(37,99,235,0.2));
                        border: 1px solid rgba(167,139,250,0.3);
                        border-radius: 24px; padding: 3rem; text-align:center;
                        backdrop-filter: blur(10px);'>
                <div style='font-size:8rem; line-height:1;'>📄</div>
                <div style='font-size:1.2rem; font-weight:700; color:#a78bfa; margin-top:1rem;'>
                    Resume Analyzer
                </div>
                <div style='color:#64748b; font-size:0.9rem; margin-top:0.5rem;'>
                    Upload · Analyze · Optimize
                </div>
                <div style='margin-top:1.5rem;'>
                    <span style='background:rgba(124,58,237,0.3); color:#c4b5fd; padding:0.3rem 0.8rem; 
                                 border-radius:20px; font-size:0.8rem; margin:0.2rem; display:inline-block;'>
                        ✅ ATS Friendly
                    </span>
                    <span style='background:rgba(37,99,235,0.3); color:#93c5fd; padding:0.3rem 0.8rem; 
                                 border-radius:20px; font-size:0.8rem; margin:0.2rem; display:inline-block;'>
                        🤖 AI Powered
                    </span>
                    <span style='background:rgba(16,185,129,0.3); color:#6ee7b7; padding:0.3rem 0.8rem; 
                                 border-radius:20px; font-size:0.8rem; margin:0.2rem; display:inline-block;'>
                        ⚡ Instant Results
                    </span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    avs(5)
    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)


def render_offerings():
    st.markdown("<h1 style='text-align:center;'>What We Offer</h1>", unsafe_allow_html=True)
    avs(2)

    offerings = [
        ("🎯", "ATS-Optimized Analysis", "Deep scan of your resume against job descriptions"),
        ("✍️", "Resume Optimization", "Actionable tips to improve your resume instantly"),
        ("🧠", "Skill Enhancement", "Identify and bridge your skill gaps"),
        ("🚀", "Career Progression", "Guidance tailored to your career goals"),
        ("📝", "Profile Summaries", "AI-crafted summaries that stand out"),
        ("⚡", "Streamlined Process", "Fast, simple, and effective workflow"),
        ("💡", "Smart Recommendations", "Personalized suggestions powered by AI"),
        ("🗺️", "Career Navigation", "Find the right path in a competitive market"),
    ]

    cols = st.columns(4)
    for i, (icon, title, desc) in enumerate(offerings):
        with cols[i % 4]:
            st.markdown(f"""
            <div class='card' style='text-align:center; min-height:140px;'>
                <div style='font-size:2.2rem;'>{icon}</div>
                <div style='font-weight:700; color:#a78bfa; margin:0.5rem 0; font-size:0.95rem;'>{title}</div>
                <div style='font-size:0.8rem; color:#94a3b8;'>{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    avs(5)
    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
