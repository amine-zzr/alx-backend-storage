#!/usr/bin/env python3
"""
This module defines a function to fetch a web page
"""

import redis
import requests
from typing import Callable
from functools import wraps


# Initialize Redis client
redis_client = redis.Redis()


def cache_result(expiration: int = 10):
    """
    Decorator to cache the result of a function in Redis.
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(url: str) -> str:
            # Check if the result is already cached
            cache_key = f"result:{url}"
            cached_result = redis_client.get(cache_key)
            if cached_result:
                return cached_result.decode('utf-8')

            # Otherwise, call the function to get the result and cache it
            result = func(url)
            redis_client.setex(cache_key, expiration, result)
            return result
        return wrapper
    return decorator


@cache_result(expiration=10)
def get_page(url: str) -> str:
    """
    Fetches the HTML content of a given URL
    """
    # Track how many times the URL has been accessed
    access_count_key = f"count:{url}"
    redis_client.incr(access_count_key)

    # Fetch the HTML content
    response = requests.get(url)
    return response.text
