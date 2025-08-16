# app.py

import os
import streamlit as st
from rag_pipeline import RAGPipeline

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Visual Document RAG 📄",
    page_icon="🔍",
    layout="wide"
)

# --- DIRECTORY SETUP ---
# Create necessary directories if they don't exist
if not os.path.exists("uploads"):
    os.makedirs("uploads")
if not os.path.exists("vector_store"):
    os.makedirs("vector_store")

# --- STATE MANAGEMENT ---
# Initialize the RAG pipeline in Streamlit's session state
if 'rag_pipeline' not in st.session_state:
    st.session_state.rag_pipeline = RAGPipeline()
    print("RAG Pipeline initialized in session state.")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- UI LAYOUT ---
st.title("Visual Document Analysis with RAG 🔍")
st.markdown("""
Welcome! Upload a document (PDF, JPG, PNG) and ask questions about its content. 
The system uses Retrieval-Augmented Generation to find answers within your document.
""")

# --- SIDEBAR FOR FILE UPLOAD ---
with st.sidebar:
    st.header("Upload Your Document")
    uploaded_file = st.file_uploader(
        "Choose a PDF, JPG, or PNG file",
        type=["pdf", "jpg", "png"]
    )

    if uploaded_file is not None:
        # Save the file temporarily
        file_path = os.path.join("uploads", uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.success(f"File '{uploaded_file.name}' uploaded successfully.")

        # Index the document
        with st.spinner("Processing and indexing document... This may take a moment."):
            try:
                message = st.session_state.rag_pipeline.index_document(file_path)
                st.success(message)
            except Exception as e:
                st.error(f"An error occurred during indexing: {e}")

# --- MAIN CHAT INTERFACE ---

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Ask a question about your document..."):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.spinner("Thinking..."):
        try:
            # Generate response  RAG pipeline
            response = st.session_state.rag_pipeline.ask_question(prompt)

            with st.chat_message("assistant"):
                st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

        except Exception as e:
            st.error(f"An error occurred while getting the answer: {e}")