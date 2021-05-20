"""
Contains meaning type.

.. class Meaning(ParsedObject)
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
    """

    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        return f'{class_name}(part_of_speech={self.part_of_speech!r}, definitions={self.definitions!r})'

    @property
    def part_of_speech(self) -> str:
        """
        :return: part of speech
        :rtype: :obj:`str`
        """

        part_of_speech: str = self._data.get('partOfSpeech')

        return part_of_speech

    @property
    def definitions(self) -> list[Definition]:
        """
        :return: list of definitions (parsed objects)
        :rtype: :obj:`list[Definition]`
        """

        definitions_data: list[dict[str, Union[str, list]]] = self._data.get('definitions')
        definitions = [Definition(definition_data) for definition_data in definitions_data]

        return definitions
