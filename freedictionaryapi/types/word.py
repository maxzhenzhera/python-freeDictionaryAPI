"""
Contains word type (the biggest scale).

.. class Word(ParsedObject)
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
    """

    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        return f'{class_name}(word={self.word!r})'

    @property
    def word(self) -> str:
        """ Word (word name) """
        word: str = self._data.get('word')

        return word

    @property
    def phonetics(self) -> list[Phonetic]:
        """ List of phonetics """
        phonetics_data: list[dict[str, str]] = self._data.get('phonetics')
        phonetics = [Phonetic(phonetic_data) for phonetic_data in phonetics_data]

        return phonetics

    @property
    def meanings(self) -> list[Meaning]:
        """ List of meanings """
        meanings_data: list[dict[str, Union[str, list]]] = self._data.get('meanings')
        meanings = [Meaning(meaning_data) for meaning_data in meanings_data]

        return meanings
