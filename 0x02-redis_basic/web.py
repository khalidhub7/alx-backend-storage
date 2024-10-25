#!/usr/bin/env python3
"""Implementing an expiring web cache and tracker with Redis and requests"""

import redis
import requests
from typing import Callable
from functools import wraps

r = redis.Redis()

def count_requests(method: Callable) -> Callable:
    """Decorator to count requests and cache responses."""
    @wraps(method)
    def wrapper(url: str) -> str:
        """Wrapper function to manage caching and counting."""
        try:
            cached_html = r.get(f"cached:{url}")
            if cached_html:
                return cached_html.decode('utf-8')
            
            html = method(url)
            r.incr(f"count:{url}")
            r.setex(f"cached:{url}", 10, html)
            return html
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return ""
    return wrapper

@count_requests
def get_page(url: str) -> str:
    """Fetch HTML content of the specified URL."""
    response = requests.get(url)
    response.raise_for_status()  # Raises an error for bad status codes
    return response.text
