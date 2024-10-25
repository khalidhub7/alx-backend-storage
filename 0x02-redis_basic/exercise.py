#!/usr/bin/env python3
""" redis basics """
import redis
import uuid
from typing import Union


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
