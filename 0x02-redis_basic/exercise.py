#!/usr/bin/env python3
"""Redis basics with improved error handling and functionality."""
import redis
from uuid import uuid4
from typing import Union, Callable


class Cache:
    """Class to store data in Redis."""

    def __init__(self) -> None:
        """Initialize the Cache instance."""
        self._redis = redis.Redis(host='localhost', port=6379)
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Store a value in Redis and return the key."""
        key = str(uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Callable = None) -> Union[bytes, int, str, float, None]:
        """Retrieve a value from Redis."""
        data = self._redis.get(key)
        if data is None:
            return None
        return fn(data) if fn else data

    def get_str(self, key: str) -> Union[str, None]:
        """Retrieve a string value from Redis."""
        return self.get(key, lambda x: x.decode('utf-8'))

    def get_int(self, key: str) -> Union[int, None]:
        """Retrieve an integer value from Redis."""
        return self.get(key, lambda x: int(x))


def replay(method: Callable) -> None:
    """Display the history of calls of a particular function."""
    if method is None or not hasattr(method, '__self__'):
        return
    redis_client = getattr(method.__self__, '_redis', None)
    if not isinstance(redis_client, redis.Redis):
        return
    method_name = method.__qualname__
    inputs_key = f"{method_name}:inputs"
    outputs_key = f"{method_name}:outputs"
    call_count = int(redis_client.get(method_name) or 0)
    print(f"{method_name} was called {call_count} times:")
    inputs = redis_client.lrange(inputs_key, 0, -1)
    outputs = redis_client.lrange(outputs_key, 0, -1)
    for input_args, output in zip(inputs, outputs):
        print(f"{method_name}(*{input_args.decode('utf-8')}) -> {output.decode('utf-8')}")
