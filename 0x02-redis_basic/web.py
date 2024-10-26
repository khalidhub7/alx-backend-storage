#!/usr/bin/env python3
"""
Implementing an expiring web cache and tracker with enhanced functionality
"""
import redis
import requests
import uuid
from functools import wraps
from typing import Callable, Union

# Redis connection
r = redis.Redis(host='localhost', port=6379, db=0)

# Decorators for counting calls and storing call history
def count_calls(method: Callable) -> Callable:
    """
    Count calls of each function
    """
    @wraps(method)
    def wrapper(*args, **kwargs):
        key = method.__qualname__
        r.incr(key)
        return method(*args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """
    Store history of inputs and outputs for a function
    """
    @wraps(method)
    def wrapper(*args, **kwargs):
        name = method.__qualname__
        # Push inputs
        r.rpush(f"{name}:inputs", str(args))
        # Execute method and store output
        output = method(*args, **kwargs)
        r.rpush(f"{name}:outputs", output)
        return output
    return wrapper


def replay(method: Callable):
    """ Replay stored history of inputs and outputs for a function """
    method_name = method.__qualname__
    calls = int(r.get(method_name) or 0)
    inputs = r.lrange(f"{method_name}:inputs", 0, -1)
    outputs = r.lrange(f"{method_name}:outputs", 0, -1)
    print(f"{method_name} was called {calls} times:")
    for inp, out in zip(inputs, outputs):
        input_str = inp.decode('utf-8')
        output_str = out.decode('utf-8')
        print(f"{method_name}(*{input_str}) -> {output_str}")


# Enhanced Cache class with history tracking
class Cache:
    """ Cache class for storing and retrieving data """
    def __init__(self):
        """ Initialize the Redis connection and flush the database """
        self._redis = redis.Redis(host='localhost', port=6379, db=0)
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store data in Redis and return a unique key
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Callable = None) -> Union[str, bytes, int, float]:
        """
        Retrieve data from Redis, optionally applying a conversion function
        """
        value = self._redis.get(key)
        if value is not None and fn:
            return fn(value)
        return value

    def get_str(self, key: str) -> str:
        """ Retrieve a string value from Redis """
        return self.get(key, lambda x: x.decode('utf-8'))

    def get_int(self, key: str) -> int:
        """ Retrieve an integer value from Redis """
        return self.get(key, int)


# Function to get page content with caching and tracking
@count_calls
@call_history
def get_page(url: str) -> str:
    """ Get page content and track requests """
    # Check if content is cached
    cached_html = r.get(f"cached:{url}")
    if cached_html:
        return cached_html.decode('utf-8')

    # Cache miss, increment count and fetch from the web
    r.incr(f"count:{url}")
    response = requests.get(url)
    html = response.text

    # Cache the content for 10 seconds
    r.setex(f"cached:{url}", 10, html)
    return html

# Example usage
if __name__ == "__main__":
    cache = Cache()
    url = "http://slowwly.robertomurray.co.uk/delay/5000/url/http://www.example.com"
    print(get_page(url))
    print(get_page(url))  # Should retrieve from cache
    replay(get_page)

    # Store and retrieve data using Cache
    key = cache.store("some data")
    print(cache.get_str(key))
    replay(cache.store)
