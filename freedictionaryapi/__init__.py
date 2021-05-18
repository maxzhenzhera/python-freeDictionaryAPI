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
from .clients import (
    DictionaryApiClient,
    AsyncDictionaryApiClient
)
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
    # # clients
    'DictionaryApiClient',
    'AsyncDictionaryApiClient',
    # # parsers
    'DictionaryApiParser',
    'DictionaryApiErrorParser',
    # # supported languages
    'LanguageCodes',
    # # API url generator
    'ApiUrl',
]


__version__ = '0.0.1'
