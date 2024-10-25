#!/usr/bin/env python3
""" web cache and tracker """
import requests
import redis

store = redis.Redis()


def get_page(url: str) -> str:
    """ Returns HTML content of a URL and tracks URL access count in Redis """
    count_key = f"count:{url}"
    cached_key = f"cached:{url}"
    
    cached_data = store.get(cached_key)
    if cached_data:
        return cached_data.decode("utf-8")
    
    html = requests.get(url).text
    store.incr(count_key)
    store.setex(cached_key, 10, html)
    return html
