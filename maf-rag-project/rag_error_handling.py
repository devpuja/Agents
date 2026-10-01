import asyncio
import random

from rag_research_agent import RAGResearchAgent, RAGResearchResult


MAX_RETRIES = 3
TIMEOUT_SECONDS = 120


class RetryableRAGError(Exception):
    pass


class NonRetryableRAGError(Exception):
    pass


class RAGTimeoutError(Exception):
    pass


async def research_with_retry(
    research_agent: RAGResearchAgent,
    question: str,
    max_retries: int = MAX_RETRIES,
    timeout_seconds: int = TIMEOUT_SECONDS) -> RAGResearchResult:

    for attempt in range(1, max_retries + 1):

        try:

            print(f"\nAttempt {attempt}...")

            result = await asyncio.wait_for(
                research_agent.research(question),
                timeout=timeout_seconds
            )

            print("RAG Research Agent succeeded.")

            return result

        except asyncio.TimeoutError:

            error = RAGTimeoutError(
                f"RAG Research Agent timed out "
                f"after {timeout_seconds} seconds."
            )

            if attempt == max_retries:
                print("Maximum retry attempts reached.")
                raise error

            print(
                f"Retryable error on attempt {attempt}: "
                f"{error}"
            )

        except RetryableRAGError as e:

            print(f"Retryable error on attempt {attempt}: {e}")

            if attempt == max_retries:
                print("Maximum retry attempts reached.")
                raise

        except NonRetryableRAGError as e:
            print(f"Non-retryable error: {e}")
            print("Failing immediately. No retry.")

            raise

        base_delay = 2 ** (attempt - 1)
        jitter = random.uniform(0, 0.5)
        delay = base_delay + jitter

        print(f"Waiting {delay:.6f} seconds before retry...")

        await asyncio.sleep(delay)

        print("Retrying...")

    raise RuntimeError("Unexpected retry loop termination.")