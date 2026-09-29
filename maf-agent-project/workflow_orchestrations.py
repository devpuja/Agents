import asyncio

from agent_framework import Agent
from agent_framework.orchestrations import ConcurrentBuilder
from agent_framework_ollama import OllamaChatClient


async def main():

    client = OllamaChatClient(
        model="llama3.1:latest"
    )

    postgres_agent = Agent(
        client=client,
        name="PostgreSQLAgent",
        instructions=(
            "You are a PostgreSQL specialist. "
            "Analyze the user's question from the PostgreSQL perspective. "
            "Provide concise technical facts, strengths, limitations, "
            "and relevant enterprise considerations."
        ),
    )

    mysql_agent = Agent(
        client=client,
        name="MySQLAgent",
        instructions=(
            "You are a MySQL specialist. "
            "Analyze the user's question from the MySQL perspective. "
            "Provide concise technical facts, strengths, limitations, "
            "and relevant enterprise considerations."
        ),
    )

    architecture_agent = Agent(
        client=client,
        name="ArchitectureAgent",
        instructions=(
            "You are a software architecture specialist. "
            "Analyze the user's question from a system architecture "
            "perspective. Focus on scalability, reliability, "
            "operational concerns, and architectural trade-offs."
        ),
    )
    
    workflow = ConcurrentBuilder(
        participants=[
            postgres_agent,
            mysql_agent,
            architecture_agent
        ]
    ).build()
    
    events = await workflow.run("Compare PostgreSQL and MySQL for an enterprise application.")
    
    outputs = events.get_outputs()
    
    print("\n========== FINAL AGGREGATED RESULTS ==========\n")
    
    for output in outputs:
        if hasattr(output, "messages"):
            for message in output.messages:
                name = message.author_name or "assistant"
                print("-" * 60)
                print(f"[{name}]")
                print(message.text)

        else:
            print(output)
        
        

if __name__ == "__main__":
    asyncio.run(main())