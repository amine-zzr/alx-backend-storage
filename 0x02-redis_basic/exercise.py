#!/usr/bin/env python3
"""
This module provides a Cache class to interface with Redis.
"""

import redis
import uuid
from typing import Union


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
