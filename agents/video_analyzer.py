# agents/video_analyzer.py
import streamlit as st
import google.generativeai as genai
from pathlib import Path
import tempfile
import time
import os
from utils.helpers import configure_google_api

class VideoAnalyzer:
    def __init__(self):
        configure_google_api()
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')  # You can check phi data docs to change the model

    def run(self):
        col1, col2 = st.columns([2, 1])

        with col1:
            video_file = st.file_uploader(
                "📤 Upload your video",
                type=["mp4", "avi", "mov", "mkv"],
                help="Supported formats: MP4, AVI, MOV, MKV"
            )

        with col2:
            st.markdown("### 💡 Sample Queries")
            st.markdown("""
            - Summarize the main events in this video
            - What are the key messages conveyed?
            - Describe the visual style and transitions
            - Analyze the tone and mood of the video
            """)

        if video_file:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_video:
                temp_video.write(video_file.read())
                video_path = temp_video.name

            st.markdown("### 📺 Preview")
            st.video(video_path, format="video/mp4", start_time=0)

            user_query = st.text_area(
                "🤔 What would you like to know about this video?",
                placeholder="Enter your question or analysis request here...",
                help="Be specific in your query for better results"
            )

            if st.button("🔍 Analyze Video", key="analyze_video_button", use_container_width=True):
                if not user_query:
                    st.warning("⚠️ Please provide a question or topic to analyze.")
                else:
                    try:
                        with st.spinner("🔄 Analyzing your video..."):
                            upload_response = genai.upload_file(video_path)
                            st.info("upload processed")
                            time.sleep(2)  # Small delay for API processing.

                            analysis_prompt = f"""
                                Please analyze this video and provide insights for the following query:

                                QUERY: {user_query}

                                Please structure your response as follows:
                                1. 📝 Video Description: A detailed overview of what you observe
                                2. 🎯 Analysis: Specific answers to the query
                                3. 🔍 Additional Insights: Any relevant context or observations
                                """

                            start_time = time.time()
                            response = self.model.generate_content([analysis_prompt, upload_response])
                            generation_time = time.time() - start_time
                            st.write(f"Generation time: {generation_time:.2f} seconds")

                            if response.text:
                                st.markdown("### 📊 Analysis Results")
                                st.markdown(
                                    f"""<div class="analysis-result">{response.text}</div>""",
                                    unsafe_allow_html=True
                                )
                            else:
                                st.warning("⚠️ No insights could be generated for this video (empty response).")

                    except Exception as e:
                        st.error(f"❌ Processing Error: {str(e)}")
                    finally:
                        Path(video_path).unlink(missing_ok=True)

        else:
            st.info("👆 Upload a video to get started!")

        st.markdown("---")
        st.markdown(
            """
            <div style='text-align: center; color: #666;'>
            🛠️ Built with Streamlit & Gemini 2.0 |
            💡 For best results, use MP4 videos under 200MB
            </div>
            """,
            unsafe_allow_html=True
        )