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

from .base_client import BaseDictionaryApiClient
from ..languages import (
    DEFAULT_LANGUAGE_CODE,
    LanguageCodes
)
from ..parsers import DictionaryApiParser
from ..types import Word


__all__ = ['AsyncDictionaryApiClient']


logger = logging.getLogger(__name__)


class AsyncDictionaryApiClient(BaseDictionaryApiClient):
    """
    Implements async dictionary API client.
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

        :raises TypeError:
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
        """ :obj:`aiohttp.ClientSession` used for making HTTP requests """
        return self._session

    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        return f'{class_name}(default_language_code={self._default_language_code!r})'

    async def __aenter__(self) -> 'AsyncDictionaryApiClient':
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def fetch_json(self, word: str, language_code: Optional[LanguageCodes] = None) -> Any:
        """
        Fetch API json response that loaded in Python object (``response.json()``).

        :param word: searched word
        :type word: :obj:`str`
        :param language_code: language of the searched word
        :type language_code: :obj:`Optional[LanguageCodes]`

        :return: json response (supposed to be ``list`` or ``dict``)
        :rtype: :obj:`Any`

        :raises :obj:`DictionaryApiError`` and inherited errors: raised
            when unsuccessful status code got of API request
        """

        url, language_code = self._generate_url(word, language_code)

        logger.info(f'Send request to API with word: <{word!r}> and language code: <{language_code!r}>. URL: {url!r}.')

        response: aiohttp.ClientResponse
        async with self._session.get(url) as response:
            json_response = await response.json()

        # logging - handling of API errors (and raising them)
        analyzed_response = self._analyze_response(url, response.status, json_response)

        return analyzed_response

    async def fetch_parser(self, word: str, language_code: Optional[LanguageCodes] = None) -> DictionaryApiParser:
        """
        Fetch dictionary API parser.

        :param word: searched word
        :type word: :obj:`str`
        :param language_code: language of the searched word (`word`)
        :type language_code: :obj:`Optional[LanguageCodes]`

        :return: dictionary API parser
        :rtype: :obj:`DictionaryApiParser`
        """

        json_response = await self.fetch_json(word, language_code)
        parser = DictionaryApiParser(json_response)

        return parser

    async def fetch_word(self, word: str, language_code: Optional[LanguageCodes] = None) -> Word:
        """
        Fetch word (:obj:`Word`) - parsed object that has all word info.
        Shortcut for the :obj:`DictionaryApiParser.word`.

        :param word: searched word
        :type word: :obj:`str`
        :param language_code: language of the searched word
        :type language_code: :obj:`Optional[LanguageCodes]`

        :return: word (parsed object)
        :rtype: :obj:`Word`
        """

        parser = await self.fetch_parser(word, language_code)
        word = parser.word

        return word

    async def close(self) -> None:
        """ Close dictionary API client """
        await self._session.close()

        logger.info('Client has been closed.')
