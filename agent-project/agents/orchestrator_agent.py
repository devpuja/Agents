from typing import Any
import logging

from agents.planner_agent import PlannerAgent
from agents.researcher_agent import ResearchAgent
from agents.writer_agent import WriterAgent
from agents.memory_agent import MemoryAgent
from agents.router_agent import RouterAgent
from agents.tool_agent import ToolAgent
from agents.memory_router_agent import MemoryRouterAgent

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
        self.memory_router_agent = MemoryRouterAgent()

    def get_research_result(self, user_input: str) -> ResearchResult:
        return self.researcher.research(user_input)

    def orchestrate(self, user_input: str) -> dict[str, str]:
        plan = self.planner.create_plan(user_input)
        logger.info("PLAN: %s", plan)
        print("PLAN:", plan)

        router_decision = self.router.route(user_input)
        logger.info("ROUTER DECISION: %s", router_decision)
        print("ROUTER DECISION:", router_decision)
        
        topic = self.memory_router_agent.extract_memory_topic(user_input)
        topic = topic.split("\n")[0].strip()
        print("TOPIC:", topic)
        
        #memory_context = self.memory.recent_context()
        memory_context = ""
        if self.memory_router_agent.should_recall(user_input):
            memory_context = self.memory.recall(topic)
        
        logger.info("MEMORY CONTEXT: %s", memory_context)
        print("MEMORY CONTEXT:", memory_context)

        # TOOL Flow
        if router_decision == "TOOL":
            tool_result = self.tool_agent.execute(user_input)
            tool_answer = "" if tool_result is None else str(tool_result)
            self.memory.save(user_input, tool_answer)
            return {
                "plan": "Tool Execution",
                "answer": tool_answer
            }

        # CHAT Flow & RESEARCH Flow #
        research_result: ResearchResult
        if router_decision == "CHAT":
            research_result = {"documents": [], "metadatas": []}
        else:
            research_result = self.get_research_result(user_input)

        logger.info("RESEARCH: %s", research_result)
        print("RESEARCH:", research_result)

        answer = self.writer.write_task(user_input, research_result, memory_context)

        self.memory.save(user_input, answer)

        logger.info("ANSWER: %s", answer)
        print("ANSWER:", answer)

        return {
            "plan": plan,
            "answer": answer
        }
        
print(OrchestratorAgent().orchestrate("What database do I prefer?"))