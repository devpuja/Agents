import asyncio

from datetime import datetime
from agent_framework import Agent
from agent_framework_ollama import OllamaChatClient


def calculate(expression: str) -> str:
    try:
        result = eval(expression, {"__builtins__":{}}, {})
        return str(result)
    except:
        return "Unable to calculate the expression."


def get_current_time() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    
async def main():
    agent = Agent(
        client = OllamaChatClient(),
        name="CalculatorAssistant",
        instructions=(
            "You are a helpful assistant. "
            "Use the calculate tool whenever the user asks for an arithmetic calculation. "
            "Use the get_current_time tool whenever the user asks for the current date or time."
        ),
        tools=[calculate, get_current_time]
    )
    
    query = "What is 125 * 37?"
    result = await agent.run(query)
    print(result)
    
    query = "What is the current time?"
    result = await agent.run(query)
    print(result)
        
    query = "What is CAP Theorem?"
    result = await agent.run(query)
    print(result)
    
    
    # agent = Agent(
    #     client = OllamaChatClient(),
    #     name="HelpfulAssistant",
    #     instructions="You are a helpful assistant running locally via Ollama.",
    # )
    
    # query = "What is my favorite database?"
    # #query = "What is CAP Theorem?"
    # result = await agent.run(query)
    # print(result)
    

if __name__ == "__main__":
    asyncio.run(main())
    