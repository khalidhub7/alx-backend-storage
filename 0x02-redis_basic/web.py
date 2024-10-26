#!/usr/bin/env python3
"""
web.py

This module contains the get_page function that fetches HTML content from a URL,
tracks access count, and caches the result for a specified duration.
"""

import requests
import redis
from functools import wraps

# Redis connection
r = redis.Redis()

def cache_page(expiration=10):
    """
    Decorator to cache the HTML content of a URL for a given expiration time
    and track the number of times the URL was accessed.

    Args:
        expiration (int): Time in seconds for the cache to expire.

    Returns:
        Function: A wrapped function with caching and tracking enabled.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(url):
            key_count = f"count:{url}"
            key_cache = f"cache:{url}"
            r.incr(key_count)
            cached_content = r.get(key_cache)
            if cached_content:
                return cached_content.decode("utf-8")
            result = func(url)
            r.setex(key_cache, expiration, result)
            return result
        return wrapper
    return decorator

@cache_page()
def get_page(url: str) -> str:
    """
    Fetches the HTML content of a URL.

    Args:
        url (str): The URL to fetch.

    Returns:
        str: HTML content of the URL.
    """
    response = requests.get(url)
    return response.text
