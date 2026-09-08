from services.sqlite_service import (get_history, save_chat)

class MemoryAgent:
    def save(self, user: str, assistant: str) -> None:
        save_chat(user, assistant)
    
    def history(self) -> None:
        get_history()