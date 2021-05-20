"""
Contains sync dictionary API client.

FOR WORK REQUIRE ``httpx`` PACKAGE TO BE INSTALLED.

.. class:: DictionaryApiClient(BaseDictionaryApiClient)
"""

import logging
from typing import (
    Any,
    Optional
)

import httpx

from .base_sync_client import BaseDictionaryApiClient
from ..languages import (
    DEFAULT_LANGUAGE_CODE,
    LanguageCodes
)


__all__ = ['DictionaryApiClient']


logger = logging.getLogger(__name__)


class DictionaryApiClient(BaseDictionaryApiClient):
    """
    Implements sync dictionary API client.

    Based on :obj:`httpx.Client`.
    """

    def __init__(self, default_language_code: LanguageCodes = DEFAULT_LANGUAGE_CODE, *,
                 client: Optional[httpx.Client] = None
                 ) -> None:
        """
        Init sync dictionary API client instance.

        :param default_language_code: default language of the searched words for the client
        :type default_language_code: LanguageCodes
        :keyword client: ``httpx`` client to make HTTP requests
        :type client: :obj:`Optional[httpx.Client]`

        :raise:
            :TypeError:
                - if ``language_code`` is not an instance of :obj:`LanguageCodes`
                - if ``client`` is not an instance of :obj:`httpx.Client`
        """

        super().__init__(default_language_code)

        if client:
            self._client = client

            if not isinstance(self._client, httpx.Client):
                message = (
                    'For `client` has been passed object with unsupported type. '
                    'Expected to get argument with type <httpx.Client>! '
                    f'Got (client={self._client!r})'
                )
                raise TypeError(message)
        else:
            self._client = httpx.Client()

            logger.debug(f'``httpx.Client`` client has been created for sync dictionary API client: {self._client!r}.')

        logger.info('Client has been init-ed.')

    def fetch_api_response(self, url: str) -> tuple[int, Any]:
        """
        Fetch data of the API response.

        Implemented abstract method for ``sync`` client with :obj:`httpx.Client` usage.

        :param url: url that is generated by input params in invoked function
        :type url: :obj:`str`

        :return: tuple of
            - response status code;
            - python object loaded from API response with JSON decoding.
        :rtype: :obj:`tuple[int, Any]`
        """

        response = self._client.get(url)

        response_status_code = response.status_code
        json_response = response.json()

        data_of_the_api_response = (response_status_code, json_response)

        return data_of_the_api_response

    @property
    def client(self) -> httpx.Client:
        """
        :return: client used for making HTTP requests
        :rtype: :obj:`httpx.Client`
        """

        return self._client

    def __enter__(self) -> 'DictionaryApiClient':
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self) -> None:
        """
        Close dictionary API client

        :return: None
        :rtype: :obj:`None`
        """

        self._client.close()

        logger.info('Client has been closed.')
