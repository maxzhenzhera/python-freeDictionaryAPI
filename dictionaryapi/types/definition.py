"""
Contains definition type.

.. class Definition(ParsedObject)
    Implements definition type (info about definition)
"""

from .base import ParsedObject


__all__ = ['Definition']


class Definition(ParsedObject):
    """
    Implements the object of API json response
    that consists of definition data:
        * definition - phrase about word meaning;
        * synonyms - list of synonyms;
        * example - example sentence or phrase with word usage by current definition.

    .. property:: definition(self) -> str
    .. property:: synonyms(self) -> list[str]
    .. property:: example(self) -> str
    """

    def __repr__(self) -> str:
        return f'Definition(definition={self.definition}, synonyms={self.synonyms}, example={self.example})'

    @property
    def definition(self) -> str:
        """ Get definition """
        definition: str = self._data.get('definition')

        return definition

    @property
    def synonyms(self) -> list[str]:
        """ Get list of synonyms """
        synonyms: list[str] = self._data.get('synonyms')

        return synonyms

    @property
    def example(self) -> str:
        """ Get example """
        example: str = self._data.get('example')

        return example
