"""
Contains dictionary API error response parser.

.. class:: DictionaryApiErrorParser
    Implements dictionary API error response parser
"""

from .base import BaseDictionaryApiParser
from ..types import Error


__all__ = ['DictionaryApiErrorParser']


class DictionaryApiErrorParser(BaseDictionaryApiParser):
    """
    Implements dictionary API error response parser.

    Contains useful ``get_formatted_error_message`` method
    that return pretty formatted error message.

    .. attrs:: _status_code int: response status code
    .. attr:: _response dict: API json response loaded in python object
    .. attrs:: _data dict: data for parsing actually
    .. attrs:: _error Error: parsed object that contains error info

    .. property:: status_code(self) -> int
    .. property:: title(self) -> str
    .. property:: message(self) -> str
    .. property:: resolution(self) -> str

    .. method:: get_formatted_error_message(self) -> str
        Get formatted error message (might be used on errors raising)
    """

    def __init__(self, status_code: int, response: dict) -> None:
        """
        Init dictionary API error response parser.
        Parse API error response.

        :param status_code: http status code
        :type status_code: int
        :param response: API json response loaded in python object
        :type response: dict
        """

        super().__init__(response)

        self._status_code = status_code
        # For the same behaviour as in the ``DictionaryApiParser``
        # where in API response returned list, we save some attrs:
        # * response - python object loaded from json response;
        # * data - actually data for parsing (supposed to be simple ``dict``).
        # In case of ``DictionaryApiParser`` we have to get first element of returned list.
        # Here we just repeat the same behaviour.
        self._data = self._response

        self._error = Error(self._data)

    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        return f'{class_name}(status_code={self._status_code})'

    @property
    def data(self) -> dict:
        """ Get ``dict`` of the API response """
        return self._data

    @property
    def status_code(self) -> int:
        """ Get error http status code """
        return self._status_code

    @property
    def title(self) -> str:
        """ Get error title. Shortcut for ``error.title`` """
        return self._error.title

    @property
    def message(self) -> str:
        """ Get error message. Shortcut for ``error.message`` """
        return self._error.message

    @property
    def resolution(self) -> str:
        """ Get error resolution. Shortcut for ``error.resolution`` """
        return self._error.resolution

    def get_formatted_error_message(self) -> str:
        """ Get readable error message """
        error_message = '\n\t'.join(
            (
                'API error occured during request processing.',
                f'Status code: {self.status_code}.',
                f'Title: {self.title}.',
                f'Message: {self.message}.',
                f'Resolution: {self.resolution}.',
            )
        )

        return error_message
