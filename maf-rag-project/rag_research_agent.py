from pydantic import BaseModel

from agent_framework import Agent
from agent_framework_ollama import OllamaChatClient

from rag_service import retrieve


class RAGResearchResult(BaseModel):
    answer: str
    sources: list[str]
    retrieved_chunks: list[str]


class RAGResearchAgent:
    def __init__(self, client: OllamaChatClient):

        self.agent = Agent(
            client=client,
            name="RAGResearchAgent",
            instructions=(
                "You are a research agent that uses retrieved "
                "documents to answer questions.\n\n"
                "Use only the retrieved context.\n"
                "Do not invent information.\n"
                "Return a concise answer."
            )
        )

    async def research(self, question: str) -> RAGResearchResult:
        results = await retrieve(
            question,
            top_k=2
        )

        context = "\n\n".join(
            f"Source: {result['filename']}\n"
            f"Content:\n{result['content']}"
            for result in results
        )

        prompt = (
            f"Research Question:\n"
            f"{question}\n\n"
            f"Retrieved Context:\n"
            f"{context}\n\n"
            f"Answer using only the retrieved context."
        )

        response = await self.agent.run(
            prompt,
            options={
                "response_format": RAGResearchResult
            }
        )

        if not isinstance(response.value, RAGResearchResult):
            raise ValueError("Invalid response from the agent.")
        else:
            return response.value