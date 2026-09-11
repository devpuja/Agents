from typing import Any, Dict, List
from services.ollama_service import ask_llm

class WriterAgent:
    def write_task(self, task: str, research_result: Dict[str, List[Any]], memory_context: str) -> str:
        documents = research_result.get("documents", [])
        
        metadatas = research_result.get("metadatas", [])
        
        context = "\n".join(documents) if documents else "No relevant context found."
        
        sources = "\n".join([f"Source: {metadata.get('source', 'Unknown')}, Chunk ID: {metadata.get('chunk_id', 'N/A')}" for metadata in metadatas]) if metadatas else "No sources available."
        
        prompt = f""" You are a technical assistant.
        Task: {task}
        
        Conversation Memory: {memory_context}
        
        Retrieved Context: {context}
        
        Sources: {sources}
        
        Rules:
        1. Use retrieved context if relevant.
        2. Ignore unrelated information.
        3. If context is insufficient, use general knowledge.
        4. Keep the response structured.
        5. Do not invent sources.

        Answer:
        """
        
        answer = ask_llm(prompt)
        
        return f"""{answer} \n\nSources:\n{sources}"""