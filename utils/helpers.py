#utils/helpers.py
import google.generativeai as genai
import os
import streamlit as st
from urllib.parse import urlparse, urlunparse

def configure_google_api():
    """
    Configures the Google Generative AI API using the API key from environment variables.
    Displays an error message in Streamlit if the API key is not set.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        st.error("⚠️ GOOGLE_API_KEY is not set in the environment variables")
        st.stop()
    genai.configure(api_key=api_key)

def sanitize_url(url_string):
    """
    Sanitizes a URL string to ensure it is valid and properly formatted.
    If the URL is invalid or cannot be parsed, it returns a placeholder '#invalid-url'.

    This function helps prevent issues with Markdown rendering of URLs in Streamlit.
    """
    try:
        result = urlparse(url_string) 
        if all([result.scheme, result.netloc]): 
            return urlunparse(result)  
        else:
            return "#invalid-url"
    except:
        return "#invalid-url"