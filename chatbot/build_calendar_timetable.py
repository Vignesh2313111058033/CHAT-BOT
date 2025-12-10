import os
from dotenv import load_dotenv

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

load_dotenv()

BASE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE, "data")
VECTOR_BASE = os.path.join(BASE, "vectorstores")

embedder = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

def build_store(pdf_path, out_dir):
    if not os.path.exists(pdf_path):
        print(f"❌ PDF not found: {pdf_path}")
        return False

    os.makedirs(out_dir, exist_ok=True)

    print(f"📄 Loading PDF: {pdf_path}")
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()

    print("🔍 Splitting text...")
    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
    chunks = splitter.split_documents(docs)

    print("📦 Building FAISS index...")
    vectorstore = FAISS.from_documents(chunks, embedder)

    vectorstore.save_local(out_dir)
    print(f"✅ Saved vectorstore at: {out_dir}")
    return True


def find_pdf_in_dir(folder):
    if not os.path.exists(folder):
        return None
    for f in os.listdir(folder):
        if f.lower().endswith('.pdf'):
            return os.path.join(folder, f)
    return None


def build_all():
    # calendar
    cal_folder = os.path.join(DATA_DIR, "calendar")
    cal_pdf = find_pdf_in_dir(cal_folder)
    if cal_pdf:
        build_store(cal_pdf, os.path.join(VECTOR_BASE, "calendar"))
    else:
        print("No calendar PDF found.")

    # timetable (note: folder sometimes named TimeTable)
    tt_folder = os.path.join(DATA_DIR, "timetable")
    if not os.path.exists(tt_folder):
        tt_folder = os.path.join(DATA_DIR, "TimeTable")
    tt_pdf = find_pdf_in_dir(tt_folder)
    if tt_pdf:
        build_store(tt_pdf, os.path.join(VECTOR_BASE, "timetable"))
    else:
        print("No timetable PDF found.")


if __name__ == '__main__':
    build_all()
