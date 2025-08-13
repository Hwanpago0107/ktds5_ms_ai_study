import openai
import os
from dotenv import load_dotenv
import streamlit as st
import pymupdf  # PyMuPDF

load_dotenv()

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.azure_endpoint = os.getenv("AZURE_ENDPOINT")
openai.api_type = os.getenv("OPENAI_API_TYPE")
openai.api_version = os.getenv("OPENAI_API_VERSION")

# LLM 응답을 가져오는 함수
def get_llm_response(messages):
    response = openai.chat.completions.create(
        model="dev-gpt-4.1-mini",
        messages=messages,
        max_tokens=1000,
        temperature=0.7
    )

    return response.choices[0].message.content

def extract_text_from_pdf(pdf_file):
    doc = pymupdf.open(stream=pdf_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# streamlit을 사용하여 사용자 인터페이스를 생성
st.title("Azure OpenAI Chatbot")
st.write("궁금한 것을 물어보세요. AI가 답변해 드립니다.")

# 채팅 기록의 초기화
if 'messages' not in st.session_state:
    st.session_state.messages = []

# 채팅 기록의 표시
for message in st.session_state.messages:
    st.chat_message(message['role']).write(message['content'])

# 파일 업로드 기능
uploaded_file = st.file_uploader("파일을 업로드하세요 (선택 사항)", type=["pdf"])
if uploaded_file is not None:
    # 파일 내용을 읽어오는 로직 (예: 텍스트 파일이나 PDF의 경우)
    if uploaded_file.type == "application/pdf":
        content = extract_text_from_pdf(uploaded_file)
        st.session_state.messages.append({"role": "system", "content": content})
        st.chat_message("system").write("파일 내용이 시스템 메시지로 추가되었습니다.")
    else:
        st.error("지원하지 않는 파일 형식입니다. PDF만 업로드할 수 있습니다.")

# 사용자 입력을 받는 텍스트 박스
if user_input := st.chat_input("메시지를 입력하세요:", key="chat_input"):
    # 채팅 기록에 사용자 메시지를 추가
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    # LLM 응답을 가져옴
    with st.spinner("AI가 답변을 생성하는 중..."):
        response = get_llm_response(st.session_state.messages)
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.chat_message("assistant").write(response)

