# agents/video_analyzer.py
import streamlit as st
import google.generativeai as genai
from pathlib import Path
import tempfile
import time
import os
from utils.helpers import configure_google_api

class VideoAnalyzer:
    """
    Agent for analyzing video content using Google Gemini API.
    Allows users to upload a video and ask questions about its content.
    """
    def __init__(self):
        """Initializes the VideoAnalyzer, configures Google API and sets up the Gemini model."""
        configure_google_api()  # Configure Google API using helper function
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp') # Initialize Gemini model

    def run(self):
        """
        Runs the Video Analyzer application in Streamlit.

        Handles video upload, displays video preview, and processes user queries.
        """
        col1, col2 = st.columns([2, 1]) # Create layout columns

        with col1:
            video_file = st.file_uploader(
                "📤 Upload your video",
                type=["mp4", "avi", "mov", "mkv"], # Supported video formats
                help="Supported formats: MP4, AVI, MOV, MKV"
            )

        with col2:
            st.markdown("### 💡 Sample Queries")
            st.markdown("""
            - Summarize the main events in this video
            - What are the key messages conveyed?
            - Describe the visual style and transitions
            - Analyze the tone and mood of the video
            """) # Display sample queries in the sidebar

        if video_file: # Process if a video file is uploaded
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_video:
                temp_video.write(video_file.read()) # Save uploaded video to a temporary file
                video_path = temp_video.name # Get the temporary file path

            st.markdown("### 📺 Preview")
            st.video(video_path, format="video/mp4", start_time=0) # Display video preview

            user_query = st.text_area(
                "🤔 What would you like to know about this video?",
                placeholder="Enter your question or analysis request here...",
                help="Be specific in your query for better results"
            ) # Text area for user query

            if st.button("🔍 Analyze Video", key="analyze_video_button", use_container_width=True): # Analyze button
                if not user_query:
                    st.warning("⚠️ Please provide a question or topic to analyze.") # Warn if no query is entered
                else:
                    try:
                        with st.spinner("🔄 Analyzing your video..."): # Show spinner during analysis
                            upload_response = genai.upload_file(video_path) # Upload video to Gemini API
                            st.info("upload processed") # Inform user that upload is processed
                            time.sleep(2) # Small delay for processing

                            analysis_prompt = f"""
                                Please analyze this video and provide insights for the following query:

                                QUERY: {user_query}

                                Please structure your response as follows:
                                1. 📝 Video Description: A detailed overview of what you observe
                                2. 🎯 Analysis: Specific answers to the query
                                3. 🔍 Additional Insights: Any relevant context or observations
                                """ # Prompt for video analysis

                            start_time = time.time()
                            response = self.model.generate_content([analysis_prompt, upload_response]) # Generate content using Gemini API
                            generation_time = time.time() - start_time
                            st.write(f"Generation time: {generation_time:.2f} seconds") # Display generation time

                            if response.text:
                                st.markdown("### 📊 Analysis Results")
                                st.markdown(
                                    f"""<div class="analysis-result">{response.text}</div>""",
                                    unsafe_allow_html=True # Display analysis results in a styled container
                                )
                            else:
                                st.warning("⚠️ No insights could be generated for this video (empty response).") # Warn if empty response

                    except Exception as e:
                        st.error(f"❌ Processing Error: {str(e)}") # Display error message
                    finally:
                        Path(video_path).unlink(missing_ok=True) # Delete temporary video file

        else:
            st.info("👆 Upload a video to get started!") # Info message when no video is uploaded

        st.markdown("---") # Separator line
        st.markdown(
            """
            <div style='text-align: center; color: #666;'>
            🛠️ Built with Streamlit & Gemini 2.0 |
            💡 For best results, use MP4 videos under 200MB
            </div>
            """,
            unsafe_allow_html=True # Footer message
        )