import re
import requests
import streamlit as st

def _strip_html(html: str) -> str:
    """Remove HTML tags and decode common entities."""
    text = re.sub(r"<br\s*/?>", "\n", html, flags=re.IGNORECASE)
    text = re.sub(r"<li\s*/?>", "\n• ", text, flags=re.IGNORECASE)
    text = re.sub(r"<[^>]+>", "", text)
    text = text.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">") \
               .replace("&nbsp;", " ").replace("&#39;", "'").replace("&quot;", '"')
    # Collapse excessive blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()

def fetch_jobs(search_term: str, limit: int = 10):
    try:
        url = "https://www.arbeitnow.com/api/job-board-api"
        response = requests.get(url, params={"search": search_term}, timeout=10)
        response.raise_for_status()
        jobs = response.json().get("data", [])[:limit]
        # Clean HTML from descriptions
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
