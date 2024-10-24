#!/usr/bin/env python3
""" redis basics """
import redis
from uuid import uuid4
from typing import Union

r = redis.Redis(
    host='localhost', port=6379)


class Cache:
    def __init__(self):
        self._redis = r
        self._redis.flushdb()

    def store(
            self, data: Union[
                str, int, bytes, float
            ]) -> str:
        keyy = str(uuid4())
        self._redis.set(keyy, data)
        return keyy
