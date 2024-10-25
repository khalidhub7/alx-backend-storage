#!/usr/bin/env python3
""" redis basics """
import redis
from uuid import uuid4
from typing import Union, Callable


class Cache:
    """ store data in redis """

    def __init__(self) -> None:
        """ constructor """
        self._redis = redis.Redis(
            host='localhost', port=6379)
        self._redis.flushdb()

    def store(
            self, data: Union[
                str, int, bytes, float
            ]) -> str:
        """ store value in uuid key """
        keyy = str(uuid4())
        self._redis.set(keyy, data)
        # store data type in redis itself
        self._redis.set(f"{keyy}:type", type(data).__name__)
        return keyy

    def get(self, key: str, fn: Callable = None) -> Union[
            bytes, int, str, float, None]:
        """ get value from redis """
        data = self._redis.get(key)
        if data is None:
            return None
        elif fn is not None and data is not None:
            return fn(data)

        data_type = self._redis.get(f"{key}:type")
        if data_type == b'str':
            return self.get_str(key)
        elif data_type == b'int':
            return self.get_int(key)
        else:
            return data

    def get_str(self, key: str) -> Union[str, None]:
        """ convert value to str """
        data = self.get(key, lambda i: i.decode('utf-8'))
        if data is None:
            return None
        return data

    def get_int(self, key: str) -> Union[int, None]:
        """ convert value to int """
        try:
            return self.get(key, int)
        except ValueError:
            return None
