from rag_engine import create_rag_index

if __name__ == "__main__":
    print("📦 Creating embedding store...")
    ok = create_rag_index()
    if ok:
        print("✅ Embedding store created successfully!")
    else:
        print("❌ Failed to create embedding store.")
