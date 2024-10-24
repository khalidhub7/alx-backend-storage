#!/usr/bin/env python3
""" redis basics """
import redis
from uuid import uuid4
from typing import Union


class Cache:
    """ store data in redis """

    def __init__(self):
        """ constructor """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(
            self, data: Union[
                str, int, bytes, float
            ]) -> str:
        """ store value in uuid key """
        keyy = str(uuid4())
        self._redis.set(keyy, data)
        return keyy
