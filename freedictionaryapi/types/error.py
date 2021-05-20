"""
Contains error type (of json API response, meaning parsed object).

.. class Error(ParsedObject)
"""

from .base import ParsedObject


__all__ = ['Error']


class Error(ParsedObject):
    """
    Implements the object of API json response
    that consists of error data:

        * title - short error title;
        * message - more detailed error message;
        * resolution - offer to solve problem.
    """

    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        return f'{class_name}(title={self.title!r}, message={self.message!r}, resolution={self.resolution!r})'

    @property
    def title(self) -> str:
        """
        :return: error title
        :rtype: :obj:`str`
        """

        title: str = self._data.get('title')

        return title

    @property
    def message(self) -> str:
        """
        :return: error message
        :rtype: :obj:`str`
        """

        message = self._data.get('message')

        return message

    @property
    def resolution(self) -> str:
        """
        :return: error resolution
        :rtype: :obj:`str`
        """

        resolution = self._data.get('resolution')

        return resolution
