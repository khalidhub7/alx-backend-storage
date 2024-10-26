#!/usr/bin/env python3
"""
An expiring web cache and tracker
"""
import requests
import redis
from functools import wraps
from typing import Callable

store = redis.Redis()

def cache_and_count(expire: int = 10) -> Callable:
    """
    Decorator to cache the HTML response of a URL and count the number of times accessed.
    """
    def decorator(method: Callable[[str], str]) -> Callable[[str], str]:
        @wraps(method)
        def wrapper(url: str) -> str:
            key_cache = f"cached:{url}"
            key_count = f"count:{url}"

            # Attempt to retrieve from cache
            cached_data = store.get(key_cache)
            if cached_data:
                return cached_data

            # If not cached, fetch and store in cache
            html = method(url)
            store.incr(key_count)
            store.set(key_cache, html, ex=expire)

            return html

        return wrapper
    return decorator


@cache_and_count(expire=10)
def get_page(url: str) -> str:
    """
    Fetches the HTML content of a URL using the requests module.
    """
    response = requests.get(url)
    return response.text
