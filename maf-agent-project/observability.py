import asyncio
import logging
# import time

from pydantic import BaseModel

from agent_framework import Agent
from agent_framework_ollama import OllamaChatClient
from tracing import trace_agent


# ============================================================
# 1. STRUCTURED OUTPUT MODELS
# ============================================================

class PostgreSQLInfo(BaseModel):
    name: str
    strengths: list[str]
    use_cases: list[str]


class MySQLInfo(BaseModel):
    name: str
    strengths: list[str]
    use_cases: list[str]


class ArchitectureInfo(BaseModel):
    factors: list[str]
    scalability: str
    reliability: str
    security: str
    performance: str
    trade_offs: list[str]


class DatabaseComparison(BaseModel):
    postgresql: PostgreSQLInfo
    mysql: MySQLInfo
    architecture: ArchitectureInfo
    summary: str
    
    
# ============================================================
# 2. LOGGING CONFIGURATION
# ============================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)


# ============================================================
# 3. OLLAMA CLIENT
# ============================================================

client = OllamaChatClient(
    model="llama3.1:latest"
)


# ============================================================
# 4. SPECIALIST AGENTS
# ============================================================

postgres_agent = Agent(
    client=client,
    name="PostgreSQLAgent",
    instructions=(
        "You are a PostgreSQL specialist. "
        "Provide accurate information about PostgreSQL "
        "strengths, features, and use cases."
    )
)


mysql_agent = Agent(
    client=client,
    name="MySQLAgent",
    instructions=(
        "You are a MySQL specialist. "
        "Provide accurate information about MySQL "
        "strengths, features, and use cases."
    )
)


architecture_agent = Agent(
    client=client,
    name="ArchitectureAgent",
    instructions=(
        "You are a software architecture specialist. "
        "Focus on scalability, reliability, security, "
        "performance, maintainability, and trade-offs."
    )
)


# ============================================================
# 5. POSTGRESQL SPECIALIST
# ============================================================

async def ask_postgresql_specialist(task: str) -> PostgreSQLInfo:

    async with trace_agent("PostgreSQLAgent"):

        response = await postgres_agent.run(
            task,
            options={
                "response_format": PostgreSQLInfo
            }
        )

        structured_value = getattr(response, "value", None)

        if structured_value is None:
            raise RuntimeError(
                "PostgreSQLAgent did not return a structured value."
            )

        return structured_value


# ============================================================
# 6. MYSQL SPECIALIST
# ============================================================

async def ask_mysql_specialist(task: str) -> MySQLInfo:

    async with trace_agent("MySQLAgent"):

        response = await mysql_agent.run(
            task,
            options={
                "response_format": MySQLInfo
            }
        )

        structured_value = getattr(response, "value", None)

        if structured_value is None:
            raise RuntimeError(
                "MySQLAgent did not return a structured value."
            )

        return structured_value


# ============================================================
# 7. ARCHITECTURE SPECIALIST
# ============================================================

async def ask_architecture_specialist(task: str) -> ArchitectureInfo:

    async with trace_agent("ArchitectureAgent"):

        response = await architecture_agent.run(
            task,
            options={
                "response_format": ArchitectureInfo
            }
        )

        structured_value = getattr(response, "value", None)

        if structured_value is None:
            raise RuntimeError(
                "ArchitectureAgent did not return a structured value."
            )

        return structured_value


# ============================================================
# 8. MAIN AGENT
# ============================================================

async def main():

    #start_time = time.perf_counter()

    logger.info("START | DatabaseAgent")

    main_agent = Agent(
        client=client,
        name="DatabaseAgent",
        instructions=(
            "You are the main database assistant.\n\n"

            "You have access to three specialist tools:\n"

            "1. ask_postgresql_specialist - PostgreSQL questions.\n"

            "2. ask_mysql_specialist - MySQL questions.\n"

            "3. ask_architecture_specialist - architecture, "
            "scalability, reliability, security, performance, "
            "and trade-offs.\n\n"

            "When a question involves multiple areas, "
            "call all relevant specialist tools.\n\n"

            "Synthesize the specialist responses into "
            "a clear answer."
        ),

        tools=[
            ask_postgresql_specialist,
            ask_mysql_specialist,
            ask_architecture_specialist
        ]
    )

    # async with trace_agent("PostgreSQLAgent"):
    #     result = await ask_postgresql_specialist(
    #         "What are the main strengths of PostgreSQL?"
    #     )

    async with trace_agent("DatabaseAgent"):
        result = await main_agent.run(
            "Compare PostgreSQL and MySQL for an enterprise application. "
            "What architectural factors should I consider?",
            options={
                "response_format": DatabaseComparison
            }
        )

    print("\n========== FINAL ANSWER ==========")
    print(result)
                
    # try:
    #     async with trace_agent("DatabaseAgent"):
    #         result = await main_agent.run(
    #             "Compare PostgreSQL and MySQL for an "
    #             "enterprise application. "
    #             "What architectural factors should I consider?",
    #             options={"response_format": DatabaseComparison}
    #         )

    #     duration = time.perf_counter() - start_time
    #     logger.info("SUCCESS | DatabaseAgent | %.2f seconds", duration)

    #     print("\n========== FINAL ANSWER ==========")
    #     print(result)

    # except Exception:

    #     duration = time.perf_counter() - start_time

    #     logger.exception(
    #         "FAILED | DatabaseAgent | %.2f seconds",
    #         duration
    #     )

    #     raise


# ============================================================
# 9. APPLICATION ENTRY POINT
# ============================================================

if __name__ == "__main__":
    asyncio.run(main())