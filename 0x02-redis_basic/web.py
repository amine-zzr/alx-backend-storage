#!/usr/bin/env python3
"""
Module to fetch and cache webpage content using Redis.
Tracks access count and caches the page content with a 10-second expiration.
"""

import redis
import requests
from typing import Callable

# Initialize Redis client
redis_client = redis.Redis()


def get_page(url: str) -> str:
    """
    Fetches the HTML content of a URL, tracks the number of accesses,
    and caches the content with an expiration of 10 seconds.

    Args:
        url (str): The URL of the page to fetch.

    Returns:
        str: The HTML content of the page.
    """
    # Redis key for access count
    count_key = f"count:{url}"

    # Redis key for cached HTML content
    cache_key = f"cache:{url}"

    # Increment the access count for this URL
    redis_client.incr(count_key)

    # Check if the content is cached in Redis
    cached_content = redis_client.get(cache_key)
    if cached_content:
        return cached_content.decode("utf-8")

    # If not cached, fetch the content from the URL
    response = requests.get(url)
    html_content = response.text

    # Cache the content with a 10-second expiration
    redis_client.setex(cache_key, 10, html_content)

    return html_content


# Optional: Bonus with a decorator
def cache_page(func: Callable) -> Callable:
    """
    Decorator to cache the result of a function that fetches a webpage,
    tracks access count, and applies caching with a 10-second expiration.

    Args:
        func (Callable): The function to decorate.

    Returns:
        Callable: The wrapped function with caching and tracking.
    """
    def wrapper(url: str) -> str:
        # Redis keys
        count_key = f"count:{url}"
        cache_key = f"cache:{url}"

        # Increment the access count for this URL
        redis_client.incr(count_key)

        # Check if the content is cached in Redis
        cached_content = redis_client.get(cache_key)
        if cached_content:
            return cached_content.decode("utf-8")

        # If not cached, fetch the content using the original function
        html_content = func(url)

        # Cache the content with a 10-second expiration
        redis_client.setex(cache_key, 10, html_content)

        return html_content

    return wrapper
