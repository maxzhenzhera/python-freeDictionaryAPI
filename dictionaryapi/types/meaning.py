"""
Contains meaning type.

.. class Meaning(ParsedObject)
    Implements meaning type (info about meaning)
"""

from typing import Union

from .base import ParsedObject
from .definition import Definition


__all__ = ['Meaning']


class Meaning(ParsedObject):
    """
    Implements the object of API json response
    that consists of meaning data:
        * partOfSpeech - part of speech;
        * definitions - list of definitions.

    .. property:: part_of_speech(self) -> str
    .. property:: definitions(self) -> list[Definition]
    """

    def __repr__(self) -> str:
        return f'Meaning(part_of_speech={self.part_of_speech}, definitions={self.definitions})'

    @property
    def part_of_speech(self) -> str:
        """ Get part of speech """
        part_of_speech: str = self._data.get('partOfSpeech')

        return part_of_speech

    @property
    def definitions(self) -> list[Definition]:
        """ Get list of definitions """
        definitions_data: list[dict[str, Union[str, list]]] = self._data.get('definitions')
        definitions = [Definition(definition_data) for definition_data in definitions_data]

        return definitions
