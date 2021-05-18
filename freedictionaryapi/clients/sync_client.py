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

from .base_client import BaseDictionaryApiClient
from ..languages import (
    DEFAULT_LANGUAGE_CODE,
    LanguageCodes
)
from ..parsers import DictionaryApiParser
from ..types import Word


__all__ = ['DictionaryApiClient']


logger = logging.getLogger(__name__)


class DictionaryApiClient(BaseDictionaryApiClient):
    """
    Implements sync dictionary API client.
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

        :raises TypeError:
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

    @property
    def client(self) -> httpx.Client:
        """ :obj:`httpx.Client` used for making HTTP requests """
        return self._client

    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        return f'{class_name}(default_language_code={self._default_language_code!r})'

    def __enter__(self) -> 'DictionaryApiClient':
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def fetch_json(self, word: str, language_code: Optional[LanguageCodes] = None) -> Any:
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

        logger.info(f'Send request to API with word <{word!r}> and language code: <{language_code!r}>. URL: {url!r}.')

        response = self._client.get(url)
        json_response = response.json()

        # logging - handling of API errors (and raising them)
        analyzed_response = self._analyze_response(url, response.status_code, json_response)

        return analyzed_response

    def fetch_parser(self, word: str, language_code: Optional[LanguageCodes] = None) -> DictionaryApiParser:
        """
        Fetch dictionary API parser.

        :param word: searched word
        :type word: :obj:`str`
        :param language_code: language of the searched word (`word`)
        :type language_code: :obj:`Optional[LanguageCodes]`

        :return: dictionary API parser
        :rtype: :obj:`DictionaryApiParser`
        """

        json_response = self.fetch_json(word, language_code)
        parser = DictionaryApiParser(json_response)

        return parser

    def fetch_word(self, word: str, language_code: Optional[LanguageCodes] = None) -> Word:
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

        parser = self.fetch_parser(word, language_code)
        word = parser.word

        return word

    def close(self) -> None:
        """ Close dictionary API client """
        self._client.close()

        logger.info('Client has been closed.')
