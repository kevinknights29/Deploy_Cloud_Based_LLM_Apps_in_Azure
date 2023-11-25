from __future__ import annotations

from io import StringIO

import PyPDF2
import streamlit as st
from langchain.text_splitter import CharacterTextSplitter

from src.llm import openai
from src.utils import common
from src.vectordb import qdrant

logger = common.create_logger(__name__)

APP_TITLE = common.config()["app"]["title"]
APP_ONBOARDING = common.config()["app"]["onboarding"]
INPUT_INSTRUCTION = common.config()["app"]["input"]
UPLOAD_INSTRUCTION = common.config()["app"]["upload"]
ALLOWED_EXTENSIONS = common.config()["settings"]["extensions"]
RAG_CHECBOX = common.config()["app"]["rag"]["checkbox"]
RAG_INPUT_INSTRUCTION = common.config()["app"]["rag"]["input"]
RAG_SEARCH_BUTTON = common.config()["app"]["rag"]["search"]
SELECT_BOX_INSTRUCTION = common.config()["app"]["select_box"]["instruction"]
SELECT_BOX_OPTIONS = common.config()["app"]["select_box"]["options"]
OUTPUT_INSTRUCTION = common.config()["app"]["output"]
SUBMIT_BUTTON = common.config()["app"]["submit"]

# Set the page title and onboarding text
st.title(APP_TITLE)
st.markdown("\n".join(APP_ONBOARDING))

# Upload the content
content = None
docs = None
is_rag = st.checkbox(RAG_CHECBOX)
uploaded_file = st.file_uploader(UPLOAD_INSTRUCTION, type=ALLOWED_EXTENSIONS)
if uploaded_file is not None:
    if uploaded_file.type == "application/pdf":
        # Read the PDF file
        reader = PyPDF2.PdfReader(uploaded_file)
        # Extract the content
        page_content = []
        for page in reader.pages:
            if page.extract_text() is not None:
                clean_page = page.extract_text().strip().replace("\n", " ")
                page_content.append(clean_page)
        content = "\n".join(page_content)
        if is_rag:
            # Split the content into chunks
            text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
            docs = text_splitter.create_documents([content])
            qdrant.insert_documents(collection="content", documents=docs)
    else:
        # To read file as bytes:
        bytes_data = uploaded_file.getvalue()
        # To convert to a string based IO:
        stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
        # To read file as string:
        content = stringio.read()

# Enable Retrieval (RAG) if the user wants to
query = None
if is_rag:
    st.text_input(RAG_INPUT_INSTRUCTION, value=query)
    if st.button(RAG_SEARCH_BUTTON):
        # Fetch the content from the database
        content = qdrant.query_collection(collection="content", query=query)
    else:
        content = "👀 Information will be searched from the database."

# Select the content and tone
content = st.text_area(INPUT_INSTRUCTION, value=content)
tone = st.selectbox(SELECT_BOX_INSTRUCTION, SELECT_BOX_OPTIONS)

# Generate the post
if st.button(SUBMIT_BUTTON):
    if is_rag:
        # Fetch the content from the database
        content = qdrant.query_collection(collection="content", query=query)
    post_content = openai.generate_post(content, tone)
    st.text_area(OUTPUT_INSTRUCTION, value=post_content, height=500)
