"""
Contains dictionary API parsers.
"""

from .base_parser import BaseDictionaryApiParser
from .response_parser import DictionaryApiParser
from .error_parser import DictionaryApiErrorParser


__all__ = [
    'BaseDictionaryApiParser',
    'DictionaryApiParser',
    'DictionaryApiErrorParser'
]
