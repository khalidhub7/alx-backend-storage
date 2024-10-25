#!/usr/bin/env python3
""" redis basics """
import redis
import uuid
from typing import Union, Callable


class Cache:
    """ cache class """

    def __init__(self):
        """ initializing ... """
        self._redis = redis.Redis(
            host='localhost', port=6379)
        self._redis.flushdb()

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

