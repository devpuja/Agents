import chromadb
from typing import Any, Dict, List

COLLECTION_NAME = "knowledge"
client = chromadb.PersistentClient(path="data/chroma_db")
collection = client.get_or_create_collection(COLLECTION_NAME)


def add_document_chunk(text: str, doc_name: str, chunk_id: int):
    collection.add(
        documents=[text],
        ids=[f"{doc_name}_chunk_{chunk_id}"],
        metadatas=[{"source": doc_name, "chunk_id": chunk_id}]
    )
    
def search(query: str) -> Dict[str, List[Any]]:
    results = collection.query(
        query_texts=[query],
        n_results=3
    )

    documents = results.get("documents") or []
    metadatas = results.get("metadatas") or []

    if not documents:
        return {"documents": [], "metadatas": []}
    
    return {
        "documents": documents[0],
        "metadatas": metadatas[0] if metadatas else []
        }


def reset_collection():
    global collection
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass

    collection = client.get_or_create_collection(COLLECTION_NAME)