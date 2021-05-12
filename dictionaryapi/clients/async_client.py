"""
Contains async dictionary API client.

FOR WORK REQUIRE ``aiohttp`` PACKAGE TO BE INSTALLED.

.. class:: AsyncDictionaryApiClient(BaseDictionaryApiClient)
    Implements async dictionary API client
"""

import contextlib
from http import HTTPStatus
import logging
from typing import (
    Any,
    Optional
)

import aiohttp

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


__all__ = ['AsyncDictionaryApiClient']


logger = logging.getLogger(__name__)


class AsyncDictionaryApiClient(BaseDictionaryApiClient):
    """
    Implements async dictionary API client.

    .. attrs:: _session aiohttp.ClientSession: session for http requests

    .. property:: session(self) -> aiohttp.ClientSession

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
                 session: Optional[aiohttp.ClientSession] = None
                 ) -> None:
        """
        Init async dictionary API client.

        :param default_language_code: default language of the searched words (by default English US)
        :type default_language_code: LanguageCodes

        :keyword session: session for async requests
        :type session: aiohttp.ClientSession

        :raises TypeError: raised if ``language_code`` is not instance of ``LanguageCodes``
        """

        super().__init__(default_language_code)

        if session:
            self._session = session
        else:
            self._session = aiohttp.ClientSession()

            logger.debug(f'``aiohttp`` client session has been created for async client: {self._session!r}.')

        logger.info('Async client has been successfully init-ed.')

    @property
    def session(self) -> aiohttp.ClientSession:
        """ Get aiohttp session """
        return self._session

    def __repr__(self) -> str:
        return f'AsyncDictionaryApiClient(default_language_code={self._default_language_code!r})'

    async def _fetch_json(self, word: str, language_code: Optional[LanguageCodes] = None) -> Any:
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

        response: aiohttp.ClientResponse
        async with self._session.get(url) as response:
            json_response = await response.json()

        response_status_code = response.status
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

    async def fetch_parser(self, word: str, language_code: Optional[LanguageCodes] = None) -> DictionaryApiParser:
        """
        Fetch dictionary API parser.

        :param word: searched word
        :type word: str
        :param language_code: language of the searched word
        :type language_code: Optional[LanguageCodes]

        :return: dictionary API parser
        :rtype: DictionaryApiParser
        """

        json_response = await self._fetch_json(word, language_code)
        parser = DictionaryApiParser(json_response)

        return parser

    async def fetch_word(self, word: str, language_code: Optional[LanguageCodes] = None) -> Word:
        """
        Fetch word (parsed object that has all word info).
        Shortcut for ``DictionaryApiParser.word``.

        :param word: searched word
        :type word: str
        :param language_code: language of the searched word
        :type language_code: Optional[LanguageCodes]

        :return: word (parsed object)
        :rtype: Word
        """

        parser = await self.fetch_parser(word, language_code)
        word = parser.word

        return word

    @classmethod
    @contextlib.asynccontextmanager
    async def manager(cls, *args, **kwargs) -> 'DictionaryApiParser':
        """
        Get context manager for parser client.
        Accepting all params from constructor.
        """

        client = cls(*args, **kwargs)
        try:
            yield client
        finally:
            await client.close()

    async def close(self) -> None:
        """ Close dictionary API client """
        await self._session.close()

        logger.info('Client has been successfully closed.')
