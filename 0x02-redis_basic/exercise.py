#!/usr/bin/env python3
""" redis basics """
import redis
import functools
from uuid import uuid4
from typing import Union, Callable, Any


def count_calls(method: Callable) -> Callable:
    """ count calls of method """
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs) -> Any:
        # Increment call count in Redis if Redis instance is valid
        if isinstance(self._redis, redis.Redis):
            self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """ store history of inputs and outputs of a function """
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs) -> Any:
        inputs_key = f"{method.__qualname__}:inputs"
        outputs_key = f"{method.__qualname__}:outputs"
        if isinstance(self._redis, redis.Redis):
            # Store input arguments in Redis
            self._redis.rpush(inputs_key, str(args))
        # Call original method and store result
        result = method(self, *args, **kwargs)
        if isinstance(self._redis, redis.Redis):
            # Store output result in Redis
            self._redis.rpush(outputs_key, str(result))
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
        print(f"{method_name}(*{input_args.decode('utf-8')}) -> {output.decode('utf-8')}")


class Cache:
    """ store data in redis """

    def __init__(self) -> None:
        """ constructor """
        self._redis = redis.Redis(host='localhost', port=6379)
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, int, bytes, float]) -> str:
        """ store value in uuid key """
        key = str(uuid4())
        self._redis.set(key, data)
        # store data type in redis itself
        self._redis.set(f"{key}:type", type(data).__name__)
        return key

    def get(self, key: str, fn: Callable = None) -> Union[bytes, int, str, float, None]:
        """ get value from redis """
        data = self._redis.get(key)
        if data is None:
            return None
        return fn(data) if fn else data

    def get_str(self, key: str) -> str:
        """ convert value to str """
        data = self._redis.get(key)
        if data is None:
            return ""
        return data.decode('utf-8')

    def get_int(self, key: str) -> int:
        """ convert value to int """
        data = self._redis.get(key)
        if data is None:
            return 0
        return int(data)
