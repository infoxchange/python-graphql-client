"""Caches for the GraphQL client."""

from .base import BaseCache
from .dict import DictionaryCache

__all__ = (
    'BaseCache',
    'DictionaryCache',
)
