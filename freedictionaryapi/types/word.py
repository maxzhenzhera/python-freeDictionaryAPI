"""
Contains word type (the biggest scale).

.. class Word(ParsedObject)
"""

import typing
from .base import ParsedObject
from .meaning import Meaning
from .phonetic import Phonetic


__all__ = ['Word']


class Word(ParsedObject):
    """
    Implements the biggest object of the API JSON response,
    so it contains all information about word
    that might be retrieved from API
    that structured in different parsed objects.
    """

    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        return f'{class_name}(word={self.word!r})'

    @property
    def word(self) -> str:
        """
        :return: actually word
        :rtype: :obj:`str`
        """

        word: str = self._data.get('word')

        return word

    @property
    def phonetics(self) -> typing.List[Phonetic]:
        """
        :return: list of phonetics
        :rtype: :obj:`list[Phonetic]`
        """

        phonetics_data: typing.List[dict] = self._data.get('phonetics')
        phonetics = [Phonetic(phonetic_data) for phonetic_data in phonetics_data]

        return phonetics

    @property
    def meanings(self) -> typing.List[Meaning]:
        """
        :return: list of meanings
        :rtype: :obj:`list[Meaning]`
        """

        meanings_data: typing.List[dict] = self._data.get('meanings')
        meanings = [Meaning(meaning_data) for meaning_data in meanings_data]

        return meanings
