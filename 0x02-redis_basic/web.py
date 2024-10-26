#!/usr/bin/env python3
"""
Implementing an expiring web cache and tracker
"""
import redis
import requests
from functools import wraps
from typing import Callable
from exercise import count_calls, call_history

# Redis connection
r = redis.Redis(host='localhost', port=6379, db=0)


def count_requests(method: Callable) -> Callable:
    """
    Count requests decorator
    """
    @wraps(method)
    def wrapper(url: str) -> str:
        """ Wrapper function """
        r.incr("count:{}".format(str(url)))
        cached_html = r.get("cached:{}".format(str(url)))
        if cached_html:
            return cached_html.decode('utf-8')
        html = method(url)
        r.setex("cached:{}".format(url), 10, html)
        return html
    return wrapper


class WebCache:
    """ Web Cache class """
    def __init__(self):
        self._redis = redis.Redis(host='localhost', port=6379, db=0)
        self._redis.flushdb()

    @count_requests
    @count_calls
    @call_history
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
