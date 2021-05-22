"""
Implements convenient API wrapper for Free Dictionary API.
    - WEB:    [https://dictionaryapi.dev/]
    - Github: [https://github.com/meetDeveloper/freeDictionaryAPI]
"""

from . import (
    clients,
    parsers,
    types,
    errors,
    languages,
    urls
)
from .errors import DictionaryApiError
from .languages import LanguageCodes
from .parsers import (
    DictionaryApiParser,
    DictionaryApiErrorParser
)
from .urls import ApiUrl


__all__ = [
    # packages
    'clients',
    'parsers',
    'types',
    # modules
    'errors',
    'languages',
    'urls',
    # classes
    # # parsers
    'DictionaryApiParser',
    'DictionaryApiErrorParser',
    # # supported languages
    'LanguageCodes',
    # # API url generator
    'ApiUrl',
    # # Common error
    'DictionaryApiError'
]


__version__ = '0.0.1'
