import chromadb
from typing import List

client = chromadb.PersistentClient(path="data/chroma_db")
collection = client.get_or_create_collection("knowledge")

def add_document(doc: str):
    collection.add(
        documents=[doc],
        ids=[str(hash(doc))]
    )
    
def search(query: str) -> List[str]:
    results = collection.query(
        query_texts=[query],
        n_results=3
    )
    
    documents = results.get("documents")
    
    if not documents:
        return []
    return documents[0]

