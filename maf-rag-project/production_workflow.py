import asyncio

from agent_framework_ollama import OllamaChatClient

from rag_research_agent import RAGResearchAgent
from rag_error_handling import research_with_retry
from rag_observability import trace_rag


async def run_production_workflow(question: str):

    client = OllamaChatClient(
        model="llama3.1:latest"
    )

    research_agent = RAGResearchAgent(client)

    try:

        with trace_rag("End-to-End RAG Workflow"):

            result = await research_with_retry(
                research_agent,
                question
            )

        return result

    except Exception as e:

        print("\n========== WORKFLOW FAILURE ==========")
        print(type(e).__name__)
        print("Error:", e)

        raise


async def main():

    question = ("Which database supports ACID transactions?")

    print("\n========== END-TO-END RAG WORKFLOW ==========")

    print("\nUser Question:")
    print(question)

    result = await run_production_workflow(question)

    print("\n========== FINAL ANSWER ==========")

    print(result.answer)

    print("\n========== SOURCES ==========")

    for source in result.sources:
        print("-", source)

    print("\n========== RETRIEVED CONTEXT ==========")

    for chunk in result.retrieved_chunks:
        print("-", chunk)


if __name__ == "__main__":
    asyncio.run(main())