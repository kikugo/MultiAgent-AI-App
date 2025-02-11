#app.py
import streamlit as st
from agents.video_analyzer import VideoAnalyzer
from agents.financial_agent import FinancialAgent
from agents.pdf_assistant import PDFAssistant
from utils.helpers import configure_google_api
from dotenv import load_dotenv

load_dotenv()

# Streamlit page configuration
st.set_page_config(
    page_title="Multi-Agent AI Platform",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"  # Sidebar open by default
)

# Sidebar for agent selection and theme settings
with st.sidebar:
    st.markdown("### 🚀 Choose Your AI Assistant")
    selected_agent = st.selectbox(
        "Select an Agent",
        ("Video Analyzer", "Financial Agent", "PDF Assistant")
    )
    st.markdown("### 🎨 Appearance Settings")

    # Theme selection using radio buttons in the sidebar
    if "theme" not in st.session_state:
        st.session_state["theme"] = "Dark"  # Default theme is Dark

    theme = st.radio(
        "Select a Theme",
        ("Light", "Dark"),
        horizontal=True,
        label_visibility="collapsed",  # Hide radio button labels
        index=1 if st.session_state["theme"] == "Dark" else 0,  # Set index based on current theme
        key="theme_radio" # Key for the radio button
    )
    st.session_state["theme"] = theme # Update session state with selected theme

# Apply selected theme to the Streamlit app
if st.session_state["theme"] == "Dark":
    st.markdown("""
        <style>
        /* Dark theme CSS styles */
        .stApp {
            background-color: #0e1117;
            color: #fafafa;
        }
        
        /* Containers */
        .stTextArea textarea {
            background-color: #262730 !important;
            color: #fafafa !important;
            border-radius: 10px !important;
            border: 1px solid #464B5C !important;
            padding: 15px !important;
            font-size: 16px !important;
        }
        
        /* Modern Button Styling */
        .stButton button {
            background: linear-gradient(45deg, #7C3AED, #5B21B6) !important;
            color: white !important;
            border: none !important;
            border-radius: 10px !important;
            padding: 10px 25px !important;
            font-weight: 500 !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1) !important;
        }
        
        .stButton button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 8px -1px rgba(0, 0, 0, 0.2) !important;
        }
        
        /* Results Container */
        .analysis-result {
            padding: 2rem;
            background-color: #262730;
            border-radius: 15px;
            margin-top: 2rem;
            color: #fafafa;
            border: 1px solid #464B5C;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }
        
        /* File Uploader */
        .uploadedFile {
            background-color: #262730 !important;
            border-radius: 10px !important;
            padding: 15px !important;
            border: 2px dashed #464B5C !important;
        }
        
        /* Headers */
        h1, h2, h3 {
            color: #fafafa !important;
            font-weight: 600 !important;
            letter-spacing: -0.5px !important;
        }
        
        /* Markdown text */
        div[data-testid="stMarkdownContainer"] {
            color: #fafafa;
            line-height: 1.6;
        }
        
        /* Sidebar */
        .css-1d391kg {
            background-color: #1a1c23 !important;
        }
        
        /* Progress bar */
        .stProgress > div > div > div > div {
            background-color: #7C3AED !important;
        }
        </style>
        """, unsafe_allow_html=True)
else:
    st.markdown("""
        <style>
        /* Light theme CSS styles */
        .stApp {
            background-color: #ffffff;
            color: #111827;
        }
        
        /* Containers */
        .stTextArea textarea {
            background-color: #f3f4f6 !important;
            color: #111827 !important;
            border-radius: 10px !important;
            border: 1px solid #e5e7eb !important;
            padding: 15px !important;
            font-size: 16px !important;
        }
        
        /* Modern Button Styling */
        .stButton button {
            background: linear-gradient(45deg, #2563eb, #1d4ed8) !important;
            color: white !important;
            border: none !important;
            border-radius: 10px !important;
            padding: 10px 25px !important;
            font-weight: 500 !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 6px -1px rgba(37, 99, 235, 0.1) !important;
        }
        
        .stButton button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 8px -1px rgba(37, 99, 235, 0.2) !important;
        }
        
        /* Results Container */
        .analysis-result {
            padding: 2rem;
            background-color: #f3f4f6;
            border-radius: 15px;
            margin-top: 2rem;
            color: #111827;
            border: 1px solid #e5e7eb;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }
        
        /* File Uploader */
        .uploadedFile {
            background-color: #f3f4f6 !important;
            border-radius: 10px !important;
            padding: 15px !important;
            border: 2px dashed #e5e7eb !important;
        }
        
        /* Headers */
        h1, h2, h3 {
            color: #111827 !important;
            font-weight: 600 !important;
            letter-spacing: -0.5px !important;
        }
        
        /* Markdown text */
        div[data-testid="stMarkdownContainer"] {
            color: #111827;
            line-height: 1.6;
        }
        
        /* Progress bar */
        .stProgress > div > div > div > div {
            background-color: #2563eb !important;
        }
        </style>
        """, unsafe_allow_html=True)


# Main application title
st.title("Multi-Agent AI Platform")

# Agent selection logic to run the selected agent
if selected_agent == "Video Analyzer":
    st.header("🎥 Video AI Analyzer")
    video_analyzer = VideoAnalyzer()
    video_analyzer.run()

elif selected_agent == "Financial Agent":
    st.header("💰 Financial Agent")
    financial_agent = FinancialAgent()
    ticker = st.text_input("Enter Stock Ticker (e.g., NVDA):", "") # Input for stock ticker
    if st.button("Get Financial Data"):
        financial_agent.run(ticker=ticker)  # Run financial agent with ticker

elif selected_agent == "PDF Assistant":
    st.header("📄 PDF Assistant")
    pdf_assistant = PDFAssistant()
    pdf_assistant.run()