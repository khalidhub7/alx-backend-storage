#!/usr/bin/env python3
"""
Implementing an expiring web cache and tracker
"""
import redis
import requests

# Redis connection
r = redis.Redis(host='localhost', port=6379, db=0)

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
