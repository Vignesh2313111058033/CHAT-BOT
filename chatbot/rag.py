import os

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

def load_documents():
    docs = {}
    for file in os.listdir(DATA_DIR):
        if file.endswith(".txt"):
            path = os.path.join(DATA_DIR, file)
            with open(path, "r", encoding="utf-8") as f:
                docs[file.replace(".txt", "")] = f.read()
    return docs

def search_context(query):
    docs = load_documents()
    best_match = ""

    for title, content in docs.items():
        if title.lower() in query.lower():
            best_match += f"\n\n[{title.upper()}]\n{content}"

    return best_match
