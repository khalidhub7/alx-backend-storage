
#!/usr/bin/env python3
"""
an expiring web cache and tracker
"""
import requests
import redis
from functools import wraps
r = redis.Redis()


def count_url_access(method):
    """
count times that a URL is accessed
    """
    @wraps(method)
    def wrapper(url):
        key_cache = "cached:" + url
        data_cache = r.get(key_cache)
        if data_cache:
            return data_cache.decode("utf-8")
        key_count = "count:" + url
        html = method(url)
        r.incr(key_count)
        r.set(key_cache, html, ex=10)
        return html
    return wrapper


@count_url_access
def get_page(url: str) -> str:
    """
html of cached site
    """
    req = requests.get(url)
    return req.text
