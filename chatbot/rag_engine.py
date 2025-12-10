# import os
# import numpy as np
# import pickle
# from sklearn.metrics.pairwise import cosine_similarity
# from groq import Groq
# from dotenv import load_dotenv
# from langchain_community.document_loaders import PyPDFLoader

# load_dotenv()
# client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# BASE_DIR = os.path.dirname(os.path.dirname(__file__))
# DATA_DIR = os.path.join(BASE_DIR, "chatbot","data")

# PDF_PATH = os.path.join(DATA_DIR, "rules.pdf")
# STORE_PATH = os.path.join(DATA_DIR, "embedding_store.pkl")



# def get_embedding(text):
#     resp = client.embeddings.create(
#         model="text-embedding-nomic-embed",
#         input=text
#     )
#     return np.array(resp.data[0].embedding)



# def create_rag_index():
#     print("📄 Extracting text from PDF...")

#     if not os.path.exists(PDF_PATH):
#         raise FileNotFoundError(f"PDF not found at: {PDF_PATH}")

#     loader = PyPDFLoader(PDF_PATH)
#     docs = loader.load()

#     # Convert PDF pages to paragraphs
#     paragraphs = []
#     for d in docs:
#         page_text = d.page_content.strip()
#         for p in page_text.split("\n"):
#             if len(p.strip()) > 20:
#                 paragraphs.append(p.strip())

#     print(f"📝 Total passages extracted: {len(paragraphs)}")

#     print("🧠 Creating embeddings...")
#     embeddings = [get_embedding(p) for p in paragraphs]

#     data = {"paragraphs": paragraphs, "embeddings": embeddings}

#     with open(STORE_PATH, "wb") as f:
#         pickle.dump(data, f)

#     print(f"✅ Embedding store saved at: {STORE_PATH}")
#     return True


# def answer_question(question):
#     if not os.path.exists(STORE_PATH):
#         return "Embedding store missing. Run index builder."

#     with open(STORE_PATH, "rb") as f:
#         data = pickle.load(f)

#     paragraphs = data["paragraphs"]
#     stored_embeddings = data["embeddings"]

#     q_embed = get_embedding(question)

#     sims = [cosine_similarity([q_embed], [emb])[0][0] for emb in stored_embeddings]

#     top_idx = np.argmax(sims)
#     best_passage = paragraphs[top_idx]

#     llm_resp = client.chat.completions.create(
#         model="llama-3.1-70b-versatile",
#         messages=[
#             {"role": "system", "content": "Answer ONLY based on the college rule passage."},
#             {"role": "user", "content": f"Passage:\n{best_passage}\n\nQuestion: {question}"}
#         ],
#     )

#     return llm_resp.choices[0].message.content
# import os
# from groq import Groq
# from dotenv import load_dotenv
# from langchain_community.vectorstores import FAISS
# from langchain_community.embeddings import HuggingFaceEmbeddings

# load_dotenv()

# client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# BASE_DIR = os.path.dirname(os.path.dirname(__file__))
# VECTORSTORE_PATH = os.path.join(BASE_DIR, r"chatbot\vectorstore")  # raw string to fix \d warning

# # Use the same embedding model as build_rag.py
# embedder = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")


# def load_vectorstore():
#     if not os.path.exists(VECTORSTORE_PATH):
#         print("❌ Vectorstore not found! Run build_rag.py first.")
#         return None

#     return FAISS.load_local(
#         VECTORSTORE_PATH,
#         embedder,
#         allow_dangerous_deserialization=True
#     )


# def answer_question(question, top_k=2):
#     vectorstore = load_vectorstore()
#     if vectorstore is None:
#         return "Embedding store missing. Run index builder."

#     # Retrieve similar passages
#     docs = vectorstore.similarity_search(question, k=top_k)
#     context = "\n\n".join([d.page_content for d in docs])

