"""
Contains base abstract dictionary API parser.

.. class:: BaseDictionaryApiParser(abc.ABC)
"""

import abc
from typing import Any


__all__ = ['BaseDictionaryApiParser']


class BaseDictionaryApiParser(abc.ABC):
    """
    Implements base abstract dictionary API parser.
    Supposed to be inherited by other dictionary API parsers.
    """

    def __init__(self, response: Any) -> None:
        """
        Init base dictionary API parser instance.

        :param response: API json response loaded in python object
        :type response: :obj:`Any`
        """

        self._response = response

    @property
    def response(self) -> Any:
        """
        :return: API json response loaded in python object
        :rtype: :obj:`Any`
        """

        return self._response

    @property
    @abc.abstractmethod
    def data(self) -> dict:
        """
        Response data. Actually, :obj:`dict` of API response.
        API response object is not always a :obj:`dict`.

        To make sure that in :obj:`ParsedObject` instances
        we use :obj:`dict` here is this property.

        :return: response data for parsing
        :rtype: :obj:`dict`
        """
