# agents/pdf_assistant.py
import streamlit as st
from phi.assistant import Assistant
from phi.storage.assistant.postgres import PgAssistantStorage
from phi.knowledge.pdf import PDFKnowledgeBase
from phi.vectordb.chroma import ChromaDb
from phi.llm.groq import Groq  # You can check phi data docs to change the model
import os
import tempfile
from dotenv import load_dotenv

load_dotenv()

class PDFAssistant:
    def __init__(self):
        self.db_url = os.getenv("DATABASE_URL")
        if not self.db_url:
            st.error("DATABASE_URL is not set in .env file.")
            st.stop()

        self.storage = PgAssistantStorage(table_name="pdf_assistant", db_url=self.db_url)
        self.llm = Groq(id="llama-3.3-70b-versatile")  # Users can change the model in phi data docs
        # Knowledge base is initialized after file upload

    def run(self):
        if "uploaded_file" not in st.session_state:
            st.session_state["uploaded_file"] = None

        if st.session_state["uploaded_file"] is None:
            st.session_state["uploaded_file"] = st.file_uploader("Upload a PDF file", type="pdf")

        if st.session_state["uploaded_file"] is not None and "pdf_loaded" not in st.session_state:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
                temp_pdf.write(st.session_state["uploaded_file"].read())
                temp_pdf_path = temp_pdf.name

            try:
                with st.spinner("Initializing PDF Knowledge Base..."):
                    self.knowledge_base = PDFKnowledgeBase(
                        path=temp_pdf_path,
                        vector_db=ChromaDb(collection="recipes", path="./chromadb"),
                        llm=self.llm
                    )
                    self.knowledge_base.load()
                    st.session_state["knowledge_base"] = self.knowledge_base
                    st.session_state["pdf_loaded"] = True
                    st.session_state["temp_pdf_path"] = temp_pdf_path
                    st.success("PDF Knowledge Base initialized!")
            except Exception as e:
                st.error(f"Error loading PDF: {e}")
                st.stop()
                return

        if "pdf_loaded" in st.session_state and st.session_state["pdf_loaded"]:
            if 'run_id' not in st.session_state:
                st.session_state['run_id'] = None
                st.session_state['user'] = "user"
                existing_run_ids = self.storage.get_all_run_ids(st.session_state['user'])
                if len(existing_run_ids) > 0:
                    st.session_state['run_id'] = existing_run_ids[0]

            self.assistant = Assistant(
                run_id=st.session_state['run_id'],
                user_id=st.session_state['user'],
                knowledge_base=st.session_state["knowledge_base"],
                storage=self.storage,
                show_tool_calls=True,
                search_knowledge=True,
                read_chat_history=True,
            )

            if st.session_state['run_id'] is None:
                 st.session_state['run_id'] = self.assistant.run_id
                 st.write(f"Started Run: {st.session_state['run_id']}")
            else:
                 st.write(f"Continuing Run: {st.session_state['run_id']}")

            user_input = st.text_input("Ask a question about the PDF:", key="pdf_input")
            if st.button("Submit", key="submit_query"):
                if user_input:
                    with st.spinner("Processing..."):
                        response = self.assistant.run(user_input, stream=False)
                        st.markdown(response)
                else:
                    st.warning("Please enter a question.")

            if "temp_pdf_path" in st.session_state:
                if os.path.exists(st.session_state["temp_pdf_path"]):
                    try:
                        os.unlink(st.session_state["temp_pdf_path"])
                    except Exception as e:
                        st.error(f"Could not delete temp file: {e}")
                del st.session_state["temp_pdf_path"]

        elif st.session_state["uploaded_file"] is not None:
            pass
        else:
            st.info("Please upload a PDF file to get started.")