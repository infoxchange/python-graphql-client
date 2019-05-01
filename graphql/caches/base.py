"""The base cache class."""

from abc import ABC, abstractmethod


class BaseCache(ABC):
    """The base class for GraphQL client caches."""
    
    @abstractmethod
    def check(self, req):
        """Check if a key exists in the cache."""
        pass

    @abstractmethod
    def read(self, req):
        """Read a value from the cache."""
        pass

    @abstractmethod
    def write(self, req, data):
        """Write a value to the cache."""
        pass
