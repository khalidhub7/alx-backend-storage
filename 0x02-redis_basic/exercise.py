#!/usr/bin/env python3
""" redis basics """
import redis
import uuid
from functools import wraps
from typing import Union, Callable


def count_calls(method: Callable
                ) -> Callable:
    """
count calls of each function
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        key = method.__qualname__
        self._redis.incr(key)
        return method(
            self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """
store history of inputs and outputs for a function
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
rpush: like append
        """
        name = method.__qualname__
        # push inputs
        self._redis.rpush(
            '{}:inputs'.format(name), str(args))
        # push outputs
        output = method(self, *args, **kwargs)
        self._redis.rpush(
            '{}:outputs'.format(name), output)
        return output
    return wrapper


def replay(method: Callable):
    """ replay """
    _redis = method.__self__._redis
    method_name = method.__qualname__
    calls = int(_redis.get(method_name)) or 0
    inputs = _redis.lrange(
        '{}:inputs'.format(method_name),
        0, -1)
    outputs = _redis.lrange(
        '{}:outputs'.format(method_name),
        0, -1)
    print("{} was called {} times:"
          .format(method_name, calls))
    for inp, out in zip(inputs, outputs):
        input_str = inp.decode('utf-8')
        output_str = out.decode('utf-8')
        print('{}(*{}) -> {}'.format(
            method_name, input_str,
            output_str))


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

    def get(self, key: str,
            fn: Callable = None) -> Union[
            str, bytes, int, float]:
        """
get value from redis server
        """
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
