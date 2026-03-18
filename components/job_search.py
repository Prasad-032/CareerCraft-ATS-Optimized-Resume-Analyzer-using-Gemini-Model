import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space as avs
from utils.job_utils import fetch_jobs

def render_job_search():
    st.markdown("<h1 style='text-align:center;'>Search Real Job Listings</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#94a3b8;'>Find live job postings and auto-fill the job description for instant analysis.</p>", unsafe_allow_html=True)
    avs(2)

    col1, col2 = st.columns([4, 1])
    with col1:
        search_term = st.text_input("", placeholder="🔍  Search for a job title (e.g. Python Developer, Data Scientist)", label_visibility="collapsed")
    with col2:
        search_btn = st.button("Search Jobs", use_container_width=True)

    if search_btn and search_term:
        with st.spinner("🔎 Fetching live job listings..."):
            jobs = fetch_jobs(search_term)

        if jobs:
            st.markdown(f"""<div style='background:rgba(16,185,129,0.1); border:1px solid rgba(110,231,183,0.3);
                            border-radius:10px; padding:0.8rem; margin:1rem 0;'>
                ✅ Found <strong style='color:#6ee7b7;'>{len(jobs)} jobs</strong> for "{search_term}". 
                Select one to auto-fill the job description below.
            </div>""", unsafe_allow_html=True)

            for i, job in enumerate(jobs):
                title = job.get("title", "N/A")
                company = job.get("company_name", "N/A")
                location = job.get("location", "Remote")
                desc = job.get("description", "No description available.")

                with st.expander(f"💼 {title} — {company} · 📍 {location}"):
                    st.markdown(f"<div style='color:#cbd5e1; line-height:1.7;'>{desc[:1000] + '...' if len(desc) > 1000 else desc}</div>", unsafe_allow_html=True)
                    if st.button("✅ Use this Job Description", key=f"job_{i}"):
                        st.session_state["selected_jd"] = desc
                        st.success("Job description loaded! Scroll down to analyze your resume.")
        else:
            st.warning("No jobs found. Try a different search term.")

    avs(3)
    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
