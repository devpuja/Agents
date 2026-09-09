from services.chroma_service import collection

print("Collection Count:", collection.count())

data = collection.get()

print("IDs:")
print(data["ids"])

print("\nDocuments:")
print(data["documents"])

print("\nMetadata:")
print(data["metadatas"])