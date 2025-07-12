#!/usr/bin/env python3
"""Module to track URL access count and cache HTML content using Redis."""

import redis
import requests
from functools import wraps
from urllib.parse import quote, unquote

# Global Redis client
r = redis.Redis()

def count_access(method):
    """Decorator to track how many times a URL has been accessed."""

    @wraps(method)
    def wrapper(url: str) -> str:
        # Encode URL safely for Redis key
        safe_url = quote(url, safe='')
        r.incr(f"count:{safe_url}")
        return method(url)
    return wrapper

def cache_page(expire=10):
    """Decorator to cache page content in Redis with expiration."""

    def decorator(method):
        @wraps(method)
        def wrapper(url: str) -> str:
            safe_url = quote(url, safe='')
            cached = r.get(f"cache:{safe_url}")
            if cached:
                return cached.decode('utf-8')

            result = method(url)
            r.setex(f"cache:{safe_url}", expire, result)
            return result

        return wrapper

    return decorator

@count_access
@cache_page(expire=10)
def get_page(url: str) -> str:
    """Retrieve HTML content from URL, cache it, and track access count."""
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.text
