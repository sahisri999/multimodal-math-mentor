from backend.rag.retriever import retrieve_context

query = "What is Bayes theorem?"

results = retrieve_context(query)

print("\nRetrieved Context:\n")

for r in results:
    print(r)
    print("\n---\n")