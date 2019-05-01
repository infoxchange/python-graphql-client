"""GraphQL client exceptions."""

class CacheError(Exception):
    """An error with the cache."""

    def __init__(self, message):
        """Initialise a new exception."""
        self.message = message
