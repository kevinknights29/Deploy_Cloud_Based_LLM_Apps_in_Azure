from __future__ import annotations

from io import StringIO

import PyPDF2
import streamlit as st

from src.llm import openai
from src.utils import common

logger = common.create_logger(__name__)

APP_TITLE = common.config()["app"]["title"]
APP_ONBOARDING = common.config()["app"]["onboarding"]
INPUT_INSTRUCTION = common.config()["app"]["input"]
UPLOAD_INSTRUCTION = common.config()["app"]["upload"]
ALLOWED_EXTENSIONS = common.config()["settings"]["extensions"]
RAG_CHECBOX = common.config()["app"]["rag"]["checkbox"]
RAG_INPUT_INSTRUCTION = common.config()["app"]["rag"]["input"]
SELECT_BOX_INSTRUCTION = common.config()["app"]["select_box"]["instruction"]
SELECT_BOX_OPTIONS = common.config()["app"]["select_box"]["options"]
OUTPUT_INSTRUCTION = common.config()["app"]["output"]
SUBMIT_BUTTON = common.config()["app"]["submit"]

# Set the page title and onboarding text
st.title(APP_TITLE)
st.markdown("\n".join(APP_ONBOARDING))

# Select the content and tone
content = None
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
    else:
        # To read file as bytes:
        bytes_data = uploaded_file.getvalue()
        # To convert to a string based IO:
        stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
        # To read file as string:
        content = stringio.read()

# Enable Retrieval (RAG) if the user wants to
query = None
is_rag = st.checkbox(RAG_CHECBOX)
if is_rag:
    st.text_input(RAG_INPUT_INSTRUCTION, value=query)
    # Embed the query

    # Fetch the content from the database

    content = "WIP: RAG is not yet implemented."

content = st.text_area(INPUT_INSTRUCTION, value=content)
tone = st.selectbox(SELECT_BOX_INSTRUCTION, SELECT_BOX_OPTIONS)

# Generate the post
if st.button(SUBMIT_BUTTON):
    post_content = openai.generate_post(content, tone)
    st.text_area(OUTPUT_INSTRUCTION, value=post_content, height=500)
