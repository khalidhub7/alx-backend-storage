#!/usr/bin/env python3
""" redis basics """
import redis
import uuid
from typing import Union


class Cache:
    """ cache class """

    def __init__(self) -> None:
        """ initializing ... """
        self._redis = redis.Redis()
        self._redis.flushdb(True)

    def store(self, data: Union[str, bytes, int, float]):
        """
store data to redis-server
        """
        key = uuid.uuid4()
        self._redis.set(str(key), data)
        return key
