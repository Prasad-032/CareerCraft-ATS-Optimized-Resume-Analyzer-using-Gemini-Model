import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space as avs

def render_faq():
    st.markdown("<h1 style='text-align:center;'>Frequently Asked Questions</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#94a3b8;'>Everything you need to know about CareerCraft.</p>", unsafe_allow_html=True)
    avs(2)

    faq_data = [
        ("🤖", "How does CareerCraft analyze resumes?",
         "CareerCraft uses advanced AI algorithms to scan your resume and job description, identifying key keywords, skills, and compatibility scores to give you an accurate ATS match percentage."),
        ("✍️", "Can CareerCraft suggest improvements for my resume?",
         "Yes! CareerCraft provides personalized recommendations including missing keywords, skill gaps, and alignment tips tailored to the specific job you're applying for."),
        ("👥", "Is CareerCraft suitable for all experience levels?",
         "Absolutely. Whether you're a fresh graduate or a seasoned professional, CareerCraft adapts its insights to your career stage and helps you put your best foot forward."),
        ("🔒", "Is my resume data safe?",
         "Your data is processed in real-time and never stored. We take privacy seriously and ensure your personal information stays secure."),
        ("⚡", "How fast are the results?",
         "Results are generated within seconds using our AI engine, giving you instant feedback without any waiting time."),
    ]

    col1, col2 = st.columns(2)
    for i, (icon, question, answer) in enumerate(faq_data):
        with (col1 if i % 2 == 0 else col2):
            st.markdown(f"""
            <div class='card' style='margin-bottom:1rem;'>
                <div style='display:flex; align-items:flex-start; gap:1rem;'>
                    <div style='font-size:1.8rem; flex-shrink:0;'>{icon}</div>
                    <div>
                        <div style='font-weight:700; color:#a78bfa; margin-bottom:0.5rem; font-size:1rem;'>{question}</div>
                        <div style='color:#94a3b8; font-size:0.9rem; line-height:1.6;'>{answer}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
