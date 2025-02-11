# utils/helpers.py
import google.generativeai as genai
import os
import streamlit as st
from urllib.parse import urlparse, urlunparse

def configure_google_api():
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        st.error("⚠️ GOOGLE_API_KEY is not set in the environment variables")
        st.stop()
    genai.configure(api_key=api_key)

def sanitize_url(url_string):
    try:
        result = urlparse(url_string)
        if all([result.scheme, result.netloc]):
            return urlunparse(result)
        else:
            return "#invalid-url"
    except:
        return "#invalid-url"