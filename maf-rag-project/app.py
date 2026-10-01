import asyncio

from agent_framework_ollama import OllamaChatClient

from rag_research_agent import RAGResearchAgent
from rag_error_handling import research_with_retry
from rag_observability import trace_rag


async def main():
    client = OllamaChatClient(model="llama3.1:latest")

    research_agent = RAGResearchAgent(client)

    question = "Which database supports ACID transactions?"

    try:

        # result = await research_with_retry(research_agent, question)
        with trace_rag("RAG Research"):
            result = await research_with_retry(research_agent, question)

        print("\n========== RAG RESULT ==========")

        print("\nAnswer:")
        print(result.answer)

        print("\nSources:")
        for source in result.sources:
            print("-", source)

    except Exception as e:

        print("\n========== FINAL FAILURE ==========")
        print(type(e).__name__)
        print("Error:", e)


if __name__ == "__main__":
    asyncio.run(main())