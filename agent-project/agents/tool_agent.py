import logging
from typing import Callable
from agents.tool_router_agent import ToolRouterAgent
from tools.datetime_tool import current_datetime
from tools.calculator_tool import calculate_expression


logger = logging.getLogger(__name__)


class ToolAgent:
    def __init__(self):
        self.tools: dict[str, Callable[..., str]] = {
            "current_datetime": current_datetime,
            "calculate_expression": calculate_expression,
        }
        
        self.tool_router = ToolRouterAgent()

    def execute(self, user_input: str):
        text = user_input.lower()
        tool_name = self.tool_router.select_tool(text)
        
        logger.info(f"[ToolAgent] Selected Tool: {tool_name}")


        if tool_name == "DATETIME":
            return self.tools["current_datetime"]()

        if tool_name == "CALCULATOR":
            expression = text.replace("calculate", "").strip()
            return str(self.tools["calculate_expression"](expression))

        return "ToolAgent: No relevant tool found for the input."


print(ToolAgent().execute("What is the current date and time?"))
print(ToolAgent().execute("Calculate 250 + 107"))
print(ToolAgent().execute("Calculate 99 * 9"))
print(ToolAgent().execute("Calculate 2000 * 13 %"))