#     try:
#         # Ask Groq LLM for the final answer
#         resp = client.chat.completions.create(
#             model="llama-3.1-8b-instant",
#             messages=[
#                 {"role": "system", "content": "Answer strictly based on college rules given."},
#                 {"role": "user", "content": f"Rules:\n{context}\n\nQuestion: {question}"}
#             ],
#         )
#         return resp.choices[0].message.content
#     except Exception as e:
#         return f"❌ Error while calling Groq API: {str(e)}"
# import os
# from groq import Groq
# from dotenv import load_dotenv

# from langchain_community.vectorstores import FAISS
# from langchain_community.embeddings import HuggingFaceEmbeddings

# load_dotenv()

# client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# # ---------------- RULES VECTORSTORE ----------------
# RULES_VECTORSTORE = os.path.join(BASE_DIR, "chatbot/vectorstore")

# # ---------------- SYLLABUS VECTORSTORES ----------------
# SYLLABUS_BASE = os.path.join(BASE_DIR, "chatbot/vectorstores/syllabus")

# # Embedding model
# embedder = HuggingFaceEmbeddings(
#     model_name="sentence-transformers/all-MiniLM-L6-v2"
# )


# # ============================================================
# #  LOADER FUNCTIONS
# # ============================================================

# def load_rules_vectorstore():
#     """Load vectorstore for rules.pdf"""
#     if not os.path.exists(RULES_VECTORSTORE):
#         print("❌ Rules vectorstore missing!")
#         return None

#     return FAISS.load_local(
#         RULES_VECTORSTORE,
#         embedder,
#         allow_dangerous_deserialization=True
#     )


# def load_syllabus_vectorstore(subject):
#     """Load syllabus vectorstore for given subject"""
#     subject_path = os.path.join(SYLLABUS_BASE, subject.lower())

#     if not os.path.exists(subject_path):
#         return None

#     return FAISS.load_local(
#         subject_path,
#         embedder,
#         allow_dangerous_deserialization=True
#     )


# # ============================================================
# #  SUBJECT DETECTION
# # ============================================================

# def detect_subject(question):
#     """Detect subject name from question text"""

#     subjects = {
#         "ds": ["data structures", "ds"],
#         "os": ["operating system", "os"],
#         "cn": ["computer networks", "cn", "network"],
#         "python": ["python"],
#         "rdbms": ["dbms", "rdbms", "database"],
#         "maths": ["math", "maths"],
#         "english": ["english"],
#         "tamil": ["tamil"]
#     }

#     q = question.lower()

#     for key, keywords in subjects.items():
#         for word in keywords:
#             if word in q:
#                 return key

#     return None  # no match


# # ============================================================
# #  ANSWER FUNCTIONS
# # ============================================================

# def answer_rules(question, top_k=2):
#     """Answer questions ONLY from rules.pdf"""

#     vectorstore = load_rules_vectorstore()
#     if vectorstore is None:
#         return "Rules embedding store missing. Run build_rag.py first."

#     docs = vectorstore.similarity_search(question, k=top_k)
#     context = "\n\n".join([d.page_content for d in docs])

#     try:
#         resp = client.chat.completions.create(
#             model="llama3-8b-8192",
#             messages=[
#                 {"role": "system", "content": "Answer strictly based on college rules."},
#                 {"role": "user", "content": f"Rules:\n{context}\n\nQuestion: {question}"}
#             ],
#         )
#         return resp.choices[0].message.content

#     except Exception as e:
#         return f"❌ Groq API Error: {str(e)}"


# def answer_syllabus(question):
#     """Answer questions based on syllabus PDFs"""

#     subject = detect_subject(question)

#     if subject is None:
#         return "Please mention a subject (OS, DS, CN, Python, DBMS...)."

#     vectorstore = load_syllabus_vectorstore(subject)

#     if vectorstore is None:
#         return f"No syllabus data found for '{subject}'. Build syllabus index first."

#     docs = vectorstore.similarity_search(question, k=2)
#     context = "\n\n".join([d.page_content for d in docs])

