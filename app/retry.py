import random
import time
from collections.abc import Callable
from typing import TypeVar

T = TypeVar("T")


def retry_sync(
    fn: Callable[[], T],
    *,
    tries: int = 5,
    base_delay: float = 0.5,
    max_delay: float = 8.0,
) -> T:
    """Retries a synchronous function applying an exponential backoff."""
    last_exc = None
    for attempt in range(tries):
        try:
            return fn()
        except Exception as exc:
            last_exc = exc
            if attempt == tries - 1:
                raise
            delay = min(max_delay, base_delay * (2**attempt))
            delay = delay * (0.8 + 0.4 * random.random())  # Jitter to avoid thundering herd
            time.sleep(delay)
    raise last_exc  # type: ignore
