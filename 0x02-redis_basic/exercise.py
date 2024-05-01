#!/usr/bin/env python3
"""
This Module contains the Cache class to store data in redis
"""
import uuid
import redis
from typing import Union


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
