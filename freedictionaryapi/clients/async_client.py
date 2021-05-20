"""
Contains async dictionary API client.

FOR WORK REQUIRE ``aiohttp`` PACKAGE TO BE INSTALLED.

.. class:: AsyncDictionaryApiClient(BaseDictionaryApiClient)
"""

import logging
from typing import (
    Any,
    Optional
)

import aiohttp

from .base_async_client import BaseAsyncDictionaryApiClient
from ..languages import (
    DEFAULT_LANGUAGE_CODE,
    LanguageCodes
)


__all__ = ['AsyncDictionaryApiClient']


logger = logging.getLogger(__name__)


class AsyncDictionaryApiClient(BaseAsyncDictionaryApiClient):
    """
    Implements asynchronous dictionary API client.

    Based on :obj:`aiohttp.ClientSession`.
    """

    def __init__(self, default_language_code: LanguageCodes = DEFAULT_LANGUAGE_CODE, *,
                 session: Optional[aiohttp.ClientSession] = None
                 ) -> None:
        """
        Init async dictionary API client instance.

        :param default_language_code: default language of the searched words for the client
        :type default_language_code: :obj:`LanguageCodes`
        :keyword session: ``aiohttp`` session to make HTTP requests asynchronously
        :type session: :obj:`Optional[aiohttp.ClientSession]`

        :raise:
            :TypeError:
                - if ``language_code`` is not an instance of :obj:`LanguageCodes`
                - if ``session`` is not an instance of :obj:`aiohttp.ClientSession`
        """

        super().__init__(default_language_code)

        if session:
            self._session = session

            if not isinstance(session, aiohttp.ClientSession):
                message = (
                    'For `session` has been passed object with unsupported type. '
                    'Expected to get argument with type <aiohttp.ClientSession>! '
                    f'Got (session={self._session!r})'
                )
                raise TypeError(message)
        else:
            self._session = aiohttp.ClientSession()

            logger.debug(f'``aiohttp.ClientSession`` session has been created for async API client: {self._session!r}.')

        logger.info('Async client has been successfully init-ed.')

    @property
    def session(self) -> aiohttp.ClientSession:
        """
        :return: session used for making HTTP requests
        :rtype: :obj:`aiohttp.ClientSession`
        """
        return self._session

    async def __aenter__(self) -> 'AsyncDictionaryApiClient':
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def fetch_api_response(self, url: str) -> tuple[int, Any]:
        """
        Fetch data of the API response.

        Implemented abstract method for ``async`` client with :obj:`aiohttp.ClientSession` usage.

        :param url: url that is generated by input params in invoked function
        :type url: :obj:`str`

        :return: tuple of
            - response status code;
            - python object loaded from API response with JSON decoding.
        :rtype: :obj:`tuple[int, Any]`
        """

        async with self._session.get(url) as response:
            response_status_code = response.status
            json_response = await response.json()

        data_of_the_api_response = (response_status_code, json_response)

        return data_of_the_api_response

    async def close(self) -> None:
        """
        Close dictionary API client

        :return: None
        :rtype: :obj:`None`
        """

        await self._session.close()

        logger.info('Client has been closed.')
