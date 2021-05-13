"""
Contains dictionary API parsers.
"""

from .base import BaseDictionaryApiParser
from .response import DictionaryApiParser
from .error import DictionaryApiErrorParser


__all__ = [
    'BaseDictionaryApiParser',
    'DictionaryApiParser',
    'DictionaryApiErrorParser'
]