#     try:
#         resp = client.chat.completions.create(
#             model="llama3-8b-8192",
#             messages=[
#                 {"role": "system", "content": "Answer only using the syllabus content."},
#                 {"role": "user", "content": f"Syllabus:\n{context}\n\nQuestion: {question}"}
#             ],
#         )
#         return resp.choices[0].message.content

#     except Exception as e:
#         return f"❌ Groq API Error: {str(e)}"


# # ============================================================
# #  UNIVERSAL ANSWER HANDLER
# # ============================================================

# def answer_question(question):
#     """Automatically choose between rules or syllabus"""

#     # If question contains words like rule, allowed, exam — assume rules
#     if any(x in question.lower() for x in ["rule", "allowed", "dress", "exam", "discipline", "attendance"]):
#         return answer_rules(question)

#     # Otherwise syllabus
#     return answer_syllabus(question)

import os
import re
from groq import Groq
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
RULES_STORE = os.path.join(BASE_DIR, "chatbot/vectorstore")
SYLLABUS_DIR = os.path.join(BASE_DIR, "chatbot/vectorstores/syllabus")

embedder = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")


# --------------------------
# LOAD RULES VECTORSTORE
# --------------------------
def load_rules_store():
    if not os.path.exists(RULES_STORE):
        print("❌ Rules vectorstore missing.")
        return None

    return FAISS.load_local(
        RULES_STORE,
        embedder,
        allow_dangerous_deserialization=True
    )


# --------------------------
# LOAD SYLLABUS VECTORSTORES
# --------------------------
def load_syllabus_stores():
    stores = {}
    
    if not os.path.exists(SYLLABUS_DIR):
        return stores

    for folder in os.listdir(SYLLABUS_DIR):
        path = os.path.join(SYLLABUS_DIR, folder)
        if os.path.isdir(path):
            store = FAISS.load_local(
                path,
                embedder,
                allow_dangerous_deserialization=True
            )
            # store under the folder name and also an alias without the trailing ' syllabus'
            stores[folder.lower()] = store
            if folder.lower().endswith(' syllabus'):
                alias = folder.lower().replace(' syllabus', '')
                stores[alias] = store

    return stores


def detect_subject(question):
    """Detect subject name from question text. Returns folder key if found."""
    q = question.lower()
    mapping = {
        'se': ['software engineering', 'se ', ' se\n', ' se. ', 'software eng'],
        'cn': ['computer networks', 'cn', 'network'],
        'os': ['operating system', 'os'],
        'rdbms': ['dbms', 'rdbms', 'database'],
        'ds': ['data structures', 'ds'],
        'python': ['python'],
        'maths': ['math', 'maths'],
        'english': ['english'],
        'tamil': ['tamil']
    }

    for key, keywords in mapping.items():
        for kk in keywords:
            if kk in q:
                return key
    return None


def detect_unit(question):
    """Detect unit number mentioned in question. Returns integer unit (1..6) or None."""
    q = question.lower()
    # patterns: 'unit 2', 'second unit', 'unit ii', 'unit II', 'unit two'
    m = re.search(r"unit\s*(?:[:.]\s*)?(\d)", q)
    if m:
        try:
            u = int(m.group(1))
            return u
        except Exception:
            pass

    # roman numerals II, III etc.
    m2 = re.search(r"unit\s*(ii|iii|iv|v|vi)\b", q)
    if m2:
        romans = {"ii":2, "iii":3, "iv":4, "v":5, "vi":6}
        return romans.get(m2.group(1), None)

    # words: 'second unit', 'third unit'
    words = {
        'first':1,'second':2,'third':3,'fourth':4,'fifth':5,'sixth':6,
        'one':1,'two':2,'three':3,'four':4,'five':5,'six':6
    }
    for w,k in words.items():
        if f"{w} unit" in q or f"unit {w}" in q:
            return k

    return None


# --------------------------
# LOAD OTHER VECTORSTORES
# --------------------------
VECTORSTORES_BASE = os.path.join(BASE_DIR, "chatbot/vectorstores")

