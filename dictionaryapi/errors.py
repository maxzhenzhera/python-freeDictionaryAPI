"""
Contains API errors.

.. exception:: DictionaryApiError(Exception)
    Common error for all API errors
.. exception:: DictionaryApiNotFoundError(DictionaryApiError):
    Raised on 404 status code

.. data:: API_ERRORS_MAPPER
    Mapper of http status codes and error objects (exception classes)
"""

from typing import Type


__all__ = ['DictionaryApiError', 'DictionaryApiNotFoundError', 'API_ERRORS_MAPPER']


class DictionaryApiError(Exception):
    """
    Common error for all API errors.
    """

    code = None


class DictionaryApiNotFoundError(DictionaryApiError):
    """
    API error that raised
    if response status code is 404 (Not Found).

    The most often might occur
    when searched word is not found.
    """

    code = 404


ERRORS: list[Type[DictionaryApiError]] = [
    DictionaryApiNotFoundError,
]

API_ERRORS_MAPPER: dict[int, Type[DictionaryApiError]] = {error.code: error for error in ERRORS}
