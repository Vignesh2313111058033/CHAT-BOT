import os
from dotenv import load_dotenv

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

load_dotenv()

PDF_PATH = "chatbot/data/rules.pdf"
VECTOR_STORE_PATH = "chatbot/vectorstore"

def build_index():
    print("📄 Loading PDF...")
    loader = PyPDFLoader(PDF_PATH)
    docs = loader.load()

    print("🔍 Splitting text...")
    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
    chunks = splitter.split_documents(docs)

    print("🧠 Using MiniLM Embeddings...")
    embedder = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    print("📦 Building FAISS index...")
    vectorstore = FAISS.from_documents(chunks, embedder)

    vectorstore.save_local(VECTOR_STORE_PATH)

    print("✅ Index created successfully!")
    print(f"📁 Saved at: {VECTOR_STORE_PATH}")

if __name__ == "__main__":
    build_index()
