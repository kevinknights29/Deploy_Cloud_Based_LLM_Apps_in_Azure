from __future__ import annotations

import streamlit as st
from langchain.embeddings.openai import OpenAIEmbeddings
from openai import OpenAI

CLIENT = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
SYSTEM_PROMPT = "You are a social media content writer. Your tasks is to be helpful, creative, clever, and engaging."
USER_PROMPT = """Create a visually striking and emotionally engaging social media post that reflects
the expertise of a digital marketer.
The content should be highly personalized, encouraging interaction through relatable
narratives or thought-provoking questions.
The post should be suitable for a diverse audience, aligned with the brand's values,
and optimized for high engagement on social media platforms."""


def generate_post(
    content: str,
    tone: str,
    client: OpenAI = CLIENT,
    system_prompt: str = SYSTEM_PROMPT,
    user_prompt: str = USER_PROMPT,
) -> str:
    """
    Generates a post using OpenAI's GPT-3.5-turbo model.

    Args:
        content (str): The content of the post.
        tone (str): The desired tone of the post.
        client (OpenAI, optional): The OpenAI client. Defaults to CLIENT.
        system_prompt (str, optional): The system prompt for the conversation. Defaults to SYSTEM_PROMPT.
        user_prompt (str, optional): The user prompt for the conversation. Defaults to USER_PROMPT.

    Returns:
        str: The generated post.

    """
    # Add the content and tone to the user prompt
    user_prompt += f"\n\nContent: ```{content}```\n\nTone: ```{tone}```"

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )
    return response.choices[0].message.content


def get_embeddings(
    client: OpenAI = CLIENT,
) -> OpenAIEmbeddings:
    """
    Get the OpenAI embeddings.

    Returns:
        OpenAIEmbeddings: The OpenAI embeddings.

    """
    return OpenAIEmbeddings(client=client.embeddings)
