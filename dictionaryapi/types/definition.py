"""
Contains definition type.

.. class Definition(ParsedObject)
    Implements definition type (info about definition)
"""

from typing import Optional

from .base import ParsedObject


__all__ = ['Definition']


class Definition(ParsedObject):
    """
    Implements the object of API json response
    that consists of definition data:
        * definition - phrase about word meaning;
        * synonyms - list of synonyms;
        * example - example sentence or phrase with word usage by current definition.

    Note:
        ``synonyms`` and ``example`` properties are not always available.
        API response does not always provide these fields.
        So in return type it is annotated accordingly:
            ``synonyms`` -> ``Optional[list[str]]``
            ``example`` -> Optional[str]

    .. property:: definition(self) -> str
    .. property:: synonyms(self) -> list[str]
    .. property:: example(self) -> str
    """

    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        return f'{class_name}(definition={self.definition!r}, example={self.example!r}, synonyms={self.synonyms!r})'

    @property
    def definition(self) -> str:
        """ Get definition """
        definition: str = self._data.get('definition')

        return definition

    @property
    def synonyms(self) -> Optional[list[str]]:
        """ Get list of synonyms """
        synonyms: Optional[list[str]] = self._data.get('synonyms')

        return synonyms

    @property
    def example(self) -> Optional[str]:
        """ Get example """
        example: Optional[str] = self._data.get('example')

        return example
