import asyncio

from pydantic import BaseModel
from agent_framework import Agent
from agent_framework_ollama import OllamaChatClient


# ============================================================
# 1. STRUCTURED OUTPUT MODEL
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
# 2. OLLAMA CLIENT
# ============================================================

client = OllamaChatClient(model="llama3.1:latest")

# ============================================================
# 3. POSTGRESQL SPECIALIST
# ============================================================

postgres_agent = Agent(
    client=client,
    name="PostgreSQLAgent",
    instructions=(
        "You are a PostgreSQL specialist.\n\n"
        "Answer questions about PostgreSQL accurately.\n"
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


# ============================================================
# 4. TOOL / ADAPTER
# ============================================================

# async def ask_postgresql_specialist(task: str) -> PostgreSQLInfo:
#     response = await postgres_agent.run(
#         task,
#         options={
#             "response_format": PostgreSQLInfo
#         }
#     )

#     print("\n========== SPECIALIST RESPONSE ==========")
#     print(response)

#     print("\n========== RESPONSE TYPE ==========")
#     print(type(response))

#     structured_value = getattr(response, "value", None)

#     print("\n========== STRUCTURED VALUE ==========")
#     print(structured_value)

#     print("\n========== STRUCTURED VALUE TYPE ==========")
#     print(type(structured_value).__name__)

#     if structured_value is None:
#         raise RuntimeError(
#             "PostgreSQLAgent did not return a structured value."
#         )

#     return structured_value

async def ask_postgresql_with_retry(task: str, max_retries: int = 3):

    for attempt in range(1, max_retries + 1):

        try:
            print(f"\nAttempt {attempt}...")

            result = await ask_postgresql_specialist(task)

            print("PostgreSQL specialist succeeded.")
            return result

        except RuntimeError as e:

            print(f"Attempt {attempt} failed: {e}")

            if attempt == max_retries:
                print("Maximum retry attempts reached.")
                raise

            print("Retrying...")
            
            
async def ask_postgresql_specialist(task: str) -> PostgreSQLInfo:
    raise RuntimeError("Simulated PostgreSQL specialist failure")
    
    
async def ask_mysql_specialist(task: str) -> MySQLInfo:
    response = await mysql_agent.run(
        task,
        options={
            "response_format": MySQLInfo
        }
    )

    print("\n========== SPECIALIST RESPONSE ==========")
    print(response)

    print("\n========== RESPONSE TYPE ==========")
    print(type(response))

    structured_value = getattr(response, "value", None)

    print("\n========== STRUCTURED VALUE ==========")
    print(structured_value)

    print("\n========== STRUCTURED VALUE TYPE ==========")
    print(type(structured_value).__name__)

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

    print("\n========== SPECIALIST RESPONSE ==========")
    print(response)

    print("\n========== RESPONSE TYPE ==========")
    print(type(response))

    structured_value = getattr(response, "value", None)

    print("\n========== STRUCTURED VALUE ==========")
    print(structured_value)

    print("\n========== STRUCTURED VALUE TYPE ==========")
    print(type(structured_value).__name__)

    if structured_value is None:
        raise RuntimeError(
            "ArchitectureAgent did not return a structured value."
        )

    return structured_value


# ============================================================
# 5. MAIN AGENT
# ============================================================

# async def main():
#     main_agent = Agent(
#         client=client,
#         name="DatabaseAgent",
#         instructions=(
#             "You are the main database assistant.\n\n"

#             "You have access to three specialist tools:\n"
            
#             "1. ask_postgresql_specialist - use this for "
#             "PostgreSQL-specific questions.\n"
            
#             "2. ask_mysql_specialist - use this for "
#             "MySQL-specific questions.\n"
            
#             "3. ask_architecture_specialist - use this for "
#             "database architecture, scalability, reliability, "
#             "security, performance, and architectural trade-off questions.\n\n"

#             "When a question involves multiple areas, "
#             "call all relevant specialist tools.\n\n"

#             "After receiving the specialist responses, "
#             "synthesize their information into a clear answer for the user."
#         ),
#         tools=[
#             ask_postgresql_specialist,
#             ask_mysql_specialist,
#             ask_architecture_specialist
#         ]
#     )


async def main():

    print("\n========== RETRY TEST ==========")

    try:
        result = await ask_postgresql_with_retry(
            "What are the main strengths of PostgreSQL?"
        )

        print("\n========== FINAL RESULT ==========")
        print(result)

    except Exception as e:
        print("\n========== FINAL FAILURE ==========")
        print("Error:", e)


    # ========================================================
    # 6. RUN MAIN AGENT
    # ========================================================

    # result = await main_agent.run("What are the main strengths of PostgreSQL?")
    # result = await main_agent.run("What are the main strengths of MySQL?")
    # result = await main_agent.run(
    #     "Compare PostgreSQL and MySQL for an enterprise application. "
    #     "What architectural factors should I consider?",
    #     options={
    #         "response_format": DatabaseComparison
    #         }
    # )


    # ========================================================
    # 7. FINAL MAIN AGENT RESPONSE
    # ========================================================

    # print("\n\n========== FINAL ANSWER ==========")
    # print(result)
    # comparison = result.value

    # if comparison is not None:
    #     print("\nPostgreSQL object:")
    #     print(comparison.postgresql)
    #     print(type(comparison.postgresql))

    #     print("\nMySQL object:")
    #     print(comparison.mysql)
    #     print(type(comparison.mysql))

    #     print("\nArchitecture object:")
    #     print(comparison.architecture)
    #     print(type(comparison.architecture))

    #     print("\nSummary:")
    #     print(comparison.summary)


# ============================================================
# 8. APPLICATION ENTRY POINT
# ============================================================

if __name__ == "__main__":
    asyncio.run(main())