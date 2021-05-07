"""
Contains word type (the biggest scale).

.. class Word(ParsedObject)
    Implements word type (all word info)
"""

from typing import Union

from .base import ParsedObject
from .meaning import Meaning
from .phonetic import Phonetic


__all__ = ['Word']


class Word(ParsedObject):
    """
    Implements the biggest object of API json response,
    so it contains all information about word
    that might be retrieved from API
    that structured in different parsed objects.

    .. property:: word(self) -> str
    .. property:: phonetics(self) -> list[Phonetic]
    .. property:: meanings(self) -> list[Meaning]
    """

    def __repr__(self) -> str:
        return f'Word(word={self.word!r})'

    @property
    def word(self) -> str:
        """ Get word actually """
        word: str = self._data.get('word')

        return word

    @property
    def phonetics(self) -> list[Phonetic]:
        """ Get list of phonetics """
        phonetics_data: list[dict[str, str]] = self._data.get('phonetics')
        phonetics = [Phonetic(phonetic_data) for phonetic_data in phonetics_data]

        return phonetics

    @property
    def meanings(self) -> list[Meaning]:
        """ Get list of meanings """
        meanings_data: list[dict[str, Union[str, list]]] = self._data.get('meanings')
        meanings = [Meaning(meaning_data) for meaning_data in meanings_data]

        return meanings
