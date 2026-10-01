import requests


OLLAMA_URL = "http://127.0.0.1:11434/api/embeddings"
EMBEDDING_MODEL = "nomic-embed-text:latest"


def create_embedding(text: str) -> list[float]:
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": EMBEDDING_MODEL,
            "prompt": text
        },
        timeout=30
    )

    response.raise_for_status()
    data = response.json()
    
    return data["embedding"]


if __name__ == "__main__":

    text = "PostgreSQL supports ACID transactions."

    embedding = create_embedding(text)

    print("\n========== EMBEDDING TEST ==========")
    print("Text:")
    print(text)

    print("\nEmbedding dimension:")
    print(len(embedding))

    print("\nFirst 10 values:")
    print(embedding[:10])