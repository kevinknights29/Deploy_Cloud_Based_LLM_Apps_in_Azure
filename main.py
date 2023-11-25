import streamlit as st

from src.utils import common
from src.llm import openai

APP_TITLE = common.config()["app"]["title"]
APP_ONBOARDING = common.config()["app"]["onboarding"]
INPUT_INSTRUCTION = common.config()["app"]["input"]
SELECT_BOX_INSTRUCTION = common.config()["app"]["select_box"]["instruction"]
SELECT_BOX_OPTIONS = common.config()["app"]["select_box"]["options"]
OUTPUT_INSTRUCTION = common.config()["app"]["output"]
SUBMIT_BUTTON = common.config()["app"]["submit"]

st.title(APP_TITLE)
st.markdown("\n".join(APP_ONBOARDING))
content = st.text_area(INPUT_INSTRUCTION)
tone = st.selectbox(SELECT_BOX_INSTRUCTION, SELECT_BOX_OPTIONS)

if st.button(SUBMIT_BUTTON):
    post_content = openai.generate_post(content, tone)
    st.text_area(OUTPUT_INSTRUCTION, value=post_content, height=500)
