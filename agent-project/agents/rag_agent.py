from services.chroma_service import search
from services.ollama_service import ask_llm

class RAGAgent:
    def run(self, query: str) -> str:
        docs = search(query=query)
        content = "\n".join(docs) if docs else "No relevant documents found."
        prompt = f"""Content: {content} Question: {query}"""
        answer = ask_llm(prompt)
        
        return answer