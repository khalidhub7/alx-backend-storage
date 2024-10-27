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
    def wrapper(url: str) -> Callable:
        """ wrapper function """
        r = method.__self__._redis
        r.incr("count:{}"
               .format(str(url)))
        cached_html = r.get(
            str("cached:{}".format(str(url))))
        if cached_html:
            return str(cached_html.decode(
                'utf-8'))
        html = str(method(str(url)).decode(
            'utf-8'))
        r.setex("cached:{}"
                .format(str(url)), 10, html)
        return str(r.get(
            "cached:{}".format(str(url))
        ).decode('utf-8'))
    return wrapper


@count_requests
def get_page(url: str) -> str:
    """ get page """
    r = requests.get(str(url))
    return str(r.text.decode(
        'utf-8'))
