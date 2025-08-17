import os
import streamlit as st
from rag_pipeline import RAGPipeline

st.set_page_config(
    page_title="Visual Document RAG 📄",
    page_icon="🔍",
    layout="wide"
)


if not os.path.exists("uploads"):
    os.makedirs("uploads")
if not os.path.exists("vector_store"):
    os.makedirs("vector_store")

if 'rag_pipeline' not in st.session_state:
    st.session_state.rag_pipeline = RAGPipeline()
    print("RAG Pipeline initialized in session state.")

if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("Visual Document Analysis with RAG 🔍")
st.markdown("""
Welcome! Upload a document (PDF, JPG, PNG) and ask questions about its content. 
The system uses Retrieval-Augmented Generation to find answers within your document.
""")

with st.sidebar:
    st.header("Upload Your Document")
    uploaded_file = st.file_uploader(
        "Choose a PDF, JPG, or PNG file",
        type=["pdf", "jpg", "png"]
    )

    if uploaded_file is not None:
        file_path = os.path.join("uploads", uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.success(f"File '{uploaded_file.name}' uploaded successfully.")

        with st.spinner("Processing and indexing document... This may take a moment."):
            try:
                message = st.session_state.rag_pipeline.index_document(file_path)
                st.success(message)
            except Exception as e:
                st.error(f"An error occurred during indexing: {e}")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask a question about your document..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.spinner("Thinking..."):
        try:
            response = st.session_state.rag_pipeline.ask_question(prompt)

            with st.chat_message("assistant"):
                st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

        except Exception as e:
            st.error(f"An error occurred while getting the answer: {e}")
