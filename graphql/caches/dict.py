"""A dictionary cache for the GraphQL client."""

from hashlib import sha1
from json import dumps as json_dumps

from .base import BaseCache
from graphql.exceptions import CacheError


class DictionaryCache(BaseCache):
    """A cache that uses an in-memory dictionary."""

    cache = {} 

    def generate_key(self, body):
        return sha1(json_dumps(body).encode()).hexdigest()

    def check(self, req):
        """Check if a key exists in the dictionary."""
        return self.generate_key(req) in self.cache

    def read(self, req):
        """Read a value from the cache."""
        try:
            return self.cache[self.generate_key(req)]
        except KeyError:
            raise CacheError("Key doesn't exist in cache.")

    def write(self, req, data):
        """Write a value to the cache."""
        self.cache[self.generate_key(req)] = data
