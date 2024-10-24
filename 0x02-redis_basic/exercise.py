#!/usr/bin/env python3
""" redis basics """
import redis
from uuid import uuid4
from typing import Union

r = redis.Redis(
    host='localhost', port=6379)


class Cache:
    """ store data in redis """

    def __init__(self):
        """ constructor """
        self._redis = r
        self._redis.flushdb()

    def store(
            self, data: Union[
                str, int, bytes, float
            ]) -> str:
        """ store value in uuid key """
        keyy = str(uuid4())
        self._redis.set(keyy, data)
        return keyy
