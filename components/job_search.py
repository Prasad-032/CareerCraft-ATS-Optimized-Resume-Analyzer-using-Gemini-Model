import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space as avs
from utils.job_utils import fetch_jobs

def render_job_search():
    st.markdown("<h1 style='text-align:center;'>Search Real Job Listings</h1>", unsafe_allow_html=True)
    st.markdown("""<p style='text-align:center; color:#94a3b8;'>
        Find live job postings and auto-fill the job description for instant analysis.<br>
        <span style='font-size:0.8rem; color:#6b7280;'>⚠️ Listings sourced from Arbeitnow — mostly Europe-based roles.</span>
    </p>""", unsafe_allow_html=True)
    avs(2)

    col1, col2 = st.columns([4, 1])
    with col1:
        search_term = st.text_input(
            "",
            placeholder="🔍  Search for a job title (e.g. Python Developer, Data Scientist)",
            label_visibility="collapsed",
            key="job_search_input"
        )
    with col2:
        search_btn = st.button("Search Jobs", use_container_width=True)

    # Fetch and store jobs in session state so they survive reruns
    if search_btn:
        if not search_term.strip():
            st.warning("⚠️ Please enter a job title to search.")
        else:
            with st.spinner("🔎 Fetching live job listings..."):
                jobs = fetch_jobs(search_term.strip())
            st.session_state["job_results"] = jobs
            st.session_state["job_search_term"] = search_term.strip()

    # Render results from session state (persists across reruns)
    jobs = st.session_state.get("job_results", [])
    search_label = st.session_state.get("job_search_term", "")

    if jobs:
        st.markdown(f"""<div style='background:rgba(16,185,129,0.1); border:1px solid rgba(110,231,183,0.3);
                        border-radius:10px; padding:0.8rem 1.2rem; margin:1rem 0; font-size:0.9rem;'>
            ✅ Found <strong style='color:#6ee7b7;'>{len(jobs)} jobs</strong> for "<em>{search_label}</em>".
            Expand a listing and click <strong style='color:#a78bfa;'>Use this Job Description</strong> to auto-fill the analyzer below.
        </div>""", unsafe_allow_html=True)

        for i, job in enumerate(jobs):
            title    = job.get("title", "N/A")
            company  = job.get("company_name", "N/A")
            location = job.get("location", "Remote")
            remote   = job.get("remote", False)
            tags     = job.get("tags", [])
            url      = job.get("url", "")
            desc     = job.get("description", "No description available.")

            label = f"💼 {title}  —  {company}  ·  📍 {location}"
            if remote:
                label += "  🌐 Remote"

            with st.expander(label):
                if tags:
                    tag_html = " ".join([
                        f"<span style='background:rgba(124,58,237,0.25); color:#c4b5fd; "
                        f"padding:0.2rem 0.7rem; border-radius:12px; font-size:0.75rem; "
                        f"margin:0.1rem; display:inline-block;'>{t}</span>"
                        for t in tags[:8]
                    ])
                    st.markdown(f"<div style='margin-bottom:0.8rem;'>{tag_html}</div>", unsafe_allow_html=True)

                preview = desc[:1500] + "\n\n[...truncated]" if len(desc) > 1500 else desc
                st.markdown(
                    f"<div style='color:#cbd5e1; line-height:1.75; font-size:0.88rem; "
                    f"white-space:pre-wrap;'>{preview}</div>",
                    unsafe_allow_html=True
                )

                col_a, col_b = st.columns([2, 1])
                with col_a:
                    if st.button("✅ Use this Job Description", key=f"use_job_{i}"):
                        st.session_state["selected_jd"] = desc
                        st.session_state["jd_loaded"] = True
                        st.rerun()
                with col_b:
                    if url:
                        st.markdown(
                            f"<a href='{url}' target='_blank' style='color:#60a5fa; font-size:0.85rem;'>🔗 View full listing</a>",
                            unsafe_allow_html=True
                        )

    elif st.session_state.get("job_search_term") and not jobs:
        st.warning("No jobs found. Try a different search term.")

    avs(3)
    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
