"""
Contains clients for interacting with API.

Available as sync as async clients.

Also it is possible to inherit one of base classes
(``sync`` or ``async``) and implement
own client.

Async client is powered with ``aiohttp``.
Since ``aiohttp`` used in all async frameworks and libraries
client works on-top of ``aiohttp``.

Sync client is powered with ``httpx`.
Since ``httpx`` is modern and powerful http client
client works on-top of ``httpx``.

Yes, ``httpx`` also provides async support
but
``aiohttp`` used more often in async projects.
"""

from .base_client_interface import BaseDictionaryApiClientInterface
from .base_async_client import BaseAsyncDictionaryApiClient
from .base_sync_client import BaseDictionaryApiClient
from .async_client import AsyncDictionaryApiClient
from .sync_client import DictionaryApiClient


__all__ = [
    # base abstract classes
    # # that inherited in classes below
    'BaseDictionaryApiClientInterface',
    # # that might be inherited manually
    'BaseAsyncDictionaryApiClient',
    'BaseDictionaryApiClient',
    # prepared clients (sync and async)
    'AsyncDictionaryApiClient',
    'DictionaryApiClient'
]
