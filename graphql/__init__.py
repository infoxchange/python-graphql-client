"""Class to handle GraphQL request."""

import json

import requests

from .caches import BaseCache

class GraphQLClient:
    """A client for sending requests to GraphQL."""

    def __init__(self, endpoint, verify_ssl=True, cache=None):
        """Initialise a new client."""
        self.endpoint = endpoint
        self.token = None
        self.header_name = 'Authorization'
        self.header_name = None
        self.verify_ssl = verify_ssl

        if cache and not isinstance(cache, BaseCache):
            raise ValueError('The cache must be an instance of BaseCache.')

        self.cache = cache

    def add_token(self, token, header_name='Authorization'):
        """Add an authentication token to requests."""
        self.token = token
        self.header_name = header_name
    
    def clear_token(self):
        """Clear an authentication token."""
        self.token = None
        self.header_name = None

    def query(self, query, variables=None, force_request=False):
        """Send a query to the GraphL server."""

        body = {
            'query': query,
        }

        if variables:
            body.update({
                'variables': variables
            })

        if not force_request and self.cache and self.cache.check({'body': body, 'auth': self.token}):
            return self.cache.read({'body': body, 'auth': self.token})

        headers = {}
        if self.token:
            headers.update({
                self.header_name: self.token
            })

        res = requests.post(
            self.endpoint,
            json=body,
            headers=headers,
            verify=self.verify_ssl,
        )
        data = res.json()

        if self.cache:
            self.cache.write({'body': body, 'auth': self.token}, data)

        return data
