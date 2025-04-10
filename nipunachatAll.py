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
        # Generate synthetic data related to uploaded Excel sheet
        # if st.button("Generate Synthetic Data Related to Uploaded Excel Sheet"):
        #     synthetic_data = pd.DataFrame({
        #     col: [f"{val}_synthetic" if df[col].dtype == 'object' else val + 10 for val in df[col].head(10)]
        #     for col in df.columns
        #     })
        #     synthetic_file_path = tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx").name
        #     synthetic_data.to_excel(synthetic_file_path, index=False)
        #     st.success("Synthetic data generated successfully based on uploaded Excel sheet!")
        #     st.download_button(
        #     label="Download Synthetic Excel File",
        #     data=open(synthetic_file_path, "rb").read(),
        #     file_name="synthetic_data.xlsx",
        #     mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        #     )
        # Update synthetic data generation to use uploaded Excel columns
        # uploaded_columns = df.columns.tolist()
        # if st.button("Generate Synthetic Excel Data Based on Uploaded Columns"):
        #     synthetic_data = pd.DataFrame({
        #         col: [f"{col}_{i}" for i in range(1, 1001)] if df[col].dtype == 'object' else [i for i in range(1, 1001)]
        #         for col in uploaded_columns
        #     })
        #     synthetic_file_path = tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx").name
        #     synthetic_data.to_excel(synthetic_file_path, index=False)
        #     st.success("Synthetic Excel data generated successfully based on uploaded columns!")
        #     st.download_button(
        #         label="Download Synthetic Excel File",
        #         data=open(synthetic_file_path, "rb").read(),
        #         file_name="synthetic_data.xlsx",
        #         mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        #     )
        # Generate synthetic Excel data if requested
        # if st.button("Generate Synthetic Excel Data"):
        #     synthetic_data = pd.DataFrame({
        #         "ID": range(1, 1001),
        #         "Name": [f"Name_{i}" for i in range(1, 1001)],
        #         "Age": [20 + (i % 30) for i in range(1, 1001)],
        #         "City": [f"City_{i % 10}" for i in range(1, 1001)],
        #         "Salary": [30000 + (i % 5000) for i in range(1, 1001)],
        #     })
        #     synthetic_file_path = tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx").name
        #     synthetic_data.to_excel(synthetic_file_path, index=False)
        #     st.success("Synthetic Excel data generated successfully!")
        #     st.download_button(
        #         label="Download Synthetic Excel File",
        #         data=open(synthetic_file_path, "rb").read(),
        #         file_name="synthetic_data.xlsx",
        #         mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        #     )

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
# Display uploaded file data in a container with borders and sufficient width
if file_text:
    with st.container():
        st.markdown(
            f"""
            <div style="border: 2px solid #4CAF50; padding: 10px; border-radius: 5px; width: 100%;">
                <h4>Uploaded File Content</h4>
                <pre style="white-space: pre-wrap; word-wrap: break-word;">{file_text}</pre>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.text_area("File Data", file_text, height=500)
        
# Button to generate synthetic data by adding 100 more records based on the uploaded Excel data
        if st.button("Generate Synthetic Data with 100 Additional Records"):
            additional_data = pd.DataFrame({
            col: [f"{val}_extra" if df[col].dtype == 'object' else val + 5 for val in df[col].sample(100, replace=True)]
            for col in df.columns
            })
            synthetic_data = pd.concat([df, additional_data], ignore_index=True)
            synthetic_file_path = tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx").name
            synthetic_data.to_excel(synthetic_file_path, index=False)
            st.success("Synthetic data with 100 additional records generated successfully!")
            st.download_button(
            label="Download Synthetic Excel File",
            data=open(synthetic_file_path, "rb").read(),
            file_name="synthetic_data_with_100_records.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

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

    
