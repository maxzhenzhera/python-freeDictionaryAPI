"""
Contains sync dictionary API client.

FOR WORK REQUIRE ``httpx`` PACKAGE TO BE INSTALLED.

.. class:: DictionaryApiClient(BaseDictionaryApiClient)
    Implements sync dictionary API client
"""

import contextlib
from http import HTTPStatus
import logging
from typing import (
    Any,
    Optional
)

import httpx

from .base_client import BaseDictionaryApiClient
from ..errors import (
    DictionaryApiError,
    API_ERRORS_MAPPER
)
from ..languages import (
    DEFAULT_LANGUAGE_CODE,
    LanguageCodes
)
from ..parsers import (
    DictionaryApiParser,
    DictionaryApiErrorParser
)
from ..types import Word
from ..urls import ApiUrl


__all__ = ['DictionaryApiClient']


logger = logging.getLogger(__name__)


class DictionaryApiClient(BaseDictionaryApiClient):
    """
    Implements sync dictionary API client.

    .. attrs:: _client httpx.Client: client for http requests

    .. property:: client(self) -> aiohttp.ClientSession

    .. method:: close(self) -> None
        Close client
    .. method:: _fetch_json(self, word: str, language_code: Optional[LanguageCodes] = None) -> Any
        Fetch API json response
    .. method:: fetch_parser(self, word: str, language_code: Optional[LanguageCodes] = None) -> DictionaryApiParser
        Fetch parser
    .. method:: fetch_word(self, word: str, language_code: Optional[LanguageCodes] = None) -> Word
        Fetch word (parsed object)
    """

    def __init__(self,
                 default_language_code: LanguageCodes = DEFAULT_LANGUAGE_CODE,
                 *,
                 client: Optional[httpx.Client] = None
                 ) -> None:
        """
        Init sync dictionary API client.

        :param default_language_code: default language of the searched words (by default English US)
        :type default_language_code: LanguageCodes

        :keyword client: client for sync requests
        :type client: httpx.Client

        :raises TypeError: raised if ``language_code`` is not instance of ``LanguageCodes``
        """

        super().__init__(default_language_code)

        if client:
            self._client = client
        else:
            self._client = httpx.Client()

            logger.debug(f'``httpx`` client has been created for sync client: {self._client!r}.')

        logger.info('Sync client has been successfully init-ed.')

    @property
    def client(self) -> httpx.Client:
        """ Get httpx client """
        return self._client

    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        return f'{class_name}(default_language_code={self._default_language_code!r})'

    def _fetch_json(self, word: str, language_code: Optional[LanguageCodes] = None) -> Any:
        """
        Fetch API json response.

        :param word: searched word
        :type word: str
        :param language_code: language of the searched word
        :type language_code: Optional[LanguageCodes]

        :return: json response (supposed to be ``list`` or ``dict``)
        :rtype: Any

        :raises ``DictionaryApiError`` and inherited errors: raised
            when unsuccessful status code got of API request
        """

        language_code = self._default_language_code if language_code is None else language_code
        url = ApiUrl(word, language_code=language_code).get_url()

        logger.info(f'Send request to API with url: {url!r}.')

        response: httpx.Response
        response = self._client.get(url)
        json_response = response.json()

        response_status_code = response.status_code
        if response_status_code != HTTPStatus.OK:
            # get error type by status code from error mapper
            # by default get common error
            error = API_ERRORS_MAPPER.get(response_status_code, DictionaryApiError)

            error_parser = DictionaryApiErrorParser(response_status_code, json_response)
            error_message = error_parser.get_formatted_error_message()

            logger.info(f'Response is !NOT! successful [code={response_status_code}] from url: {url}.')

            raise error(error_message)

        logger.info(f'Response is successful [code={response_status_code}] from url: {url}.')

        return json_response

    def fetch_parser(self, word: str, language_code: Optional[LanguageCodes] = None) -> DictionaryApiParser:
        """
        Fetch dictionary API parser.

        :param word: searched word
        :type word: str
        :param language_code: language of the searched word
        :type language_code: Optional[LanguageCodes]

        :return: dictionary API parser
        :rtype: DictionaryApiParser
        """

        json_response = self._fetch_json(word, language_code)
        parser = DictionaryApiParser(json_response)

        return parser

    def fetch_word(self, word: str, language_code: Optional[LanguageCodes] = None) -> Word:
        """
        Fetch word (parsed object that has all data fields as
        class attrs).
        Shortcut for ``DictionaryApiParser.word``.

        :param word: searched word
        :type word: str
        :param language_code: language of the searched word
        :type language_code: Optional[LanguageCodes]

        :return: word (parsed object)
        :rtype: Word
        """

        parser = self.fetch_parser(word, language_code)
        word = parser.word

        return word

    @classmethod
    @contextlib.contextmanager
    def manager(cls, *args, **kwargs) -> 'DictionaryApiParser':
        """
        Get context manager for parser client.
        Accepting all params from constructor.
        """

        client = cls(*args, **kwargs)
        try:
            yield client
        finally:
            client.close()

    def close(self) -> None:
        """ Close dictionary API client """
        self._client.close()

        logger.info('Client has been successfully closed.')
