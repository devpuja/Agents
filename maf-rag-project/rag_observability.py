import logging
import time
from contextlib import contextmanager


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)


@contextmanager
def trace_rag(operation: str):

    start_time = time.perf_counter()

    logging.info(
        "TRACE START | %s",
        operation
    )

    try:

        yield

        duration = time.perf_counter() - start_time

        logging.info(
            "TRACE SUCCESS | %s | %.2f seconds",
            operation,
            duration
        )

    except Exception as e:

        duration = time.perf_counter() - start_time

        logging.error(
            "TRACE FAILURE | %s | %.2f seconds | %s: %s",
            operation,
            duration,
            type(e).__name__,
            e
        )

        raise