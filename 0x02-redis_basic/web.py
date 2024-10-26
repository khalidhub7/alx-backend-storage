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
r.flushall()

def count_requests(method: Callable) -> Callable:
    """
    Count requests decorator
    """
    @wraps(method)
    def wrapper(self, url: str) -> str:
        """ Wrapper function """
        self._redis.incr(f"count:{url}")

        cached_html = self._redis.get(f"cached:{url}")
        if cached_html:
            return cached_html.decode('utf-8')

        html = method(self, url)
        self._redis.setex(f"cached:{url}", 10, html)
        return self._redis.get(f"cached:{url}").decode('utf-8')
    return wrapper


class WebCache:
    """ Web Cache class with Redis """
    def __init__(self):
        self._redis = redis.Redis(host='localhost', port=6379, db=0)
        self._redis.flushall()

    @count_requests
    def get_page(self, url: str) -> str:
        """ Get page content """
        response = requests.get(url)
        return response.text


# Example usage
if __name__ == "__main__":
    cache = WebCache()
    url = "http://slowwly.robertomurray.co.uk/delay/5000/url/http://www.example.com"
    print(cache.get_page(url))
    print(cache.get_page(url))  # Should retrieve from cache
