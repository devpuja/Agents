from services.ollama_service import ask_llm

class MemoryRouterAgent:
    
    def should_recall(self, question: str) -> bool:
        prompt = f"""
            Determine whether this question
            requires recalling past conversations.

            Return only:

            YES
            or
            NO

            Question:
            {question}

            Answer:
            """
            
        result = ask_llm(prompt)
        return "YES" in result.upper()
    
    def extract_memory_topic(self, question: str) -> str:
        prompt = f"""
            Extract ONLY the memory topic.

            Examples:

            Question: What is my name?
            Answer: name

            Question: What database do I prefer?
            Answer: database

            Question: Where do I work?
            Answer: work

            Question:
            {question}

            Answer:
            """
        
        result = ask_llm(prompt)
        return result.upper()