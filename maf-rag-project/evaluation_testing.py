import asyncio

from agent_framework_ollama import OllamaChatClient

from rag_research_agent import RAGResearchAgent
from rag_error_handling import research_with_retry


QUESTION = "Which database supports ACID transactions?"


async def create_rag_agent() -> RAGResearchAgent:
    client = OllamaChatClient(model="llama3.1:latest")
    return RAGResearchAgent(client)


# ============================================================
# TEST 1 — HAPPY PATH
# ============================================================

async def test_happy_path():
    print("\n========== TEST 1: HAPPY PATH ==========")

    agent = await create_rag_agent()

    result = await research_with_retry(agent, QUESTION)

    if result.answer:
        print("PASS - RAG workflow completed.")
        return True

    print("FAIL - RAG returned an empty answer.")
    return False


# ============================================================
# TEST 2 — RETRIEVAL
# ============================================================

async def test_retrieval():
    print("\n========== TEST 2: RETRIEVAL ==========")

    agent = await create_rag_agent()

    result = await research_with_retry(agent, QUESTION)

    if result.retrieved_chunks:
        print("PASS - Retrieved chunks returned.")
        print(f"Chunks: {len(result.retrieved_chunks)}")
        return True

    print("FAIL - No retrieved chunks returned.")
    return False


# ============================================================
# TEST 3 — STRUCTURED OUTPUT
# ============================================================

async def test_structured_output():
    print("\n========== TEST 3: STRUCTURED OUTPUT ==========")

    agent = await create_rag_agent()

    result = await research_with_retry(agent, QUESTION)

    expected_fields = [
        "answer",
        "sources",
        "retrieved_chunks"
    ]

    missing_fields = [
        field
        for field in expected_fields
        if not hasattr(result, field)
    ]

    if not missing_fields:
        print("PASS - RAGResearchResult returned successfully.")
        print(f"Type: {type(result).__name__}")
        return True

    print(f"FAIL - Missing fields: {missing_fields}")
    return False


# ============================================================
# TEST 4 — SOURCE ATTRIBUTION
# ============================================================

async def test_source_attribution():
    print("\n========== TEST 4: SOURCE ATTRIBUTION ==========")

    agent = await create_rag_agent()

    result = await research_with_retry(agent, QUESTION)

    if "postgresql.txt" in result.sources:
        print("PASS - PostgreSQL source correctly attributed.")
        return True

    print("FAIL - PostgreSQL source was not returned.")
    
    return False


# ============================================================
# RUN ALL TESTS
# ============================================================

async def run_evaluation():
    results: dict[str, bool] = {}

    try:
        results["Happy Path"] = await test_happy_path()
    except Exception as e:
        print(f"FAIL - {type(e).__name__}: {e}")
        results["Happy Path"] = False

    try:
        results["Retrieval"] = await test_retrieval()
    except Exception as e:
        print(f"FAIL - {type(e).__name__}: {e}")
        results["Retrieval"] = False

    try:
        results["Structured Output"] = await test_structured_output()
    except Exception as e:
        print(f"FAIL - {type(e).__name__}: {e}")
        results["Structured Output"] = False

    try:
        results["Source Attribution"] = await test_source_attribution()
    except Exception as e:
        print(f"FAIL - {type(e).__name__}: {e}")
        results["Source Attribution"] = False

    print("\n========== EVALUATION RESULTS ==========")

    for test_name, passed in results.items():
        status = "PASS" if passed else "FAIL"
        print(f"{test_name:<22} {status}")

    overall = all(results.values())

    print("\n========================================")
    print(
        f"Overall              {'PASS' if overall else 'FAIL'}"
    )
    print("========================================")


if __name__ == "__main__":
    asyncio.run(run_evaluation())