def load_misc_stores():
    """Load vectorstores placed directly under chatbot/vectorstores
    (e.g., 'calendar', 'timetable'). Skip the 'syllabus' folder because
    it contains subfolders for subjects."""
    stores = {}
    if not os.path.exists(VECTORSTORES_BASE):
        return stores

    for folder in os.listdir(VECTORSTORES_BASE):
        if folder.lower() == 'syllabus':
            continue
        path = os.path.join(VECTORSTORES_BASE, folder)
        if os.path.isdir(path):
            try:
                store = FAISS.load_local(
                    path,
                    embedder,
                    allow_dangerous_deserialization=True
                )
                stores[folder.lower()] = store
            except Exception:
                # not a faiss store, skip
                continue

    return stores


# --------------------------
# MAIN RAG QA FUNCTION
# --------------------------
def answer_question(question, top_k=2):
    # Try rules first and syllabus stores
    rules_store = load_rules_store()
    syllabus_stores = load_syllabus_stores()
    misc_stores = load_misc_stores()

    results = []

    # If the user mentions a subject (e.g., 'software engineering'), restrict search
    subject = detect_subject(question)
    if subject:
        # Try rules as well (rules may contain related guidance)
        if rules_store:
            results.extend(rules_store.similarity_search(question, k=top_k))

        # If we have a store for the detected subject, search only it
        store = syllabus_stores.get(subject)
        if store:
            # If the user asked about a specific unit, boost passages that contain that unit
            unit = detect_unit(question)
            if unit:
                # fetch more candidates and filter by unit mention
                candidates = store.similarity_search(question, k=max(12, top_k*6))
                unit_matches = []
                # Build patterns for the requested unit: digit, word, roman
                roman_map = {1:'i',2:'ii',3:'iii',4:'iv',5:'v',6:'vi'}
                word_map = {1:'one',2:'two',3:'three',4:'four',5:'five',6:'six'}
                requested_roman = roman_map.get(unit)
                requested_word = word_map.get(unit)

                for d in candidates:
                    txt = (d.page_content or "")
                    low = txt.lower()
                    matched = False
                    # exact 'unit <digit>' or 'unit <word>'
                    if re.search(rf"unit\W*{unit}\b", low):
                        matched = True
                    if requested_word and re.search(rf"unit\W*{requested_word}\b", low):
                        matched = True
                    # 'Unit II' or start-line 'II Title' where roman equals requested
                    if requested_roman:
                        if re.search(rf"unit\W*{requested_roman}\b", low):
                            matched = True
                        # roman at line start: e.g., 'II Requirement Analysis'
                        if re.search(rf"(?m)^\s*{requested_roman}\b", low):
                            matched = True

                    if matched:
                        unit_matches.append(d)

                if unit_matches:
                    results.extend(unit_matches[:top_k])
                else:
                    # fallback to normal small-k search
                    docs = store.similarity_search(question, k=top_k)
                    results.extend(docs)
            else:
                docs = store.similarity_search(question, k=top_k)
                results.extend(docs)
        else:
            # Subject detected but no vectorstore built for it
            return f"No syllabus data found for subject '{subject}'. Build the syllabus index first."

    else:
        # No specific subject detected — search rules, all syllabus folders and misc stores
        if rules_store:
            rules_docs = rules_store.similarity_search(question, k=top_k)
            results.extend(rules_docs)

        # Search in ALL syllabus folders
        for name, store in syllabus_stores.items():
            docs = store.similarity_search(question, k=top_k)
            results.extend(docs)

        # Search in miscellaneous stores (calendar, timetable, etc.)
        for name, store in (misc_stores or {}).items():
            docs = store.similarity_search(question, k=top_k)
            results.extend(docs)

    if not results:
        return "No matching information found."

    # Build context
    context = "\n\n".join([d.page_content for d in results])

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "Answer clearly using the provided syllabus or rules only."},
                {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"}
            ],
        )
        return response.choices[0].message.content

    except Exception as e:
        return f"❌ Error while calling Groq API: {str(e)}"
