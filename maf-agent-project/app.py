import asyncio

from datetime import datetime
from agent_framework import Agent, tool
from agent_framework_ollama import OllamaChatClient

from typing import Annotated
from pydantic import Field

from memory_provider import SimpleMemoryProvider
from memory_service import initialize_database, save_memory, search_memories

initialize_database()


@tool
def calculate(expression: Annotated[str, Field(description="The arithmetic expression to calculate, such as '125 * 37'.")]) -> str:
    """
    Evaluate a basic arithmetic expression.

    Use this tool for addition, subtraction, multiplication,
    division, percentages, and other basic arithmetic calculations.
    """
    try:
        result = eval(expression, {"__builtins__":{}}, {})
        return str(result)
    except:
        return "Unable to calculate the expression."

@tool
def get_current_time() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
@tool
def remember(key: str, value: str) -> str:
    """Save a user preference or personal fact to persistent memory.

    Use this tool when the user explicitly tells you a personal preference
    or fact that should be remembered for future conversations.
    Do not use it for general knowledge, temporary information, or questions.
    """
    save_memory(key, value)
    
    return f"Remembered: {key} = {value}"

    
async def main():
    agent = Agent(
        client = OllamaChatClient(model="llama3.1:latest"),
        name="CalculatorAssistant",
        instructions=(
            "You are a helpful assistant. "
            "Answer general knowledge questions directly using your own knowledge. "
            "Use the calculate tool whenever the user asks for an arithmetic calculation. "
            "Use the get_current_time tool whenever the user asks for the current date or time. "
            "Do not use a tool when it is not needed."
            "Use the remember tool when the user explicitly asks you to remember a personal preference or fact."
            "Do not save general knowledge or temporary information as memory."
        ),
        tools=[calculate, get_current_time, remember],
        context_providers = [SimpleMemoryProvider("simple-memory")]
    )
    
    session1 = agent.create_session()
    #session2 = agent.create_session()
    #session3 = agent.create_session()
    
    # ========================================================================= #
    print(search_memories("personal"))
    
    result = await agent.run("What database do I prefer for personal projects?", session=session1)
    print(result)
    
    # result = await agent.run("What is my favorite database?", session=session2)
    # print(result)
    
    # result = await agent.run("What database do I prefer for my personal projects?", session=session3)
    # print(result)
    
    # ========================================================================= #
    
    # result = await agent.run("What is 125 * 37?", session=session)
    # print("Turn 1: ", result)
    
    # result = await agent.run("What was the result?", session=session)
    # print("Turn 2: ", result)
    
    # ========================================================================= #
    # query = "What is 125 * 37?"
    # result = await agent.run(query)
    # print(result)
    
    # query = "Calculate 15% of 2000."
    # result = await agent.run(query)
    # print(result)
    
    # query = "What is the current time?"
    # result = await agent.run(query)
    # print(result)
        
    # query = "What is CAP Theorem?"
    # result = await agent.run(query)
    # print(result)
    

if __name__ == "__main__":
    asyncio.run(main())
    