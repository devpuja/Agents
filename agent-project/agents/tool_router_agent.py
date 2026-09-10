from services.ollama_service import ask_llm

class ToolRouterAgent:
    def select_tool(self, user_input: str) -> str:
        prompt = f"""
            You are a tool selection agent.

            Available tools:

            1. DATETIME
            - current date
            - current time

            2. CALCULATOR
            - mathematical calculations
            - arithmetic expressions

            Return ONLY one value:

            DATETIME
            CALCULATOR
            NONE

            User Request:
            {user_input}

            Answer:
            """
            
        response = ask_llm(prompt).strip().upper()
                
        match response:
            case "DATETIME":
                return "DATETIME"
            case "CALCULATOR":
                return "CALCULATOR"
            case _:
                return "NONE"