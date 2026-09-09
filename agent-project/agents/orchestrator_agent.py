from typing import Any

from agents.planner_agent import PlannerAgent
from agents.researcher_agent import ResearchAgent
from agents.writer_agent import WriterAgent
from agents.memory_agent import MemoryAgent

class OrchestratorAgent:
    def __init__(self):
        self.planner = PlannerAgent()
        self.researcher = ResearchAgent()
        self.writer = WriterAgent()
        self.memory = MemoryAgent()

    def should_research(self, user_input: str) -> bool:
        research_keywords = ["document", "documents", "pdf", "knowledge", "search", "explain", 
                             "what is", "tell me", "framework", "ollama", "fastapi"]
        return any(word in user_input.lower() for word in research_keywords)


    def get_research_result(self, user_input: str) -> dict[str, list[Any]]:
        if not self.should_research(user_input):
            return {
                "documents": [],
                "metadatas": []
            }
        return self.researcher.research(user_input)


    def orchestrate(self, user_input: str) -> dict[str, str]:
        plan = self.planner.create_plan(user_input)

        print("\n===== PLAN =====")
        print(plan)

        research_result = self.get_research_result(user_input)
        print("\n===== RESEARCH RESULT =====")
        print(research_result)

        answer = self.writer.write_task(user_input, research_result)

        self.memory.save(user_input, answer)

        return {
            "plan": plan,
            "answer": answer
        }