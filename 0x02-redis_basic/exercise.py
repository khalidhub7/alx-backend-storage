#!/usr/bin/env python3
""" redis basics """
import redis
import functools
from uuid import uuid4
from typing import Union, Callable


def count_calls(method: Callable) -> Callable:
    """ count calls of method """
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """ store history of inputs and outputs of a function """
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        inputs_key = f"{method.__qualname__}:inputs"
        outputs_key = f"{method.__qualname__}:outputs"
        self._redis.rpush(inputs_key, str(args))
        result = method(self, *args, **kwargs)
        self._redis.rpush(outputs_key, str(result))
        return result
    return wrapper


class Cache:
    """ store data in redis """

    def __init__(self) -> None:
        """ constructor """
        self._redis = redis.Redis(
            host='localhost', port=6379)
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, int, bytes, float]) -> str:
        """ store value in uuid key """
        key = str(uuid4())
        self._redis.set(key, data)
        # store data type in redis itself
        self._redis.set(f"{key}:type", type(data).__name__)
        return key

    def get(self,
            key: str,
            fn: Callable = None) -> Union[bytes,
                                          int,
                                          str,
                                          float,
                                          None]:
        """ get value from redis """
        data = self._redis.get(key)
        if data is None:
            return None

        if fn:
            return fn(data)

        # Get the type and convert accordingly
        data_type = self._redis.get(f"{key}:type")
        if data_type == b'str':
            return data.decode('utf-8')
        elif data_type == b'int':
            return int(data)
        elif data_type == b'float':
            return float(data)
        return data

    def get_str(self, key: str) -> Union[str, None]:
        """ convert value to str """
        data = self._redis.get(key)
        if data is None:
            return None
        return data.decode('utf-8')

    def get_int(self, key: str) -> Union[int, None]:
        """ convert value to int """
        data = self._redis.get(key)
        if data is None:
            return None
        try:
            return int(data)
        except ValueError:
            return None


def replay(method: Callable) -> None:
    """Display the history of calls of a particular function."""
    redis_client = method.__self__._redis
    method_name = method.__qualname__
    inputs_key = f"{method_name}:inputs"
    outputs_key = f"{method_name}:outputs"
    inputs = redis_client.lrange(inputs_key, 0, -1)
    outputs = redis_client.lrange(outputs_key, 0, -1)
    print(f"{method_name} was called {len(inputs)} times:")
    for input_args, output in zip(inputs, outputs):
        print(
            f"{method_name}(*{input_args.decode('utf-8')}) -> {output.decode('utf-8')}")
