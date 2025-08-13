import streamlit as st
import openai
import time
import os
from dotenv import load_dotenv

load_dotenv()

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.azure_endpoint = os.getenv("AZURE_ENDPOINT")
openai.api_type = os.getenv("OPENAI_API_TYPE")
openai.api_version = os.getenv("OPENAI_API_VERSION")

st.title("AI 시인 시몬")
st.write("시의 주제를 입력하고 내용을 작성하여 AI 시인이 시를 생성합니다.")

subject = st.text_input("시의 주제를 입력하세요.", key="subject_input")
content = st.text_area("시의 내용을 입력하세요.", key="content_input")

button_clicked = st.button("시 생성")

if button_clicked:
    messages = [
        {
            "role": "system",
            "content": "You are a AI poet."
        },
        {
            "role": "user",
            "content": f"시의 주제는 '{subject}' 이며 내용은 {content}. 시의 형식은 자유롭게"
        }
    ]

    with st.spinner("Wait for it...", show_time=True):
        response = openai.chat.completions.create(
            model="dev-gpt-4.1-mini",
            messages=messages,
            max_tokens=1000,
            temperature=0.9
        )
        st.success("시가 생성되었습니다!")

    st.write(response.choices[0].message.content)

