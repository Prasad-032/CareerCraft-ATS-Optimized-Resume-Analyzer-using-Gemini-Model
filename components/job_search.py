import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space as avs
from utils.job_utils import fetch_jobs

def render_job_search():
    st.markdown("<h1 style='text-align:center;'>Search Real Job Listings</h1>", unsafe_allow_html=True)
    st.markdown("""<p style='text-align:center; color:#94a3b8;'>
        Find live job postings and auto-fill the job description for instant analysis.<br>
        <span style='font-size:0.8rem; color:#6b7280;'>Note: Job listings are sourced from Arbeitnow (Europe-focused). Results may vary for other regions.</span>
    </p>""", unsafe_allow_html=True)
    avs(2)

    col1, col2 = st.columns([4, 1])
    with col1:
        search_term = st.text_input(
            "",
            placeholder="🔍  Search for a job title (e.g. Python Developer, Data Scientist)",
            label_visibility="collapsed"
        )
    with col2:
        search_btn = st.button("Search Jobs", use_container_width=True)

    if search_btn and not search_term.strip():
        st.warning("Please enter a job title to search.")

    if search_btn and search_term.strip():
        with st.spinner("🔎 Fetching live job listings..."):
            jobs = fetch_jobs(search_term)

        if jobs:
            st.markdown(f"""<div style='background:rgba(16,185,129,0.1); border:1px solid rgba(110,231,183,0.3);
                            border-radius:10px; padding:0.8rem; margin:1rem 0;'>
                ✅ Found <strong style='color:#6ee7b7;'>{len(jobs)} jobs</strong> for "<em>{search_term}</em>".
                Click a listing to expand, then click "Use this Job Description" to auto-fill the analyzer below.
            </div>""", unsafe_allow_html=True)

            for i, job in enumerate(jobs):
                title = job.get("title", "N/A")
                company = job.get("company_name", "N/A")
                location = job.get("location", "Remote")
                desc = job.get("description", "No description available.")
                tags = job.get("tags", [])

                with st.expander(f"💼 {title} — {company} · 📍 {location}"):
                    if tags:
                        tag_html = " ".join([
                            f"<span style='background:rgba(124,58,237,0.2); color:#c4b5fd; padding:0.2rem 0.6rem; border-radius:12px; font-size:0.75rem; margin:0.1rem; display:inline-block;'>{t}</span>"
                            for t in tags[:6]
                        ])
                        st.markdown(f"<div style='margin-bottom:0.8rem;'>{tag_html}</div>", unsafe_allow_html=True)

                    preview = desc[:1200] + "..." if len(desc) > 1200 else desc
                    st.markdown(f"<div style='color:#cbd5e1; line-height:1.7; font-size:0.9rem;'>{preview}</div>", unsafe_allow_html=True)

                    if st.button("✅ Use this Job Description", key=f"job_{i}"):
                        st.session_state["selected_jd"] = desc
                        st.session_state["jd_loaded"] = True
                        st.success("✅ Job description loaded! Scroll down to the Analyzer section.")
        else:
            st.warning("No jobs found. Try a different search term or check your internet connection.")

    avs(3)
    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
