import os
from langchain_community.document_loaders import UnstructuredFileLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_huggingface import HuggingFacePipeline


# --- 1. DOCUMENT PROCESSING ---
def process_document(file_path):
    """
    Loads and splits a document into chunks for processing.
    UnstructuredFileLoader handles various formats (PDF, images, etc.).
    """
    print(f"Loading document: {file_path}")
    loader = UnstructuredFileLoader(file_path)
    documents = loader.load()

    print("Splitting documents into chunks...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = text_splitter.split_documents(documents)

    # Simple check for content
    if not chunks:
        print("Warning: No text chunks were extracted from the document.")
        return []

    print(f"Successfully split document into {len(chunks)} chunks.")
    return chunks


# --- 2. RAG PIPELINE CLASS ---
class RAGPipeline:
    def __init__(self):
        self.vector_store = None
        self.retriever = None
        self.chain = None
        self.embedding_model = None
        self._initialize_components()

    def _initialize_components(self):
        """
        Initializes the embedding model and the LLM for the RAG chain.
        """
        print("Initializing embedding model...")
        # Using a popular, lightweight sentence transformer model
        self.embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

        print("Initializing LLM...")
        # Using a placeholder for a HuggingFace model.
        # Replace "google/flan-t5-large" with your model of choice, e.g., "mistralai/Mistral-7B-Instruct-v0.1"
        # Ensure you have the necessary hardware or API access.
        llm = HuggingFacePipeline.from_model_id(
            model_id="google/flan-t5-large",
            task="text2text-generation",
            pipeline_kwargs={"max_new_tokens": 250},
        )

        print("Setting up RAG chain...")
        # The prompt template instructs the LLM on how to use the retrieved context
        template = """
        You are an assistant for question-answering tasks. 
        Use the following pieces of retrieved context to answer the question. 
        If you don't know the answer, just say that you don't know. 
        Use three sentences maximum and keep the answer concise.

        Question: {question} 
        Context: {context} 
        Answer:
        """
        prompt = PromptTemplate.from_template(template)

        self.chain = (
                {"context": self.retriever_runnable, "question": RunnablePassthrough()}
                | prompt
                | llm
                | StrOutputParser()
        )

    def retriever_runnable(self, question):
        """
        A runnable that passes the question to the retriever.
        This is needed to correctly wire the chain.
        """
        if self.retriever is None:
            return "No documents have been indexed yet. Please upload a file."
        return self.retriever

    def index_document(self, file_path):
        """
        Processes and indexes a single document into the vector store.
        """
        chunks = process_document(file_path)
        if not chunks:
            return "Failed to extract any content from the document."

        print(f"Creating vector store for {len(chunks)} chunks...")
        # Using ChromaDB for local, persistent storage
        vector_store_path = "vector_store"
        self.vector_store = Chroma.from_documents(
            documents=chunks,
            embedding=self.embedding_model,
            persist_directory=vector_store_path
        )
        self.retriever = self.vector_store.as_retriever(search_kwargs={'k': 3})

        # We need to re-initialize the chain to use the new retriever
        self._initialize_components()

        print("Document indexed successfully.")
        return "Document indexed successfully."

    def ask_question(self, question: str):
        """
        Takes a user question, retrieves relevant context, and generates an answer.
        """
        if self.chain is None or self.retriever is None:
            return "The system is not ready. Please index a document first."

        print(f"Invoking RAG chain with question: '{question}'")
        response = self.chain.invoke(question)
        print(f"Generated response: '{response}'")
        return response