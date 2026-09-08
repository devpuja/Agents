
from services.chroma_service import search

class ResearchAgent:
    def research(self, query: str) -> str:
        docs = search(query)

        if not docs:
            return f"No relevant results found for: {query}"
        
        return "\n".join(docs)