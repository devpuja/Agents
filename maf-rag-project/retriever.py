import asyncio
from typing import cast

from embedding_service import create_embedding
from vector_store import create_vector_store
from rag_observability import trace_rag


async def retrieve(query: str, top_k: int = 2) -> list[dict[str, str | float]]:
    with trace_rag("RAG Retrieval"):
        collection = create_vector_store()
            
        query_embedding = create_embedding(query)
            
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )
    
        retrieved_documents: list[dict[str, str | float]] = []
    
        document_batches = results.get("documents")
        
        documents = document_batches[0] if document_batches else []
        
        metadata_batches = results.get("metadatas") or []
        
        metadatas = cast(
            list[dict[str, str]],
            metadata_batches[0] if metadata_batches and metadata_batches[0] else [{} for _ in documents]
        )
        
        ids = results["ids"][0]
        distance_batches = results.get("distances")
        distances = distance_batches[0] if distance_batches else []
    
        for document, metadata, chunk_id, distance in zip(documents, metadatas, ids, distances):
            retrieved_documents.append(
                {
                    "chunk_id": chunk_id,
                    "filename": metadata.get("filename", ""),
                    "content": document,
                    "distance": distance
                }
            )
    
        return retrieved_documents


async def main():
    query = "Which database supports ACID transactions?"
    results = await retrieve(query, top_k=2)

    print("\n========== RETRIEVAL ==========")

    print("Query:")
    print(query)

    print("\nRetrieved chunks:", len(results))

    for result in results:
        print("\n========================================")
        print("Chunk ID:", result["chunk_id"])
        print("Source:", result["filename"])
        print("Distance:", result["distance"])

        print("\nContent:")
        print(result["content"])


if __name__ == "__main__":
    asyncio.run(main())