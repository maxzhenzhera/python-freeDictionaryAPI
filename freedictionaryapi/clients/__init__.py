"""
Contains clients for interacting with API.

Available as synchronous as asynchronous clients.

Also it is possible to inherit one of base classes
(``sync`` or ``async``) and implement
own client.

Async client is powered with ``aiohttp``.
Since ``aiohttp`` used in all asynchronous frameworks and libraries:
client works on-top of ``aiohttp``.

Synchronous client is powered with ``httpx`.
Since ``httpx`` is modern and powerful HTTP client:
client works on-top of ``httpx``.
"""

from .base_client_interface import BaseDictionaryApiClientInterface
from .base_async_client import BaseAsyncDictionaryApiClient
from .base_sync_client import BaseDictionaryApiClient

# modules require external dependencies !!!!!!!!!!!!!!!
# from .async_client import AsyncDictionaryApiClient
# from .sync_client import DictionaryApiClient
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


__all__ = [
    # base abstract classes
    # # that inherited in classes below
    'BaseDictionaryApiClientInterface',
    # # that might be inherited manually
    'BaseAsyncDictionaryApiClient',
    'BaseDictionaryApiClient',
]
