import requests
import streamlit as st

def fetch_jobs(search_term):
    try:
        url = "https://www.arbeitnow.com/api/job-board-api"
        response = requests.get(url, params={"search": search_term}, timeout=10)
        response.raise_for_status()
        return response.json().get("data", [])[:10]
    except Exception as e:
        st.error(f"Failed to fetch jobs: {e}")
        return []
