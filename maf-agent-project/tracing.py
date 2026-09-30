import logging
import time
from contextlib import asynccontextmanager


logger = logging.getLogger("agent_tracing")


@asynccontextmanager
async def trace_agent(agent_name: str):
    start_time = time.perf_counter()

    logger.info("TRACE START | %s", agent_name)

    try:
        yield

        duration = time.perf_counter() - start_time
        logger.info(
            "TRACE SUCCESS | %s | %.2f seconds",
            agent_name,
            duration,
        )

    except Exception as e:
        duration = time.perf_counter() - start_time

        logger.error(
            "TRACE ERROR | %s | %.2f seconds | %s",
            agent_name,
            duration,
            e,
        )

        raise