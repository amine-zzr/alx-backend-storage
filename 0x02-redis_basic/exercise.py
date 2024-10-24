#!/usr/bin/env python3
"""
This module provides a Cache class to interface with Redis.
"""

import redis
import uuid
from typing import Union, Callable, Optional
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """
    A decorator that counts how many times the decorated method is called.
    """

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function that increments the call count in Redis
        """
        # Use the method's qualified name as the Redis key
        key = method.__qualname__
        # Increment the call count in Redis
        self._redis.incr(key)
        # Call the original method
        return method(self, *args, **kwargs)
    return wrapper


class Cache:
    """
    Cache class provides an interface to store data in Redis with random keys.

    Attributes:
        _redis (redis.Redis): Private Redis client instance.
    """

    def __init__(self) -> None:
        """
        Initializes a Cache instance and flushes the Redis database.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Stores the input data in Redis with a randomly generated key.

        Args:
            data (Union[str, bytes, int, float]): The data to be stored.

        Returns:
            str: The key under which the data is stored.
        """
        key = str(uuid.uuid4())  # Generate a random key
        self._redis.set(key, data)  # Store data in Redis
        return key

    def get(self, key: str,
            fn: Optional[Callable] = None) -> Union[str, bytes, int, None]:
        """
        Retrieves the data stored at the given key from Redis.
        Optionally applies a callable function to convert the data

        Args:
            key (str): The key for the data in Redis.
            fn (Optional[Callable]): A function to apply to the retrieved data.

        Returns:
            Union[str, bytes, int, None]: The data retrieved from Redis
        """
        data = self._redis.get(key)  # Get data from Redis
        if data is None:
            return None  # Return None if key doesn't exist

        if fn:
            return fn(data)  # Apply the callable if provided
        return data  # Default behavior: return raw data (bytes)

    def get_str(self, key: str) -> Optional[str]:
        """
        Retrieves the data stored at the given key as a UTF-8 decoded string.

        Args:
            key (str): The key for the data in Redis.

        Returns:
            Optional[str]: The data decoded as a UTF-8 string, or None
        """
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> Optional[int]:
        """
        Retrieves the data stored at the given key as an integer.

        Args:
            key (str): The key for the data in Redis.

        Returns:
            Optional[int]: The data converted to an integer, or None
        """
        return self.get(key, fn=lambda d: int(d))
