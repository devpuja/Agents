from services.ollama_service import ask_llm

class PlannerAgent:
    def create_plan(self, tasks: str) -> str:
        prompt = f"""You are a planning assistance. Break the following request in to actionalbe steps.
        Requests: {tasks}
        
        Retuen only steps.
        """
        plan = ask_llm(prompt)
        return plan
        