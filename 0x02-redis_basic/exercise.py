#!/usr/bin/env python3
""" redis basics """
import redis
import uuid
from functools import wraps
from typing import Union, Callable


def count_calls(method: Callable) -> Callable:
    """
Count calls to a method using Redis
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """
tore history of inputs and outputs for a function
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        input_key = f"{method.__qualname__}:inputs"
        output_key = f"{method.__qualname__}:outputs"
        self._redis.rpush(input_key, str(args))
        output = method(self, *args, **kwargs)
        self._redis.rpush(output_key, output)
        return output
    return wrapper


def replay(method: Callable):
    """Display the history of calls for a function."""
    redis_instance = method.__self__._redis
    method_key = method.__qualname__
    call_count = redis_instance.get(method_key).decode('utf-8')
    inputs = redis_instance.lrange(f"{method_key}:inputs", 0, -1)
    outputs = redis_instance.lrange(f"{method_key}:outputs", 0, -1)
    print(f"{method_key} was called {call_count} times:")
    for input_data, output_data in zip(inputs, outputs):
        print(
            f"{method_key}(*{input_data.decode('utf-8')}) -> {output_data.decode('utf-8')}")


class Cache:
    """ cache class """

    def __init__(self):
        """ initializing ... """
        self._redis = redis.Redis(
            host='localhost', port=6379)
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[
            str, bytes, int, float]) -> str:
        """
store data to redis-server
        """
        key = str(uuid.uuid4())
        self._redis.set(str(key), data)
        return key

    def get(self, key: str, fn: Callable = None) -> Union[
            str, bytes, int, float]:
        """ get value from redis server """
        value = self._redis.get(key)
        if value is not None:
            if fn:
                return fn(value)
            return value

    def get_str(self, key: str) -> str:
        """ str value """
        return str(self.get(
            key, lambda i: i.decode('utf-8')))

    def get_int(self, key: str) -> int:
        """ int value """
        return int(
            self.get(key, int))

