"""
Contains dictionary API error response parser.

.. class:: DictionaryApiErrorParser(BaseDictionaryApiParser)
"""

from .base_parser import BaseDictionaryApiParser
from ..types import Error


__all__ = ['DictionaryApiErrorParser']


class DictionaryApiErrorParser(BaseDictionaryApiParser):
    """
    Implements dictionary API error response parser.

    Contains useful :meth:`get_formatted_error_message` method
    that return pretty formatted error message.
    """

    def __init__(self, status_code: int, response: dict) -> None:
        """
        Init dictionary API error response parser instance.
        Parse API error response.

        :param status_code: http status code
        :type status_code: :obj:`int`
        :param response: API json response loaded in python object
        :type response: :obj:`dict`
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
        """
        :return: API response data
        :rtype: :obj:`dict`
        """

        return self._data

    @property
    def status_code(self) -> int:
        """
        :return: error response status code
        :rtype: :obj:`int`
        """

        return self._status_code

    @property
    def title(self) -> str:
        """
        Error title. Shortcut for :obj:`Error.title`

        :return: error title
        :rtype: :obj:`str`
        """

        return self._error.title

    @property
    def message(self) -> str:
        """
        Error message. Shortcut for :obj:`Error.message`

        :return: error message
        :rtype: :obj:`str`
        """

        return self._error.message

    @property
    def resolution(self) -> str:
        """
        Error resolution. Shortcut for `Error.resolution`

        :return: error resolution
        :rtype: :obj:`str`
        """

        return self._error.resolution

    def get_formatted_error_message(self) -> str:
        """
        Get readable error message

        :return: readable error message
        :rtype: :obj:`str`
        """

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
