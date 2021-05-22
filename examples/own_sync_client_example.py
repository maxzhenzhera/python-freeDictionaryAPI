"""
Here we gonna create our own client
with one of web lib
that we, may be, want to use
instead of ready to use clients.

Used `requests` package for this goal.
"""

import logging
from typing import (
    Any,
    Optional
)

import requests

from freedictionaryapi.clients.base_sync_client import BaseDictionaryApiClient
# or `from freedictionaryapi.clients import BaseDictionaryApiClient`
from freedictionaryapi.errors import DictionaryApiError
# or `from freedictionaryapi import DictionaryApiError`
from freedictionaryapi.languages import (
    LanguageCodes,
    DEFAULT_LANGUAGE_CODE
)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


# So, lets implement:
# 1. simple class with requests
# 2. class with requests.Session


class SimpleOwnDictionaryApiClient(BaseDictionaryApiClient):

    def fetch_api_response(self, url: str) -> tuple[int, Any]:
        # implement abstract method
        # from docs we see
        # '''
        # ...
        # The most important part is returning - method must return tuple of:
        #     1. integer code of the API response;
        #     2. python object loaded from API response with JSON decoding.
        # ...
        # '''

        response = requests.get(url)
        response_status_code = response.status_code
        json_response = response.json()

        return (response_status_code, json_response)


class NotSoSimpleOwnDictionaryApiClient(BaseDictionaryApiClient):

    def __init__(self, default_language_code: LanguageCodes = DEFAULT_LANGUAGE_CODE, *,
                 session: Optional[requests.Session] = None) -> None:
        super().__init__(default_language_code)

        if session is None:
            self._session = requests.session()
        else:
            self._session = session

            if not isinstance(self._session, requests.Session):
                raise TypeError('I`m expecting to get session with `requests.Session` type...')

    def __enter__(self) -> 'NotSoSimpleOwnDictionaryApiClient':
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

        logger.info('Session has been closed')

    def fetch_api_response(self, url: str) -> tuple[int, Any]:
        # implement abstract method
        # from docs we see
        # '''
        # ...
        # The most important part is returning - method must return tuple of:
        #     1. integer code of the API response;
        #     2. python object loaded from API response with JSON decoding.
        # ...
        # '''

        response = self._session.get(url)
        response_status_code = response.status_code
        json_response = response.json()

        return (response_status_code, json_response)

    def close(self) -> None:
        self._session.close()


def main():
    # lets test our clients

    # # simple one
    simple_client = SimpleOwnDictionaryApiClient()
    word = ' tests '
    print('{:*^20}'.format(word))
    try:
        parser = simple_client.fetch_parser(word)
    except DictionaryApiError:
        logger.error('API error')
    else:
        print(f'Definitions: {parser.get_all_definitions()!r}')

    # # and not so simple one
    with NotSoSimpleOwnDictionaryApiClient() as not_so_simple_client:
        word = ' program '
        print('{:*^20}'.format(word))
        try:
            parser = not_so_simple_client.fetch_parser(word)
        except DictionaryApiError:
            logger.error('API error')
        else:
            print(f'Definitions: {parser.get_all_definitions()!r}')


if __name__ == '__main__':
    main()
