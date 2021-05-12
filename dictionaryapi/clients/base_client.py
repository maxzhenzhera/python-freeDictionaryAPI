"""
Contains base dictionary API client.

.. class:: BaseDictionaryApiClient(abc.ABC)
    Abstract client that supposed to be inherited for ``sync`` and ``async`` clients
"""

import abc
from typing import (
    Any,
    Optional
)

from ..languages import (
    DEFAULT_LANGUAGE_CODE,
    LanguageCodes
)


__all__ = ['BaseDictionaryApiClient']


class BaseDictionaryApiClient(abc.ABC):
    """
    Base dictionary API client.
    Abstract client that supposed to be inherited
    for ``sync`` and ``async`` clients.

    .. attrs:: _default_language_code LanguageCodes: default language for searched words

    .. property:: default_language_code(self) -> LanguageCodes

    .. abstractmethod:: _fetch_json(self, word: str, language_code: Optional[LanguageCodes] = None) -> Any
        Fetch API json response that loaded in Python object (``response.json()``).
    """

    def __init__(self, default_language_code: LanguageCodes = DEFAULT_LANGUAGE_CODE) -> None:
        """
        Init base dictionary API client.

        :param default_language_code: default language of the searched words (by default English US)
        :type default_language_code: LanguageCodes
        """

        self._default_language_code = default_language_code

        if not isinstance(default_language_code, LanguageCodes):
            message = (
                'For ``language_code`` has passed unsupported type. '
                'Expected to get argument with type ``LanguageCodes``! '
                f'Got (language_code={self._default_language_code!r})'
            )
            raise TypeError(message)

    @property
    def default_language_code(self) -> LanguageCodes:
        """ Get default language code """
        return self._default_language_code

    @abc.abstractmethod
    def _fetch_json(self, word: str, language_code: Optional[LanguageCodes] = None) -> Any:
        """
        Fetch API json response that loaded in Python object (``response.json()``).

        :param word: searched word
        :type word: str
        :param language_code: language of the searched word
        :type language_code: Optional[LanguageCodes]

        :return: json response (supposed to be ``list`` or ``dict``)
        :rtype: Any

        :raises ``DictionaryApiError`` and inherited errors: raised
            when unsuccessful status code got of API request
        """

    @classmethod
    @abc.abstractmethod
    def manager(cls, *args, **kwargs):
        """ Get context manager for parser client """
