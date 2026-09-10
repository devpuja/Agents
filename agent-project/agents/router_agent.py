from services.ollama_service import ask_llm

class RouterAgent:
    def route(self, question: str) -> str:
        prompt = f"""
            You are a routing assistant.

            Return ONLY one word:

            CHAT
            RESEARCH
            TOOL

            Use TOOL when:
            - current time
            - date
            - calculation
            - filesystem request

            Question:
            {question}

            Answer:
            """
        decision = ask_llm(prompt).strip().upper()
        
        match decision:
            case "RESEARCH":
                return "RESEARCH"
            case "TOOL":
                return "TOOL"
            case _:
                return "CHAT"  # Default to CHAT if the decision is unclear
    

# print(RouterAgent().route("What is Microsoft Agent Framework?"))
# print(RouterAgent().route("What is the capital of Bihar?"))
# print(RouterAgent().route("Write a motivational quote Show more lines."))
# print(RouterAgent().route("What is FastAPI?."))
# print(RouterAgent().route("Search my documents for Ollama."))
# print(RouterAgent().route("Write a poem about coding."))