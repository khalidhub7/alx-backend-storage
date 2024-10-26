#!/usr/bin/env python3
"""
Implementing an expiring web cache and tracker
"""
import redis
import requests
from typing import Callable
from functools import wraps

# Redis connection
r = redis.Redis(host='localhost', port=6379, db=0)

def count_requests(method: Callable) -> Callable:
    """
    Count requests decorator
    """
    @wraps(method)
    def wrapper(url: str) -> str:
        """ Wrapper function """
        cached_html = r.get(f"cached:{url}")
        if cached_html:
            return cached_html.decode('utf-8')

        # Increment only on a cache miss
        r.incr(f"count:{url}")

        html = method(url)
        r.setex(f"cached:{url}", 10, html)  # Cache for 10 seconds
        return html

    return wrapper

@count_requests
def get_page(url: str) -> str:
    """ Get page content """
    response = requests.get(url)
    return response.text
