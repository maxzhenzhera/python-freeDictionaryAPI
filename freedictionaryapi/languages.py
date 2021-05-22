"""
Contains enumerations of supported languages.

.. class:: LanguageCodes(Enum)

.. const:: DEFAULT_LANGUAGE_CODE: LanguageCodes
"""

from enum import Enum


__all__ = [
    'LanguageCodes',
    'DEFAULT_LANGUAGE_CODE'
]


class LanguageCodes(Enum):
    """
    Contains supported languages that might be used in API URL.

    :obj:`Enum` members consist of :obj:`str`
    that refer on language code
    that is used in URL for API.
    """

    ARABIC = 'ar'
    BRAZILIAN_PORTUGUESE = 'pt-BR'
    ENGLISH_UK = 'en_GB'
    ENGLISH_US = 'en_US'
    FRENCH = 'fr'
    GERMAN = 'de'
    HINDI = 'hi'
    ITALIAN = 'it'
    JAPANESE = 'ja'
    KOREAN = 'ko'
    RUSSIAN = 'ru'
    SPANISH = 'es'
    TURKISH = 'tr'


DEFAULT_LANGUAGE_CODE: LanguageCodes = LanguageCodes.ENGLISH_US
""" Default language that is used in API """
