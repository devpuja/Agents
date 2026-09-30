import asyncio
import random

from pydantic import BaseModel
from agent_framework import Agent
from agent_framework_ollama import OllamaChatClient


# ============================================================
# STRUCTURED OUTPUT MODELS
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


# ============================================================
# ERROR TYPES
# ============================================================

class RetryableError(Exception):
    pass


class NonRetryableError(Exception):
    pass


class SpecialistTimeoutError(RetryableError):
    pass


# ============================================================
# OLLAMA CLIENT
# ============================================================

client = OllamaChatClient(model="llama3.1:latest")


# ============================================================
# SPECIALIST AGENTS
# ============================================================

postgres_agent = Agent(
    client=client,
    name="PostgreSQLAgent",
    instructions=(
        "You are a PostgreSQL specialist. "
        "Answer questions about PostgreSQL accurately. "
        "Focus on PostgreSQL strengths, features, and use cases."
    )
)


mysql_agent = Agent(
    client=client,
    name="MySQLAgent",
    instructions=(
        "You are a MySQL specialist. "
        "Answer questions specifically about MySQL. "
        "Provide accurate and concise technical information."
    )
)


architecture_agent = Agent(
    client=client,
    name="ArchitectureAgent",
    instructions=(
        "You are a software architecture specialist. "
        "Focus on scalability, reliability, performance, "
        "security, maintainability, and architectural trade-offs."
    )
)


# ============================================================
# SPECIALIST CALLS
# ============================================================

async def ask_postgresql_specialist(task: str) -> PostgreSQLInfo:
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


async def ask_mysql_specialist(task: str) -> MySQLInfo:
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


async def ask_architecture_specialist(task: str) -> ArchitectureInfo:
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
# TIMEOUT
# ============================================================

async def call_postgresql_with_timeout(
    task: str,
    timeout_seconds: int = 30
) -> PostgreSQLInfo:

    print(
        f"\n========== TIMEOUT CONFIG ==========\n"
        f"Timeout configured: {timeout_seconds} seconds"
    )

    try:
        async with asyncio.timeout(timeout_seconds):

            result = await ask_postgresql_specialist(task)

            print("\n========== TIMEOUT WRAPPER RESULT ==========")
            print(result)
            print(type(result))

            return result

    except TimeoutError:
        raise SpecialistTimeoutError(
            f"PostgreSQL specialist timed out after "
            f"{timeout_seconds} seconds."
        )


# ============================================================
# RETRY WITH EXPONENTIAL BACKOFF + JITTER
# ============================================================

async def ask_postgresql_with_retry(task: str, max_retries: int = 3) -> PostgreSQLInfo:
    for attempt in range(1, max_retries + 1):
        try:
            print(f"\nAttempt {attempt}...")

            result = await call_postgresql_with_timeout(task)
            print("PostgreSQL specialist succeeded.")
            return result
        
        except RetryableError as e:
            print(f"Retryable error on attempt {attempt}: {e}")
            if attempt == max_retries:
                print("Maximum retry attempts reached.")
                raise

            base_delay = 2 ** (attempt - 1)
            jitter = random.uniform(0, 0.5)
            delay = base_delay + jitter

            print(f"Waiting {delay:.6f} seconds before retry...")

            await asyncio.sleep(delay)
            print("Retrying...")

        except NonRetryableError as e:
            print(f"Non-retryable error: {e}")
            print("Failing immediately. No retry.")
            raise


# ============================================================
# MAIN
# ============================================================

async def main():

    print("========== DIRECT SPECIALIST TEST ==========")

    result = await ask_postgresql_specialist("What are the main strengths of PostgreSQL?")

    print("\n========== RESULT ==========")
    print(result)

    print("\n========== TYPE ==========")
    print(type(result))

    print("\n========== NAME ==========")
    print(result.name)

    print("\n========== STRENGTHS ==========")
    for strength in result.strengths:
        print("-", strength)

    print("\n========== USE CASES ==========")
    for use_case in result.use_cases:
        print("-", use_case)


# ============================================================
# APPLICATION ENTRY POINT
# ============================================================

if __name__ == "__main__":
    asyncio.run(main())