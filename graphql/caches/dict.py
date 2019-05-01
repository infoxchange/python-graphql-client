"""A dictionary cache for the GraphQL client."""

from datetime import datetime, timedelta
from hashlib import sha1
from json import dumps as json_dumps

from .base import BaseCache
from graphql.exceptions import CacheError


class DictionaryCache(BaseCache):
    """A cache that uses an in-memory dictionary."""

    cache = {}

    def __init__(self, timeout=15):
        """Initialise the cache."""
        self.timeout = timeout

    def generate_key(self, body):
        """Generate a key based on the GraphQL request."""
        return sha1(json_dumps(body).encode()).hexdigest()

    def check_valid_cache(self, key):
        """Check if an item in the cache has expired."""
        try:
            return self.cache[key]['timeout'] > datetime.now()
        except KeyError:
            return False

    def check(self, req):
        """Check if a key exists in the dictionary."""
        key = self.generate_key(req)
        return key in self.cache and self.check_valid_cache(key)

    def read(self, req):
        """Read a value from the cache."""
        key = self.generate_key(req)
        try:
            if self.check_valid_cache(key):
                return self.cache[key]['data']

            del self.cache[key]
            return None
        except KeyError:
            raise CacheError("Key doesn't exist in cache.")

    def write(self, req, data):
        """Write a value to the cache."""
        self.cache[self.generate_key(req)] = {
            'data': data,
            'timeout': datetime.now() + timedelta(minutes=self.timeout)
        }
