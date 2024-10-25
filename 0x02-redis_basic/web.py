#!/usr/bin/env python3
""" Track URL access and cache content with expiration """

import redis
import requests
from functools import wraps
from typing import Callable

redis_client = redis.Redis()


def count_requests(method: Callable) -> Callable:
    """Decorator to count requests to a URL"""

    @wraps(method)
    def wrapper(url: str) -> str:
        redis_client.incr(f"count:{url}")
        return method(url)
    return wrapper


def cache_with_expiration(timeout: int) -> Callable:
    """Decorator to cache request result with expiration"""

    def decorator(method: Callable) -> Callable:
        @wraps(method)
        def wrapper(url: str) -> str:
            cached = redis_client.get(url)
            if cached:
                return cached.decode("utf-8")

            result = method(url)
            redis_client.setex(url, timeout, result)
            return result
        return wrapper
    return decorator


@count_requests
@cache_with_expiration(10)
def get_page(url: str) -> str:
    """Fetch and return HTML content of a URL"""
    response = requests.get(url)
    return response.text

