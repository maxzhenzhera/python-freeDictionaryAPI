"""
Contains base dictionary API client.

.. class:: BaseDictionaryApiClient(abc.ABC)
"""

import abc
import logging
from http import HTTPStatus
from typing import (
    Any,
    Optional,
    Union
)

from ..errors import (
    API_ERRORS_MAPPER,
    DictionaryApiError
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


__all__ = ['BaseDictionaryApiClient']


logger = logging.getLogger(__name__)


class BaseDictionaryApiClient(abc.ABC):
    """
    Base dictionary API client.
    Abstract client that supposed to be inherited
    for ``sync`` and ``async`` clients.
    """

    def __init__(self, default_language_code: LanguageCodes = DEFAULT_LANGUAGE_CODE) -> None:
        """
        Init base dictionary API client instance.

        :param default_language_code: default language of the searched words for the client
        :type default_language_code: :obj:`LanguageCodes`

        :raises TypeError: if has been passed unsupported ``default_language_code``
        """

        self._default_language_code = default_language_code

        if not isinstance(self._default_language_code, LanguageCodes):
            message = (
                'For `language_code` has been passed object with unsupported type. '
                'Expected to get argument with type `freedictionaryapi.languages.LanguageCodes`! '
                f'Got (language_code={self._default_language_code!r})'
            )
            raise TypeError(message)

    @property
    def default_language_code(self) -> LanguageCodes:
        """ Default client language code """
        return self._default_language_code

    @staticmethod
    def _analyze_response(url: str, status_code: int, response: Union[dict, list]) -> Union[dict, list]:
        """
        Analyze API response.

        Do this:
            - log about response status (successful | unsuccessful);
            - raise correspond error if response is not successful.

        :param url: URL that generated for API request
        :type url: :obj:`str`
        :param status_code: response status code
        :type status_code: :obj:`int`
        :param response: API response that loaded in python object
        :type response: :obj:`Union[dict, list]`

        :return: passed response
        :rtype: :obj:`Union[dict, list]`

        :raises :obj:`DictionaryApiError` and inherited errors: if response has unsuccessful status code
        """

        if status_code != HTTPStatus.OK:
            # get error type by status code from error mapper
            # by default get common error
            error = API_ERRORS_MAPPER.get(status_code, DictionaryApiError)

            error_parser = DictionaryApiErrorParser(status_code, response)
            error_message = error_parser.get_formatted_error_message()

            logger.info(f'Response is not successful [code={status_code!r}] from url: {url!r}.')

            raise error(error_message)

        logger.info(f'Response is successful [code={status_code}] from url: {url}.')

        return response

    def _generate_url(self, word: str, language_code: Optional[LanguageCodes] = None) -> tuple[str, LanguageCodes]:
        """
        Generate URL for API request.

        :param word: searched word
        :type word: :obj:`str`
        :param language_code: language of the searched word
        :type language_code: :obj:`Optional[LanguageCodes]`

        :return: tuple of generated URL and used language code
        :rtype: :obj:`Union[str, LanguageCodes]`
        """

        language_code: LanguageCodes = self._default_language_code if language_code is None else language_code
        url = ApiUrl(word, language_code=language_code).get_url()

        return (url, language_code)

    @abc.abstractmethod
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

    @abc.abstractmethod
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

    @abc.abstractmethod
    def fetch_word(self, word: str, language_code: Optional[LanguageCodes] = None) -> Word:
        """
        Fetch word (:obj:`Word`) - parsed object that has all word info.
        Shortcut for the ``word`` property  of the :obj:`DictionaryApiParser` (``DictionaryApiParser.word``).

        :param word: searched word
        :type word: :obj:`str`
        :param language_code: language of the searched word
        :type language_code: :obj:`Optional[LanguageCodes]`

        :return: word (parsed object)
        :rtype: :obj:`Word`
        """
