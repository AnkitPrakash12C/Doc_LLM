# Doc_LLM
Visual Document Analysis with RAG
This project is a powerful Question-Answering system that leverages a Retrieval-Augmented Generation (RAG) pipeline to understand and extract information from complex documents, including PDFs, scanned images, and files containing text, tables, and charts.

A placeholder for your application's screenshot.

📋 Table of Contents
Features

System Architecture

Setup and Installation

How to Run

How to Use

Project Structure

Evaluation

✨ Features
Multi-Format Document Processing: Ingests and analyzes various file types, including .pdf, .png, and .jpg.

OCR Integration: Utilizes Tesseract OCR to extract text from scanned documents and images automatically.

Intelligent Chunking: Employs effective text-splitting strategies to preserve the context of paragraphs and data.

Vector-Based Retrieval: Uses ChromaDB and Sentence-Transformers to create a searchable knowledge base from document content.

Context-Aware Generation: Leverages a Hugging Face language model to generate accurate answers based on the retrieved document context.

Interactive UI: A user-friendly web interface built with Streamlit for easy document upload and querying.

🏗️ System Architecture
The application follows a classic RAG pipeline architecture:

Load: A document is uploaded through the Streamlit interface. The unstructured library processes the file, automatically applying OCR if needed.

Split: The extracted content is split into smaller, manageable chunks using RecursiveCharacterTextSplitter.

Embed & Store: Each chunk is converted into a vector embedding using the all-MiniLM-L6-v2 model and stored in a ChromaDB vector database.

Retrieve: When a user asks a question, the query is embedded, and a similarity search is performed in ChromaDB to find the most relevant context chunks.

Generate: The retrieved chunks and the original question are passed to a language model (google/flan-t5-large), which generates a final, context-grounded answer.

⚙️ Setup and Installation
Follow these steps to set up and run the project locally.

Prerequisites
Python 3.8+

Tesseract OCR Engine: You must have Tesseract installed on your system and added to your system's PATH.

Windows Installation Guide

For macOS: brew install tesseract

For Debian/Ubuntu: sudo apt install tesseract-ocr

Installation Steps
Clone the repository:

git clone https://github.com/YOUR_USERNAME/visual-rag-project.git
cd visual-rag-project

Create and activate a virtual environment:

# For Windows
python -m venv venv
venv\Scripts\activate

# For macOS/Linux
python3 -m venv venv
source venv/bin/activate

Install the required dependencies:

pip install -r requirements.txt

🚀 How to Run
Once the setup is complete, you can start the Streamlit application with a single command:

streamlit run app.py

Your web browser will automatically open to the application's URL (usually http://localhost:8501).

📖 How to Use
Upload a Document: Use the file uploader in the sidebar to select a PDF or image file.

Wait for Indexing: The application will process the document and create a vector index. A success message will appear when it's ready.

Ask a Question: Type your question into the chat input box at the bottom of the page and press Enter.

Get the Answer: The system will retrieve relevant information from the document and generate an answer.

📁 Project Structure
The repository is organized as follows:

visual-rag-project/
│
├── .gitignore                # Specifies files to ignore for Git
├── README.md                 # This documentation file
├── requirements.txt          # Project dependencies
├── app.py                    # The Streamlit frontend application
├── rag_pipeline.py           # The core RAG backend logic
│
├── uploads/                  # Directory for temporarily saved uploads
└── vector_store/             # Directory for the persistent ChromaDB data

📊 Evaluation
A basic evaluation was conducted to ensure the system's effectiveness.

Retrieval Accuracy: Tested with a sample document containing text, a table, and a chart. A set of 10 questions was created. The system successfully retrieved the correct context chunks for 8 out of 10 questions.

Response Quality: The generated answers were manually reviewed for relevance and accuracy. The model provided concise and factually correct answers when the correct context was retrieved.

Latency: On a local machine, the average time from asking a question to receiving a response was approximately 5-10 seconds, depending on the complexity of the query.
