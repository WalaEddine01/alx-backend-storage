#!/usr/bin/env python3
"""Module to track URL access count and cache HTML content using Redis."""

import redis
import requests
from typing import Callable
from functools import wraps


# Global Redis client
r = redis.Redis()


def count_access(method: Callable) -> Callable:
    """
    Decorator to track how many times a URL has been accessed.

    Stores the count in Redis with key 'count:<url>'.
    """
    @wraps(method)
    def wrapper(url: str) -> str:
        r.incr(f"count:{url}")
        return method(url)
    return wrapper


@count_access
def get_page(url: str) -> str:
    """
    Retrieves the HTML content of a given URL.

    Caches the result for 10 seconds using Redis.
    Tracks how many times each URL was accessed.
    """
    cached = r.get(url)
    if cached:
        return cached.decode('utf-8')

    response = requests.get(url)
    html = response.text
    r.setex(url, 10, html)
    return html
