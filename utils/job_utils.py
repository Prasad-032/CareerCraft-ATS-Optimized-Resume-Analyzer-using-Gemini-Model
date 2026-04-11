import re
import requests
import streamlit as st

def _strip_html(html: str) -> str:
    """Convert HTML job description to clean readable plain text."""
    # Block-level elements → newlines
    html = re.sub(r"<h[1-6][^>]*>", "\n\n", html, flags=re.IGNORECASE)
    html = re.sub(r"</h[1-6]>", "\n", html, flags=re.IGNORECASE)
    html = re.sub(r"<p[^>]*>", "\n", html, flags=re.IGNORECASE)
    html = re.sub(r"</p>", "\n", html, flags=re.IGNORECASE)
    html = re.sub(r"<br\s*/?>", "\n", html, flags=re.IGNORECASE)
    html = re.sub(r"</?ul[^>]*>", "\n", html, flags=re.IGNORECASE)
    html = re.sub(r"</?ol[^>]*>", "\n", html, flags=re.IGNORECASE)
    html = re.sub(r"<li[^>]*>", "\n  • ", html, flags=re.IGNORECASE)
    html = re.sub(r"</li>", "", html, flags=re.IGNORECASE)
    html = re.sub(r"</?strong[^>]*>", "", html, flags=re.IGNORECASE)
    html = re.sub(r"</?em[^>]*>", "", html, flags=re.IGNORECASE)
    html = re.sub(r"</?b[^>]*>", "", html, flags=re.IGNORECASE)
    html = re.sub(r"</?i[^>]*>", "", html, flags=re.IGNORECASE)
    html = re.sub(r"</?span[^>]*>", "", html, flags=re.IGNORECASE)
    html = re.sub(r"</?div[^>]*>", "\n", html, flags=re.IGNORECASE)
    # Strip any remaining tags
    html = re.sub(r"<[^>]+>", "", html)
    # Decode HTML entities
    html = (html
        .replace("&amp;", "&")
        .replace("&lt;", "<")
        .replace("&gt;", ">")
        .replace("&nbsp;", " ")
        .replace("&#39;", "'")
        .replace("&quot;", '"')
        .replace("&ndash;", "–")
        .replace("&mdash;", "—")
        .replace("&bull;", "•")
    )
    # Collapse excessive blank lines and trailing spaces
    html = re.sub(r" +", " ", html)
    html = re.sub(r"\n{3,}", "\n\n", html)
    return html.strip()

def fetch_jobs(search_term: str, limit: int = 10):
    try:
        url = "https://www.arbeitnow.com/api/job-board-api"
        response = requests.get(url, params={"search": search_term}, timeout=10)
        response.raise_for_status()
        jobs = response.json().get("data", [])[:limit]
        for job in jobs:
            job["description"] = _strip_html(job.get("description", ""))
        return jobs
    except requests.exceptions.ConnectionError:
        st.error("❌ No internet connection. Please check your network and try again.")
        return []
    except requests.exceptions.Timeout:
        st.error("❌ Request timed out. The job board may be slow — try again.")
        return []
    except Exception as e:
        st.error(f"❌ Failed to fetch jobs: {e}")
        return []
