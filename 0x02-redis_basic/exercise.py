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


def call_history(method: Callable) -> Callable:
    """
    A decorator that records the history of inputs and outputs

    Args:
        method (Callable): The method to be decorated.

    Returns:
        Callable: The wrapped method that stores inputs and outputs.
    """

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function that records the inputs and outputs to Redis lists.

        Args:
            self: The Cache instance to access the Redis client.
            *args: Positional arguments for the method.
            **kwargs: Keyword arguments for the method (not used).

        Returns:
            The output of the original method.
        """
        # Step 2: Get Redis keys for storing inputs and outputs
        input_key = f"{method.__qualname__}:inputs"
        output_key = f"{method.__qualname__}:outputs"

        # Step 3: Store the input arguments (converted to a string)
        self._redis.rpush(input_key, str(args))

        # Step 4: Call the original method to get the output
        output = method(self, *args, **kwargs)

        # Step 5: Store the output
        self._redis.rpush(output_key, str(output))

        return output

    return wrapper


def replay(method: Callable) -> None:
    """
    Displays the history of inputs and outputs for a given method by retrieving
    the stored history from Redis.

    Args:
        method (Callable): The method whose history should be replayed.
    """
    # Retrieve the qualified name of the method to form the Redis keys
    qualified_name = method.__qualname__

    # Get the Redis instance from the first argument (self)
    self = method.__self__

    # Keys for inputs and outputs stored in Redis
    input_key = f"{qualified_name}:inputs"
    output_key = f"{qualified_name}:outputs"

    # Fetch the inputs and outputs using LRANGE
    inputs = self._redis.lrange(input_key, 0, -1)
    outputs = self._redis.lrange(output_key, 0, -1)

    # Determine how many times the function was called
    num_calls = len(inputs)

    # Display the number of calls
    print(f"{qualified_name} was called {num_calls} times:")

    # Iterate over inputs and outputs and print the replay details
    for input_data, output_data in zip(inputs, outputs):
        # Decode the byte strings to a readable format
        input_data = input_data.decode("utf-8")
        output_data = output_data.decode("utf-8")

        # Print the inputs and outputs in the required format
        print(f"{qualified_name}(*{input_data}) -> {output_data}")


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
    @call_history
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
