from rag_engine import answer_question

if __name__ == "__main__":
    while True:
        q = input("Enter your question (or 'exit' to quit): ")
        if q.lower() == "exit":
            break

        answer = answer_question(q)
        print("\n📝 Answer:\n", answer)
        print("-" * 50)
