import os
import re
import requests
import streamlit as st

def _clean_description(text: str) -> str:
    """Clean up any residual HTML and normalize whitespace."""
    text = re.sub(r"<[^>]+>", "", text)
    text = text.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">") \
               .replace("&nbsp;", " ").replace("&#39;", "'").replace("&quot;", '"')
    text = re.sub(r" +", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()

def fetch_jobs(search_term: str, limit: int = 10):
    api_key = os.getenv("RAPIDAPI_KEY")
    if not api_key:
        st.error("❌ RAPIDAPI_KEY is not set. Please add it to your .env file.")
        return []

    try:
        headers = {
            "x-rapidapi-host": "jsearch.p.rapidapi.com",
            "x-rapidapi-key": api_key
        }
        params = {
            "query": search_term,
            "num_pages": "1",
            "page": "1",
            "country": "us",
            "language": "en"
        }
        response = requests.get(
            "https://jsearch.p.rapidapi.com/search",
            headers=headers,
            params=params,
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
        jobs_raw = data.get("data", [])[:limit]

        # Normalize to a consistent structure
        jobs = []
        for j in jobs_raw:
            desc = _clean_description(j.get("job_description", "No description available."))
            city     = j.get("job_city") or ""
            state    = j.get("job_state") or ""
            country  = j.get("job_country") or ""
            location = ", ".join(filter(None, [city, state, country])) or "Remote"

            jobs.append({
                "title":        j.get("job_title", "N/A"),
                "company_name": j.get("employer_name", "N/A"),
                "location":     location,
                "remote":       j.get("job_is_remote", False),
                "description":  desc,
                "url":          j.get("job_apply_link") or j.get("job_google_link", ""),
                "tags":         j.get("job_required_skills") or [],
                "employment_type": j.get("job_employment_type", ""),
            })
        return jobs

    except requests.exceptions.ConnectionError:
        st.error("❌ No internet connection. Please check your network and try again.")
        return []
    except requests.exceptions.Timeout:
        st.error("❌ Request timed out. Please try again.")
        return []
    except Exception as e:
        st.error(f"❌ Failed to fetch jobs: {e}")
        return []
