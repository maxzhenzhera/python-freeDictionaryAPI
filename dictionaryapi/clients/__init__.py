"""
Contains clients for interacting with API.

Available as sync as async clients.

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