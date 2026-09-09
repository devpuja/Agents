
from typing import Any, Dict, List
from services.chroma_service import search

class ResearchAgent:
    def research(self, query: str) -> Dict[str, List[Any]]:
        results = search(query)
        return results