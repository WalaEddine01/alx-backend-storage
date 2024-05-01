#!/usr/bin/env python3
"""
This Module contains the Cache class to store data in redis
"""
import uuid
import redis
from functools import wraps
from typing import Union, Optional, Callable


def call_history(method: Callable) -> Callable:
    """
    Decorator to store the inputs and outputs of a method in redis
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function to store the inputs and outputs
        """
        inputs_key = f"{method.__qualname__}:inputs"
        outputs_key = f"{method.__qualname__}:outputs"

        self._redis.rpush(inputs_key, str(args))
        result = method(self, *args, **kwargs)
        self._redis.rpush(outputs_key, str(result))

        return result
    return wrapper


def count_calls(method: Callable) -> Callable:
    """
    Decorator to count the number of calls to a method
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function to count the number of calls
        """
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


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
