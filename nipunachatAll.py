import streamlit as st
from openai import AzureOpenAI
import pandas as pd
import pdfplumber
import tempfile

# Azure OpenAI Client
client = AzureOpenAI(
    api_key="28B4Ebqs18hV5OQSCmK3R3ID6wduJRmC9byWTF5tS9N9gIjgs7gLJQQJ99BDACHYHv6XJ3w3AAABACOGghQO",
    api_version="2024-12-01-preview",
    azure_endpoint="https://hemababu-day3training.openai.azure.com/"
)

st.title("🧠 Hemababu Chatbot")

# Session State Initialization
if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "system",
        "content": "You are a helpful assistant. If a file is uploaded, summarize it or answer based on its content."
    }]

if "file_uploaded" not in st.session_state:
    st.session_state.file_uploaded = False

# File Uploader (PDF and Excel only)
uploaded_file = st.file_uploader(
    "Upload PDF or Excel file",
    type=["pdf", "xlsx", "jpeg", "png", "jpg", "mp3", "mp4", "wav"],
    accept_multiple_files=True,
)

file_text = ""

for file in uploaded_file:
    file_type = file.type

    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(file.read())
        tmp_path = tmp_file.name

    if "pdf" in file_type:
        with pdfplumber.open(tmp_path) as pdf:
            file_text += "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])

    elif "excel" in file_type or "spreadsheet" in file_type:
        df = pd.read_excel(tmp_path)
        file_text += df.to_markdown()
    
    elif "image" in file_type:
        # Handle image files if needed
        st.image(tmp_path, caption="Uploaded Image", use_column_width=True)
        file_text += f"Image uploaded: {file.name}\n"
    
    elif "audio" in file_type:
        # Handle audio files if needed
        st.audio(tmp_path, format="audio/wav")
        file_text += f"Audio uploaded: {file.name}\n"

    if file_text:
        st.session_state.messages.append({
            "role": "user",
            "content": f"I've uploaded a file. Please analyze the following content:\n{file_text}"
        })
        st.session_state.file_uploaded = True

# if uploaded_file and not st.session_state.file_uploaded:
#     file_type = uploaded_file.type

#     with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
#         tmp_file.write(uploaded_file.read())
#         tmp_path = tmp_file.name

#     if "pdf" in file_type:
#         with pdfplumber.open(tmp_path) as pdf:
#             file_text = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])

#     elif "excel" in file_type or "spreadsheet" in file_type:
#         df = pd.read_excel(tmp_path)
#         file_text = df.to_markdown()

#     if file_text:
#         st.session_state.messages.append({
#             "role": "user",
#             "content": f"I've uploaded a file. Please analyze the following content:\n{file_text}"
#         })
#         st.session_state.file_uploaded = True

# Show Chat History
for msg in st.session_state.messages[1:]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat Input
if prompt := st.chat_input("Ask anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    visible_messages = [
        {"role": m["role"], "content": m["content"]}
        for m in st.session_state.messages
    ]

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=visible_messages
            )
            reply = response.choices[0].message.content
            st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})
