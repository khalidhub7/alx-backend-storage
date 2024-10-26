#!/usr/bin/env python3
"""
An expiring web cache and tracker
"""
import requests
import redis
from functools import wraps

# Create a Redis instance
store = redis.Redis()

def count_url_access(method):
    """
    Decorator to count how many times a URL is accessed and cache the result.
    """
    @wraps(method)
    def wrapper(url: str) -> str:
        # Check if the HTML content is already cached
        key_cache = f"cached:{url}"
        cached_data = store.get(key_cache)
        if cached_data:
            return cached_data.decode("utf-8")
        
        # If not cached, call the original method to get the HTML
        key_count = f"count:{url}"
        html = method(url)
        
        # Increment the count of how many times this URL was accessed
        store.incr(key_count)
        
        # Cache the HTML content and set an expiration of 10 seconds
        store.set(key_cache, html, ex=10)
        
        return html
    return wrapper

@count_url_access
def get_page(url: str) -> str:
    """
    Fetches the HTML content of a URL using the requests module.
    """
    response = requests.get(url)
    response.raise_for_status()  # Raises an error for bad responses
    return response.text

# Example usage (use http://slowwly.robertomurray.co.uk to simulate slow response)
if __name__ == "__main__":
    test_url = "http://slowwly.robertomurray.co.uk/delay/2000/url/http://www.example.com"
    print(get_page(test_url))
    print(get_page(test_url))  # Should return cached result on the second call
