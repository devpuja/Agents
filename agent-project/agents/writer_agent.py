from services.ollama_service import ask_llm

class WriterAgent:
    def write_task(self, task:str, content:str) -> str:
        prompt = f""" You are a technical assistant.
        Task: {task}
        
        Retrieved Context: {content}
        
        Rules:
        1. Use only the context if it is relevant.
        2. Ignore unrelated information.
        3. If context is insufficient, use your general knowledge.
        4. Never mention irrelevant context.
        5. Create a clean and structured answer.

        Answer:
        """
        return ask_llm(prompt)