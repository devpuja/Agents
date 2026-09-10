from typing import Any
import logging

from agents.planner_agent import PlannerAgent
from agents.researcher_agent import ResearchAgent
from agents.writer_agent import WriterAgent
from agents.memory_agent import MemoryAgent
from agents.router_agent import RouterAgent
from agents.tool_agent import ToolAgent

logger = logging.getLogger(__name__)

ResearchResult = dict[str, list[Any]]

class OrchestratorAgent:
    def __init__(self):
        self.planner = PlannerAgent()
        self.researcher = ResearchAgent()
        self.writer = WriterAgent()
        self.memory = MemoryAgent()
        self.router = RouterAgent()
        self.tool_agent = ToolAgent()

    def get_research_result(self, user_input: str) -> ResearchResult:
        return self.researcher.research(user_input)

    def orchestrate(self, user_input: str) -> dict[str, str]:
        plan = self.planner.create_plan(user_input)
        logger.info("PLAN: %s", plan)

        router_decision = self.router.route(user_input)
        logger.info("ROUTER DECISION: %s", router_decision)

        # TOOL Flow
        if router_decision == "TOOL":
            tool_result = self.tool_agent.execute(user_input)
            self.memory.save(user_input, tool_result)
            return {
                "plan": "Tool Execution",
                "answer": tool_result
            }

        # CHAT Flow & RESEARCH Flow #
        research_result: ResearchResult
        if router_decision == "CHAT":
            research_result = {"documents": [], "metadatas": []}
        else:
            research_result = self.get_research_result(user_input)

        logger.info("RESEARCH: %s", research_result)

        answer = self.writer.write_task(user_input, research_result)

        self.memory.save(user_input, answer)

        logger.info("ANSWER: %s", answer)

        return {
            "plan": plan,
            "answer": answer
        }