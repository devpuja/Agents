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

    def orchestrate(self, user_input: str) -> dict[str, str]:
        # Step 1: Create a plan based on user input
        plan = self.planner.create_plan(user_input)
        print("\n===== PLAN =====")
        print(plan)

        # Step 2: Research information based on the plan
        context = self.researcher.research(user_input)
        print("\n===== CONTEXT =====")
        print(context)

        # Step 3: Write content based on the research results
        answer = self.writer.write_task(user_input, context)

        # Step 4: Save the interaction to memory
        self.memory.save(user_input, answer)

        return { "plan": plan, "answer": answer }
    
    
    def orchestrate2(self, user_input: str) -> dict[str, str]:
        # Step 1: Create a plan based on user input
        plan = self.planner.create_plan(user_input)

        need_research = any(
            word in user_input.lower()
            for word in [
                "document",
                "pdf",
                "explain from",
                "search",
                "knowledge"
            ]
        )

        # Step 2: Research information based on the plan
        context = self.researcher.research(user_input) if need_research else ""

        # Step 3: Write content based on the research results
        answer = self.writer.write_task(user_input, context)

        # Step 4: Save the interaction to memory
        self.memory.save(user_input, answer)

        return { "plan": plan, "answer": answer }
    
    
    def should_research(self, user_input: str) -> bool:
        research_keywords = [
            "document",
            "pdf",
            "explain from",
            "search",
            "knowledge"
        ]
        
        return any(word in user_input.lower() for word in research_keywords)