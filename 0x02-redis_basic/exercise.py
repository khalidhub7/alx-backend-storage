#!/usr/bin/env python3
"""Redis basics with method call counting and replay functionality."""
import redis
import functools
from uuid import uuid4
from typing import Union, Callable, Any

def count_calls(method: Callable) -> Callable:
    """Decorator to count calls to a method."""
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs) -> Any:
        self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """Decorator to store history of inputs and outputs of a function."""
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs) -> Any:
        inputs_key = f"{method.__qualname__}:inputs"
        outputs_key = f"{method.__qualname__}:outputs"
        self._redis.rpush(inputs_key, str(args))
        result = method(self, *args, **kwargs)
        self._redis.rpush(outputs_key, result)
        return result
    return wrapper


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
        print(f"{method_name}(*{input_args}) -> {output}")


class Cache:
    """Class to store data in Redis."""

    def __init__(self) -> None:
        """Initialize the Cache instance."""
        self._redis = redis.Redis(
            host='localhost',
            port=6379,
            decode_responses=True)
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Store a value in Redis and return the key."""
        key = str(uuid4())
        self._redis.set(key, data)
        return key

    def get(self,
            key: str,
            fn: Callable = None) -> Union[bytes,
                int,
                str,
                float,
                None]:
        """Retrieve a value from Redis."""
        data = self._redis.get(key)
        if data is None:
            return None
        return fn(data) if fn else data

    def get_str(self, key: str) -> Union[str, None]:
        """Retrieve a string value from Redis."""
        return self.get(key, lambda x: x.decode("utf-8"))

    def get_int(self, key: str) -> Union[int, None]:
        """Retrieve an integer value from Redis."""
        return self.get(key, lambda x: int(x))
