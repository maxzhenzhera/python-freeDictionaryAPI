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

    .. note::
        ``synonyms`` and ``example`` properties are not always available.
        API response does not always provide these fields.
        So in return type it is annotated accordingly:

            - ``synonyms`` -> :obj:`Optional[list[str]]`
            - ``example`` -> :obj:`Optional[str]`
    """

    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        return f'{class_name}(definition={self.definition!r}, example={self.example!r}, synonyms={self.synonyms!r})'

    @property
    def definition(self) -> str:
        """
        :return: definition (meaning phrase or sentence)
        :rtype: :obj:`str`
        """

        definition: str = self._data.get('definition')

        return definition

    @property
    def synonyms(self) -> Optional[list[str]]:
        """
        :return: list of synonyms (might be omitted)
        :rtype: :obj:`Optional[list[str]]`
        """

        synonyms: Optional[list[str]] = self._data.get('synonyms')

        return synonyms

    @property
    def example(self) -> Optional[str]:
        """
        :return: example phrase or sentence of word usage (might be omitted)
        :rtype: :obj:`Optional[str]`
        """

        example: Optional[str] = self._data.get('example')

        return example
