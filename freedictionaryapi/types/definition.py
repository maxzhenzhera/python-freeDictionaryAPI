"""
Contains definition type.

.. class Definition(ParsedObject)
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

    .. note:
        ``synonyms`` and ``example`` properties are not always available.
        API response does not always provide these fields.
        So in return type it is annotated accordingly:
            ``synonyms`` -> ``Optional[list[str]]``
            ``example`` -> Optional[str]
    """

    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        return f'{class_name}(definition={self.definition!r}, example={self.example!r}, synonyms={self.synonyms!r})'

    @property
    def definition(self) -> str:
        """ Definition (meaning phrase or sentence) """
        definition: str = self._data.get('definition')

        return definition

    @property
    def synonyms(self) -> Optional[list[str]]:
        """ List of synonyms (might be omitted) """
        synonyms: Optional[list[str]] = self._data.get('synonyms')

        return synonyms

    @property
    def example(self) -> Optional[str]:
        """ Example phrase or sentence of word usage (might be omitted) """
        example: Optional[str] = self._data.get('example')

        return example
