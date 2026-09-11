import logging

from models.tool_definition import ToolDefinition
from agents.tool_router_agent import ToolRouterAgent
from tools.datetime_tool import current_datetime
from tools.calculator_tool import calculate_expression
from tools.random_number_tool import random_number


logger = logging.getLogger(__name__)


class ToolAgent:
    def __init__(self):
        self.tools: dict[str, ToolDefinition] = {
            "DATETIME": ToolDefinition(
                name="DATETIME",
                description="Get current date and time",
                function=current_datetime,
            ),
            "CALCULATOR": ToolDefinition(
                name="CALCULATOR",
                description="Perform mathematical calculations",
                function=calculate_expression,
            ),
            "RANDOM": ToolDefinition(
                name="RANDOM",
                description="Generate random numbers",
                function=random_number
            )
        }
        
        self.tool_router = ToolRouterAgent()


    def get_available_tools(self):
        return "\n".join([f"{tool.name} {tool.description}" for tool in self.tools.values()])

    #def build_tool_context(self, user_input: str) -> dict:
        

    def execute(self, user_input: str):
        text = user_input.lower()
        tool_name = self.tool_router.select_tool(text)

        logger.info(f"[ToolAgent] Selected Tool: {tool_name}")
        print(f"[ToolAgent] Selected Tool: {tool_name}")

        tool = self.tools.get(tool_name)
        
        if not tool:
            return "ToolAgent: No relevant tool found for the input."
        
        if tool_name == "DATETIME":
            return tool.function()

        if tool_name == "CALCULATOR":
            expression = (text.replace("calculate", "").strip())
            return str(tool.function(expression))
        
        if tool_name == "RANDOM":
            return tool.function()
        

# print(ToolAgent().execute("Generate RANDOM numbers.")) 
# print(ToolAgent().execute("What is the current date and time?"))
# print(ToolAgent().execute("Calculate 250 + 107"))
# print(ToolAgent().execute("Calculate 99 * 9"))
# print(ToolAgent().execute("Calculate (2000 * 13) / 100"))
# print(ToolAgent().execute("Calculate 2000 % 5"))