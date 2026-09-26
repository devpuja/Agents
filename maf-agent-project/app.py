import asyncio

from datetime import datetime
from agent_framework import Agent, tool
from agent_framework_ollama import OllamaChatClient

from typing import Annotated
from pydantic import Field

from memory_provider import SimpleMemoryProvider
from memory_service import initialize_database, save_memory, delete_memory, get_all_memories

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
    """Save or update a user's personal preference or fact in persistent memory."""

    if not key or not key.strip():
        return "Memory was not saved because the key is empty."

    if not value or value.strip().lower() in {
        "none",
        "null",
        "unknown",
        "n/a",
    }:
        return "Memory was not saved because the value is invalid."

    normalized_key = key.strip().lower()

    # Normalize different LLM-generated variations
    # of the same database preference.
    database_keywords = {
        "database",
        "db",
        "favorite database",
        "database preference",
        "preferred database",
    }

    if (
        any(keyword in normalized_key for keyword in database_keywords)
        and (
            "personal" in normalized_key
            or "favorite" in normalized_key
            or "preference" in normalized_key
            or "preferred" in normalized_key
        )
    ):
        normalized_key = "preferred_database_for_personal_projects"

    print(
        f"REMEMBER TOOL CALLED: "
        f"key={normalized_key}, value={value}"
    )

    save_memory(normalized_key, value)

    return f"Remembered: {normalized_key} = {value}"

    
async def main():
    agent = Agent(
        client = OllamaChatClient(model="llama3.1:latest"),
        name="CalculatorAssistant",
        instructions=(
            "You are a helpful assistant. "
            "Answer general knowledge questions directly using your own knowledge. "

            "Use the calculate tool whenever the user asks for an arithmetic calculation. "
            "Use the get_current_time tool whenever the user asks for the current date or time. "

            "Use the remember tool ONLY when the user explicitly provides "
            "a new personal fact, preference, or an updated preference that "
            "should be saved for future conversations. "

            "NEVER use the remember tool to answer a question about an "
            "existing memory or preference. "
            "For example, if the user asks 'What is my favorite database?', "
            "do not call remember. "

            "Do not use a tool when it is not needed."
        ),
        tools=[calculate, get_current_time, remember],
        context_providers = [SimpleMemoryProvider("simple-memory")]
    )
    
    session1 = agent.create_session()
    session2 = agent.create_session()
    session3 = agent.create_session()
    session4 = agent.create_session()
    
    # ========================================================================= #
    # delete_memory("cap theorem")
    # delete_memory("preferred_database_for_personal_projects")
        
    result = await agent.run("What is my favorite database?", session=session1)
    print("What is my favorite database? =>", result,"\n")
    
    # result = await agent.run("What database do I prefer?", session=session2)
    # print("What database do I prefer? =>", result, "\n")
    
    # result = await agent.run("What is CAP Theorem?", session=session3)
    # print("What is CAP Theorem? =>", result, "\n")
    
    # result = await agent.run("What database do I prefer for my personal projects?", session=session4)
    # print("What database do I prefer for my personal projects? =>" ,result, "\n")
    
    print(get_all_memories())
    # ========================================================================= #
    

if __name__ == "__main__":
    asyncio.run(main())
    