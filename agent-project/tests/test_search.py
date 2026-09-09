from services.chroma_service import search

results = search("What is Microsoft Agent Framework?")

print("Search Results:")
for idx, result in enumerate(results):
    print(f"Result {idx + 1}: {result}")
    print("\n")