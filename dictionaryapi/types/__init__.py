"""
Contains types of parsed objects.

Structure of types relations:
- ParsedObject (Abstract class for all objects below)
    - Word (successful response)
        - Phonetic
        - Meaning
            - Definition
    - Error (error response)
"""

from .base import ParsedObject
from .definition import Definition
from .error import Error
from .meaning import Meaning
from .phonetic import Phonetic
from .word import Word


__all__ = [
    'ParsedObject',
    'Definition',
    'Error',
    'Meaning',
    'Phonetic',
    'Word'
]
