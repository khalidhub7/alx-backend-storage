#!/usr/bin/env python3
"""
implementing an expiring web cache and tracker
"""
import requests
from typing import Callable
from functools import wraps


def count_requests(
        method: Callable) -> Callable:
    """
count requests decorator
    """
    @wraps(method)
    def wrapper(url: str) -> str:
        """ wrapper function """
        r = method.__self__._redis
        r.incr("count:{}"
               .format(str(url)))
        cached_html = r.get(
            "cached:{}".format(str(url)))
        if cached_html:
            return cached_html.decode(
                'utf-8')
        html = method(str(url)).decode(
            'utf-8')
        r.setex("cached:{}"
                .format(url), 10, html)
        return r.get(
            "cached:{}".format(str(url))
        ).decode('utf-8')
    return wrapper


@count_requests
def get_page(url: str) -> str:
    """ get page """
    r = requests.get(url)
    return r.text.decode(
        'utf-8')
