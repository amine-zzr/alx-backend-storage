#!/usr/bin/env python3
"""
This module defines a `get_page` function
"""

from functools import wraps
import redis
import requests
from typing import Callable

# Initialize Redis client
redis_ = redis.Redis()


def count_requests(method: Callable[[str], str]) -> Callable[[str], str]:
    """
    Decorator to count how many times a specific URL has been accessed.
    It also caches the HTML content of the URL for 10 seconds.

    Args:
        method (Callable): The function to decorate

    Returns:
        Callable: The wrapped function with caching and request count tracking.
    """
    @wraps(method)
    def wrapper(url: str) -> str:
        """
        Wrapper function that increments the count of accesses

        Args:
            url (str): The URL to fetch.

        Returns:
            str: The HTML content of the requested URL.
        """
        # Increment the counter for the URL in Redis
        redis_.incr(f"count:{url}")

        # Check if the HTML content is already cached
        cached_html = redis_.get(f"cached:{url}")
        if cached_html:
            # Return the cached content if available
            return cached_html.decode('utf-8')

        # If not cached, fetch the HTML content
        html = method(url)

        # Cache the HTML content with an expiration of 10 seconds
        redis_.setex(f"cached:{url}", 10, html)

        return html

    return wrapper


@count_requests
def get_page(url: str) -> str:
    """
    Fetches the HTML content of a URL using the requests module.

    Args:
        url (str): The URL to fetch.

    Returns:
        str: The HTML content of the requested URL.
    """
    req = requests.get(url)
    return req.text
