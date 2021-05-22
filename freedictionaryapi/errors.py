"""
Contains API errors.

Errors hierarchy:

    DictionaryApiError
        +-- DictionaryApiNotFoundError

.. exception:: DictionaryApiError(Exception)
.. exception:: DictionaryApiNotFoundError(DictionaryApiError):

.. const:: API_ERRORS_MAPPER
"""

import typing


__all__ = [
    'DictionaryApiError',
    'DictionaryApiNotFoundError',
    'API_ERRORS_MAPPER'
]


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


ERRORS: typing.List[typing.Type[DictionaryApiError]] = [
    DictionaryApiNotFoundError,
]

API_ERRORS_MAPPER: typing.Dict[int, typing.Type[DictionaryApiError]] = {error.code: error for error in ERRORS}
""" Mapping of the pairs of response status code and correspond exception type """
