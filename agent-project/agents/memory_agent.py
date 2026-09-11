from services.sqlite_service import (get_history, save_chat, search_memory)

class MemoryAgent:
    def save(self, user: str, assistant: str) -> None:
        save_chat(user, assistant)

    def history(self) -> None:
        get_history()

    def recent_context(self, limit: int = 5) -> str:
        history_data = get_history()

        if not history_data:
            return ""

        conversations: list[str] = []

        for user_msg, assistant_msg in history_data[:limit]:
            conversations.append(f"User: {user_msg}")
            conversations.append(f"Assistant: {assistant_msg}")

        return "\n".join(conversations)
    
    def recall(self, keyword:str) -> str:
        memory = search_memory(keyword)

        if not memory:
            return ""

        result: list[str] = []

        for user, assistant in memory:
            result.append(f"User: {user}")
            result.append(f"Assistant: {assistant}")

        return "\n".join(result)    
        
        
        
        