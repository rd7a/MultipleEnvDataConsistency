import logging
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logger = logging.getLogger(__name__)

# Status codes that are safe to retry (server-side or transient errors)
_RETRYABLE_STATUSES: list[int] = [408, 429, 500, 502, 503, 504]


def get_with_retry(
    url: str,
    max_retries: int = 3,
    backoff_factor: float = 1.0,
    **kwargs,
) -> requests.Response:
    """
    GET request with automatic retry on transient failures.

    Retries on connection errors, timeouts, and retryable HTTP status codes.
    Backoff between attempts: 0s, backoff_factor*2^1, backoff_factor*2^2, ...
    """
    session = requests.Session()
    retry = Retry(
        total=max_retries,
        backoff_factor=backoff_factor,
        status_forcelist=_RETRYABLE_STATUSES,
        allowed_methods=["GET"],
        raise_on_status=False,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)

    logger.debug("GET %s (max_retries=%d, backoff=%.1f)", url, max_retries, backoff_factor)
    return session.get(url, **kwargs)
