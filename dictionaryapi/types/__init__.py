"""
Contains types of parsed objects.

Structure of types relations:
- ParsedObject (Abstract class for all objects below)
    - Word
        - Phonetic
        - Meaning
            - Definition
"""

from .base import ParsedObject
from .definition import Definition
from .meaning import Meaning
from .phonetic import Phonetic
from .word import Word


__all__ = [
    'ParsedObject',
    'Definition',
    'Meaning',
    'Phonetic',
    'Word'
]
