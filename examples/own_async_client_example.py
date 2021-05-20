"""
Here we gonna create our own client
with one of web lib
that we, may be, want to use
instead of ready to use clients.

Used `httpx` package for this goal.
"""

import asyncio
import logging
from typing import (
    Any,
    Optional
)

import httpx

from freedictionaryapi.errors import DictionaryApiError
from freedictionaryapi.clients import BaseAsyncDictionaryApiClient
from freedictionaryapi.languages import (
    LanguageCodes,
    DEFAULT_LANGUAGE_CODE
)


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


# So, lets implement:
# (simple class with requests but without __init__ changing check example for ``sync`` client)
# 1. class with httpx.AsyncClient


class NotSoSimpleOwnDictionaryApiClient(BaseAsyncDictionaryApiClient):

    def __init__(self, default_language_code: LanguageCodes = DEFAULT_LANGUAGE_CODE, *,
                 client: Optional[httpx.AsyncClient] = None) -> None:
        super().__init__(default_language_code)

        if client is None:
            self._client = httpx.AsyncClient()
        else:
            self._session = client

            if not isinstance(self._client, httpx.AsyncClient):
                raise TypeError('I`m expecting to get client with `httpx.AsyncClient` type...')

    async def __aenter__(self) -> 'NotSoSimpleOwnDictionaryApiClient':
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def fetch_api_response(self, url: str) -> tuple[int, Any]:
        # implement abstract method
        # from docs we see
        # '''
        # ...
        # The most important part is returning - method must return tuple of:
        #     1. integer code of the API response;
        #     2. python object loaded from API response with JSON decoding.
        # ...
        # '''

        response = await self._client.get(url)
        response_status_code = response.status_code
        json_response = response.json()

        return (response_status_code, json_response)

    async def close(self) -> None:
        await self._client.aclose()

        logger.info('Client has been closed')


async def main():
    # lets test our client

    # # not so simple one
    async with NotSoSimpleOwnDictionaryApiClient() as not_so_simple_client:
        word = ' program '
        print('{:*^20}'.format(word))
        try:
            parser = await not_so_simple_client.fetch_parser(word)
        except DictionaryApiError:
            logger.error('API error')
        else:
            print(f'Definitions: {parser.get_all_definitions()!r}')


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
