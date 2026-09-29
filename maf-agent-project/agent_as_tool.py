import asyncio

from agent_framework import Agent
from agent_framework_ollama import OllamaChatClient


async def main():

    client = OllamaChatClient(
        model="llama3.1:latest"
    )

    # ==========================================
    # Specialist Agents
    # ==========================================

    postgres_agent = Agent(
        client=client,
        name="PostgreSQLAgent",
        instructions=(
            "You are a PostgreSQL specialist. "
            "Answer questions specifically about PostgreSQL. "
            "Provide accurate and concise technical information."
        ),
    )

    mysql_agent = Agent(
        client=client,
        name="MySQLAgent",
        instructions=(
            "You are a MySQL specialist. "
            "Answer questions specifically about MySQL. "
            "Provide accurate and concise technical information."
        ),
    )

    architecture_agent = Agent(
        client=client,
        name="ArchitectureAgent",
        instructions=(
            "You are a software architecture specialist. "
            "Focus on scalability, reliability, performance, "
            "security, maintainability, and architectural "
            "trade-offs."
        ),
    )

    # ==========================================
    # Main Agent
    # ==========================================

    main_agent = Agent(
        client=client,
        name="MainAgent",
        instructions=(
            "You are the main technical assistant.\n\n"

            "You have access to three specialist agents:\n"
            "1. PostgreSQL specialist\n"
            "2. MySQL specialist\n"
            "3. Architecture specialist\n\n"

            "Delegate questions to the appropriate specialist "
            "when specialist expertise is useful.\n\n"

            "For PostgreSQL-specific questions, use the "
            "PostgreSQL specialist.\n"

            "For MySQL-specific questions, use the "
            "MySQL specialist.\n"

            "For architecture questions, use the "
            "Architecture specialist.\n\n"

            "For comparison questions involving multiple areas, "
            "you may consult multiple specialists.\n\n"

            "After receiving specialist responses, synthesize "
            "the information into a clear final answer."
        ),
    )

    # ==========================================
    # Agent-as-tools
    # ==========================================

    specialist_tools = [
        postgres_agent.as_tool(
            name="ask_postgresql_specialist",
            description=(
                "Ask the PostgreSQL specialist about PostgreSQL "
                "features, queries, indexing, transactions, "
                "performance, or other PostgreSQL-specific topics."
            ),
        ),

        mysql_agent.as_tool(
            name="ask_mysql_specialist",
            description=(
                "Ask the MySQL specialist about MySQL features, "
                "queries, indexing, transactions, performance, "
                "or other MySQL-specific topics."
            ),
        ),

        architecture_agent.as_tool(
            name="ask_architecture_specialist",
            description=(
                "Ask the architecture specialist about system "
                "architecture, scalability, reliability, security, "
                "performance, and architectural trade-offs."
            ),
        ),
    ]

    main_agent = Agent(
        client=client,
        name="MainAgent",
        instructions=(
            "You are the main technical assistant.\n\n"
            "You have access to PostgreSQL, MySQL, and architecture specialists. "
            "Delegate questions to the appropriate specialist when useful, "
            "then synthesize their responses into a clear final answer."
        ),
        tools=specialist_tools,
    )

    # ==========================================
    # Test
    # ==========================================

    result = await main_agent.run(
        "Compare PostgreSQL and MySQL for an enterprise application. "
        "Also explain the important architectural considerations."
    )

    print("\n========== FINAL ANSWER ==========\n")
    print(result)


if __name__ == "__main__":
    asyncio.run(main())