#!/usr/bin/env python3
"""
This Module contains the Cache class to store data in redis
"""
import requests
import uuid
import redis
from functools import wraps
from typing import Union, Optional, Callable


def replay(redis_client: redis.Redis, method: Callable) -> None:
    """
    Display the history of calls of a particular function
    """
    inputs_key = f"{method.__qualname__}:inputs"
    outputs_key = f"{method.__qualname__}:outputs"

    inputs = redis_client.lrange(inputs_key, 0, -1)
    outputs = redis_client.lrange(outputs_key, 0, -1)

    print(f"History of calls for function {method.__qualname__}:")
    for input_data, output_data in zip(inputs, outputs):
        print(f"Input: {input_data.decode()} - Output: {output_data.decode()}")


def count_calls(method: Callable) -> Callable:
    """
    Decorator to count the number of calls to a method
    """
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """wrap the decorated function and return the wrapper"""
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """store the history of inputs and outputs for a particular function"""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """wrap the decorated function and return the wrapper"""
        input_data = str(args)
        self._redis.rpush(method.__qualname__ + ":inputs", input_data)
        output_data = str(method(self, *args, **kwargs))
        self._redis.rpush(method.__qualname__ + ":outputs", output_data)
        return output_data
    return wrapper


def cache_page(timeout=10):
    """
    Decorator to cache the content of a webpage
    """
    def decorator(func):
        """
        Decorator to cache the content of a webpage
        """
        @wraps(func)
        def wrapper(*args, **kwargs):
            """
            Wrapper function to cache the content of a webpage
            """
            url = args[0]
            key = f"cache:{url}"
            redis_client = redis.Redis()
            cached_content = redis_client.get(key)
            if cached_content:
                return cached_content.decode('utf-8')
            else:
                content = func(*args, **kwargs)
                redis_client.setex(key, timeout, content)
                return content
        return wrapper
    return decorator


@count_calls
@cache_page()
def get_page(url):
    """
    Get the content of a webpage
    """
    response = requests.get(url)
    return response.text


class Cache:
    """
    Cache class to store data in redis
    """
    def __init__(self):
        """
        Initialize the redis connection
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store data in redis
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None)\
            -> Union[str, bytes, int, float, None]:
        """
        Get data from redis
        """
        data = self._redis.get(key)
        if data is None:
            return None
        if fn is not None:
            return fn(data)
        return data

    def get_str(self, key: str) -> Optional[str]:
        """
        Get data from redis as string
        """
        return self.get(key, lambda x: x.decode("utf-8"))

    def get_int(self, key: str) -> Optional[int]:
        """
        Get data from redis as integer
        """
        return self.get(key, lambda x: int(x))
