#!/usr/bin/env python3
"""Writing strings to Redis"""
import redis
import uuid
from typing import Union, Callable, Optional
from functools import wraps


def replay(method: Callable):
    """show the history of method calls"""
    input_key = f"{method.__qualname__}:inputs"
    output_key = f"{method.__qualname__}:outputs"

    redis_client = redis.Redis()

    inputs = redis_client.lrange(input_key, 0, -1)
    outputs = redis_client.lrange(output_key, 0, -1)

    print(f"{method.__qualname__} was called {len(inputs)} times:")
    for input_value, output_value in zip(inputs, outputs):
        input_str = input_value.decode('utf-8')
        output_str = output_value.decode('utf-8')
        print(f"{method.__qualname__}(*{input_str}) -> {output_str}")


def count_calls(method: Callable) -> Callable:
    """Decorator count the number of time methods of Cache class
    are called.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Wrapper function that increments the call count
        in Redis and calls the original method
        """
        key = method.__qualname__
        self._redis.incr(key)
        return(method(self, *args, *kwargs))

    return(wrapper)


def call_history(method: Callable) -> Callable:
    """Decorator to store function call history in redis"""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Wrapper function that logs input and output in redis"""
        inps = f"{method.__qualname__}:inputs"
        outs = f"{method.__qualname__}:outputs"

        self._redis.rpush(inps, str(args))
        ex_original_func = method(self, *args, **kwargs)
        self._redis.rpush(outs, str(ex_original_func))

        return (ex_original_func)
    return (wrapper)


class Cache:
    """Cache classe for interacting with redis."""
    def __init__(self) -> None:
        """init cache instance:
        init new redis client and flush redis db.
        ps: redis client stored as private variable.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """ store data in redis with a random key(string)
        as a key = value.
        return the key
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return (key)

    def get(self, key: str, fn: Optional[Callable] = None
            ) -> Union[str, bytes, int, float]:
        """get key"""
        get_key = self._redis.get(key)
        if get_key is None:
            return(None)
        if fn:
            return (fn(get_key))
        return (get_key)

    def get_str(self, key: str) -> str:
        """get key as str"""
        key_to_convert = self.get(key, str)
        return(key_to_convert)

    def get_int(self, key: int) -> int:
        """get key as int"""
        key_to_convert = self.get(key, int)
        return (key_to_convert)
