"""
Contains base dictionary API client interface.

.. class:: BaseDictionaryApiClientInterface(abc.ABC)
"""

import abc
import logging
from http import HTTPStatus
import typing

from ..errors import (
    API_ERRORS_MAPPER,
    DictionaryApiError
)
from ..languages import (
    DEFAULT_LANGUAGE_CODE,
    LanguageCodes
)
from ..parsers import DictionaryApiErrorParser
from ..urls import ApiUrl


__all__ = ['BaseDictionaryApiClientInterface']


logger = logging.getLogger(__name__)


class BaseDictionaryApiClientInterface(abc.ABC):
    """
    Base dictionary API client interface.

    Abstract client interface that supposed to be inherited
    for ``sync`` and ``async`` **base** clients.

    Here, interface:
        Class that implements some useful API
        and makes sense in inheritance
        for other base clients
        that also must implement this base API
        but also provide some specific
        such concrete abstract methods.

    So, for implementing of ``sync`` and ``async`` base clients
    base API is not repeated in code
    but provided with inheritance from this interface.
    """

    def __init__(self, default_language_code: LanguageCodes = DEFAULT_LANGUAGE_CODE) -> None:
        """
        Init base dictionary API client instance.

        :param default_language_code: default language of the searched words for the client
        :type default_language_code: :obj:`LanguageCodes`

        :raise:
            :TypeError: if has been passed unsupported ``default_language_code``
        """

        self._default_language_code = default_language_code

        if not isinstance(self._default_language_code, LanguageCodes):
            message = (
                'For `language_code` has been passed object with unsupported type. '
                'Expected to get argument with type `freedictionaryapi.languages.LanguageCodes`! '
                f'Got (language_code={self._default_language_code!r})'
            )
            raise TypeError(message)

    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        return f'{class_name}(default_language_code={self._default_language_code!r})'

    @property
    def default_language_code(self) -> LanguageCodes:
        """
        :return: default client language code
        :rtype: :obj:`LanguageCodes`
        """
        return self._default_language_code

    @staticmethod
    def _analyze_response(url: str, status_code: int, response: typing.Union[dict, list]) -> typing.Union[dict, list]:
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

        :raise:
            :DictionaryApiError: when unsuccessful status code got of API request
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

    def _generate_url(self, word: str, language_code: typing.Optional[LanguageCodes] = None
                      ) -> typing.Tuple[str, LanguageCodes]:
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
