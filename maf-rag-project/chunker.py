def chunk_documents(documents: list[dict[str, str]], 
                    chunk_size: int = 200, 
                    chunk_overlap: int = 50) -> list[dict[str, str]]:

    chunks: list[dict[str, str]] = []

    for document in documents:
        content = document["content"]
        filename = document["filename"]

        start = 0
        chunk_number = 1

        while start < len(content):
            end = start + chunk_size
            chunk_text = content[start:end]
            chunks.append(
                {
                    "chunk_id": f"{filename}_chunk_{chunk_number}",
                    "filename": filename,
                    "content": chunk_text,
                }
            )

            chunk_number += 1

            if end >= len(content):
                break

            start = end - chunk_overlap

    return chunks