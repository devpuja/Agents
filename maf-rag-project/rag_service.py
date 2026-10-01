from retriever import retrieve


async def get_rag_context(query: str, top_k: int = 2) -> str:
    results = await retrieve(
        query,
        top_k=top_k
    )

    if not results:
        return "No relevant documents were found."

    context_parts : list[str] = []

    for result in results:
        context_parts.append(
            f"Source: {result['filename']}\n"
            f"Content:\n{result['content']}"
        )

    return "\n\n".join(context_parts)