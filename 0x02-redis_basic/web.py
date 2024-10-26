#!/usr/bin/env python3
"""
An expiring web cache and tracker
"""
import requests
import redis
from functools import wraps

store = redis.Redis()

def count_url_access(method):
    """
    Decorator to count how many times a URL is accessed and cache the result.
    """
    @wraps(method)
    def wrapper(url: str) -> str:
        key_cache = f"cached:{url}"
        cached_data = store.get(key_cache)
        if cached_data:
            return cached_data

        key_count = f"count:{url}"
        html = method(url)

        store.incr(key_count)
        store.set(key_cache, html, ex=10)

        return html

    return wrapper


@count_url_access
def get_page(url: str) -> str:
    """
    Fetches the HTML content of a URL using the requests module.
    """
    response = requests.get(url)
    response.raise_for_status()
    return response.text


if __name__ == "__main__":
    test_url = "http://slowwly.robertomurray.co.uk/delay/2000/url/http://www.example.com"
    print(get_page(test_url))
    print(get_page(test_url))
