"""
Contains base abstract dictionary API parser.

.. class:: BaseDictionaryApiParser(abc.ABC)
    Implements base abstract dictionary API parser
"""

import abc
from typing import Any


__all__ = ['BaseDictionaryApiParser']


class BaseDictionaryApiParser(abc.ABC):
    """
    Implements base abstract dictionary API parser.
    Supposed to be inherited by other dictionary API parsers.

    .. attr:: _response Any: API json response loaded in python object

    .. property:: response(self) -> Any

    .. abstractproperty:: data(self) -> dict
    """

    def __init__(self, response: Any) -> None:
        """
        Init base dictionary API parser.

        :param response: API json response loaded in python object
        :type response: Any
        """

        self._response = response

    @property
    def response(self) -> Any:
        """ Get response object (object that loaded from json API response) """
        return self._response

    @property
    @abc.abstractmethod
    def data(self) -> dict:
        """
        Get response data. Actually, ``dict`` of API response.
        API response object is not always a ``dict``.

        To make sure that in ``ParsedObject`` instances
        we use ``dict`` here is this property.
        """
