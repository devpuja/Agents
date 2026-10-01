import chromadb

from document_loader import load_documents
from chunker import chunk_documents
from embedding_service import create_embedding


COLLECTION_NAME = "rag_documents"


def create_vector_store():
    client = chromadb.PersistentClient(path="./chroma_db")
    collection = client.get_or_create_collection(name=COLLECTION_NAME)
    return collection


def index_documents(collection: chromadb.Collection, chunks: list[dict[str, str]]):
    for chunk in chunks:
        embedding = create_embedding(chunk["content"])

        collection.upsert(
            ids=[chunk["chunk_id"]],
            embeddings=[embedding],
            documents=[chunk["content"]],
            metadatas=[
                {
                    "filename": chunk["filename"]
                }
            ]
        )


def main():
    documents = load_documents()
    chunks = chunk_documents(
        documents,
        chunk_size=200,
        chunk_overlap=50
    )

    collection = create_vector_store()

    index_documents(collection, chunks)

    print("\n========== VECTOR STORE ==========")

    print("Collection:", collection.name)

    print("Records:", collection.count())


if __name__ == "__main__":
    main()