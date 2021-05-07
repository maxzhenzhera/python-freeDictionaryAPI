"""
Contains enumerations of supported languages.

.. class:: LanguageCodes(Enum)

.. const:: DEFAULT_LANGUAGE_CODE: LanguageCodes
"""

from enum import Enum


__all__ = ['LanguageCodes', 'DEFAULT_LANGUAGE_CODE']


class LanguageCodes(Enum):
    """ Contains supported languages and codes that used in API url """
    ARABIC = 'ar'
    BRAZILIAN_PORTUGUESE = 'pt - BR'
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
