from services.ollama_service import ask_llm
from services.sqlite_service import save_chat

class ChatAgent:
    def run(self, message: str) -> str:
        answer = ask_llm(message)
        save_chat(message, answer)
        
        return answer