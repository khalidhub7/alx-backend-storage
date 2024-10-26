#!/usr/bin/env python3
""" redis basics """
import redis
import uuid
from functools import wraps
from typing import Union, Callable

def count_calls(method: Callable) -> Callable:
    """
    Count calls of each function
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """
    Store history of inputs and outputs for a function
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        rpush: like append
        """
        name = method.__qualname__
        # push inputs
        self._redis.rpush(f'{name}:inputs', str(args))
        # push outputs
        output = method(self, *args, **kwargs)
        self._redis.rpush(f'{name}:outputs', output)
        return output
    return wrapper


def replay(method: Callable):
    """ replay """
    _redis = method.__self__._redis
    method_name = method.__qualname__
    calls = int(_redis.get(method_name) or 0)
    inputs = _redis.lrange(f'{method_name}:inputs', 0, -1)
    outputs = _redis.lrange(f'{method_name}:outputs', 0, -1)
    print(f"{method_name} was called {calls} times:")
    for inp, out in zip(inputs, outputs):
        input_str = inp.decode('utf-8')
        output_str = out.decode('utf-8')
        print(f'{method_name}(*{input_str}) -> {output_str}')


class Cache:
    """ Cache class """

    def __init__(self):
        """ initializing ... """
        self._redis = redis.Redis(host='localhost', port=6379)
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store data to redis-server
        """
        key = str(uuid.uuid4())
        self._redis.set(str(key), data)
        return key

    def get(self, key: str, fn: Callable = None) -> Union[str, bytes, int, float]:
        """
        Get value from redis server
        """
        value = self._redis.get(key)
        if value is not None:
            if fn:
                return fn(value)
            return value

    def get_str(self, key: str) -> str:
        """ str value """
        return str(self.get(key, lambda i: i.decode('utf-8')))

    def get_int(self, key: str) -> int:
        """ int value """
        return int(self.get(key, int))


# Example usage
if __name__ == "__main__":
    cache = Cache()
    key = cache.store("Hello, Redis!")
    print(cache.get_str(key))
    print(cache.get_int(key))  # This will raise an error if the value isn't an integer
    replay(cache.store)
