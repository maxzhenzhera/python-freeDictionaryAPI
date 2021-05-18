"""
Contains class for work with API urls.

.. class:: ApiUrl
    Implements work with API urls. To get needed for request url - init instance and invoke .get_url() method.
"""

import logging

from .languages import (
    DEFAULT_LANGUAGE_CODE,
    LanguageCodes
)


__all__ = ['ApiUrl']


logger = logging.getLogger(__name__)


class ApiUrl:
    """
    Implements API url object.

    .. attr:: API_URL_PATTERN

    .. property:: word(self) -> str
    .. property:: language_code(self) -> LanguageCodes

    .. method:: get_url(self) -> str
        Get API url to request
    """

    # pattern:
    # https://api.dictionaryapi.dev/api/v2/entries/<language_code>/<word>

    # Note: ``API_URL_PATTERN`` is a format string!
    API_URL_PATTERN = 'https://api.dictionaryapi.dev/api/v2/entries/{language_code}/{word}'

    # example:
    # https://api.dictionaryapi.dev/api/v2/entries/en_US/hello

    def __init__(self, word: str, *, language_code: LanguageCodes = DEFAULT_LANGUAGE_CODE) -> None:
        """
        Handle params for API url.

        :param word: searched word
        :type word: str

        :keyword language_code: language of the searched word (by default English US)
        :type language_code: LanguageCodes

        :raises ValueError: raised if ``word`` is empty
        :raises TypeError: raised if ``language_code`` is not instance of ``LanguageCodes``
        """

        self._word = str(word).strip()

        if not self._word:
            message = (
                '``word`` argument has passed with empty value. '
                'Expected to get non-empty value! '
                f'Got (word={self._word!r}).'
            )
            raise ValueError(message)

        if len(self._word.split()) > 1:
            message = (
                'For ``word`` argument has passed string that contains more than one word, '
                'most likely response won`t be successful. '
                'Expected to get string that contains one word! '
                f'Got (word={self._word!r})'
            )
            logger.warning(message)

        self._language_code = language_code

        if not isinstance(language_code, LanguageCodes):
            message = (
                'For ``language_code`` has passed unsupported type. '
                'Expected to get argument with type ``LanguageCodes``! '
                f'Got (language_code={self._language_code!r})'
            )
            raise TypeError(message)

    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        return f'{class_name}(word={self._word}, language_code={self._language_code!r})'

    @property
    def word(self) -> str:
        """ Get word that used in url """
        return self._word

    @property
    def language_code(self) -> LanguageCodes:
        """ Get language code that used in url """
        return self._language_code

    def get_url(self) -> str:
        """ Get prepared (with substituted word and language code) url that ready for request """
        url = self.API_URL_PATTERN.format(
            word=self._word,
            language_code=self._language_code.value
        )

        logger.debug(f'Generated url={url!r} with word={self._word!r} and language_code={self._language_code!r}')

        return url
