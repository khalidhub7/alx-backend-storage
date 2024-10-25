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

class Cache:
    """ store data in redis """

    def __init__(self) -> None:
        """ constructor """
        self._redis = redis.Redis(
            host='localhost', port=6379)
        self._redis.flushdb()

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
