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
        """ Error title """
        return self._data.get('title')

    @property
    def message(self) -> str:
        """ Error message """
        return self._data.get('message')

    @property
    def resolution(self) -> str:
        """ Error resolution """
        return self._data.get('resolution')
