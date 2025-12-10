from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
import os

path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'vectorstores', 'syllabus', 'se syllabus')
emb = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')

try:
    store = FAISS.load_local(path, emb, allow_dangerous_deserialization=True)
except Exception as e:
    print('Failed to load FAISS store:', e)
    raise

q = 'second unit software engineering'
docs = store.similarity_search(q, k=6)

print(f"Found {len(docs)} docs for query: '{q}'\n")
for i, d in enumerate(docs):
    print('--- DOC', i, '---')
    print(d.page_content)
    print('\n')
