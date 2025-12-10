import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
import re

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
SYLLABUS_DIR = os.path.join(BASE_DIR, "chatbot/data/syllabus")
VECTOR_BASE = os.path.join(BASE_DIR, "chatbot/vectorstores/syllabus")

embedder = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

def build_for_pdf(pdf_name):
    pdf_path = os.path.join(SYLLABUS_DIR, pdf_name)
    subject = pdf_name.replace(".pdf", "").lower()
    
    print(f"\n📄 Processing {subject} ...")

    loader = PyPDFLoader(pdf_path)
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
    chunks = splitter.split_documents(docs)

    # Try to detect and prefix unit headers in each chunk to improve retrieval precision.
    # Common patterns: "Unit II ...", "II Requirement Analysis...", "Unit 2", "second unit"
    def extract_unit_header(text: str):
        t = text or ""
        # Try explicit 'Unit X' (roman, digit, or word)
        m = re.search(r"(?i)\bunit\s*(?:[:.\-]?\s*)?(?P<hdr>(?:ii|iii|iv|v|vi|i|\d+|one|two|three|four|five|six)[^\n]*)", t)
        if m:
            hdr = m.group('hdr').strip()
            return f"Unit {hdr}" if not hdr.lower().startswith('unit') else hdr

        # Try roman numeral at line start, e.g., 'II Requirement Analysis'
        m2 = re.search(r"(?m)^\s*(?P<r>(?:I|II|III|IV|V|VI))\b[\.\-:\s]*(?P<title>[^\n]+)", t)
        if m2:
            r = m2.group('r').strip()
            title = m2.group('title').strip()
            return f"Unit {r} {title}"

        return None

    # Prefix chunk content when a unit header is detected in the chunk text
    for c in chunks:
        header = extract_unit_header(c.page_content)
        if header:
            # Avoid double-prefixing
            if not c.page_content.lower().startswith(header.lower()):
                c.page_content = header + "\n\n" + c.page_content

    vector_dir = os.path.join(VECTOR_BASE, subject)
    os.makedirs(vector_dir, exist_ok=True)

    vectorstore = FAISS.from_documents(chunks, embedder)
    vectorstore.save_local(vector_dir)

    print(f"✅ Vectorstore created: {vector_dir}")

if __name__ == "__main__":
    for file in os.listdir(SYLLABUS_DIR):
        if file.endswith(".pdf"):
            build_for_pdf(file)
