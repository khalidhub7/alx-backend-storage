#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
web.py - A simple web page fetcher with caching

Usage:
    from web import get_page
    html = get_page('http://example.com')
"""

import requests
from functools import wraps
from cachetools import cached, TTLCache

# Create a cache with a TTL of 10 seconds
cache = TTLCache(maxsize=100, ttl=10)

def cache_result(ttl=10):
    """Decorator to cache the result of a function for a given TTL"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            key = f"count:{args[0]}"
            result = cache.get(key)
            if result is None:
                result = func(*args, **kwargs)
                cache[key] = result
            return result
        return wrapper
    return decorator

@cache_result(ttl=10)
def get_page(url: str) -> str:
    """
    Fetch the HTML content of a given URL and return it.

    Args:
        url (str): The URL to fetch

    Returns:
        str: The HTML content of the page
    """
    response = requests.get(url)
    response.raise_for_status()
    return response.text
