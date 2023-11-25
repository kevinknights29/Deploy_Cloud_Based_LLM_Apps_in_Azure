import streamlit as st

from src.utils import common

APP_TITLE = common.config()["app"]["title"]
APP_ONBOARDING = common.config()["app"]["onboarding"]
INPUT_INSTRUCTION = common.config()["app"]["input"]
SELECT_BOX_INSTRUCTION = common.config()["app"]["select_box"]["instruction"]
SELECT_BOX_OPTIONS = common.config()["app"]["select_box"]["options"]
OUTPUT_INSTRUCTION = common.config()["app"]["output"]
SUBMIT_BUTTON = common.config()["app"]["submit"]

st.title(APP_TITLE)
st.markdown("\n".join(APP_ONBOARDING))
st.text_area(INPUT_INSTRUCTION)
st.selectbox(SELECT_BOX_INSTRUCTION, SELECT_BOX_OPTIONS)
st.text_area(OUTPUT_INSTRUCTION)
st.button(SUBMIT_BUTTON)
