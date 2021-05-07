"""

"""

from http import HTTPStatus
from typing import Optional
import logging

import aiohttp
import aiocache


from .languages import (
    DEFAULT_LANGUAGE_CODE,
    LanguageCodes
)
from .types import (
    Word,
    Definition,
    Phonetic,
    Meaning
)
from .parsers import DictionaryApiParser
from .urls import ApiUrl
from .errors import (
    DictionaryApiError,
    DictionaryApiNotFoundError,
    API_ERRORS_MAPPER
)

__all__ = ['DictionaryApiClient']


logger = logging.getLogger(__name__)


class DictionaryApiClient:
    """

    """

    def __init__(self,
                 default_language_code: LanguageCodes = DEFAULT_LANGUAGE_CODE,
                 *,
                 aiohttp_client_session_kwargs: Optional[dict] = None
                 ) -> None:
        """
        Init client for dictionary API.

        :param default_language_code: default language of the searched words (by default English US)
        :type default_language_code: LanguageCodes

        :keyword aiohttp_client_session_kwargs: kwargs for ``aiohttp.ClientSession`` instance
        :type aiohttp_client_session_kwargs: dict

        :raises TypeError: raised if ``language_code`` is not instance of ``LanguageCodes``
        """

        self._default_language_code = default_language_code

        if not isinstance(default_language_code, LanguageCodes):
            message = (
                'For ``language_code`` has passed unsupported type. '
                'Expected to get argument with type ``LanguageCodes``! '
                f'Got (language_code={self._default_language_code!r})'
            )
            raise TypeError(message)

        if aiohttp_client_session_kwargs:
            self._session = aiohttp.ClientSession(**aiohttp_client_session_kwargs)
        else:
            self._session = aiohttp.ClientSession()

    @property
    def default_language_code(self) -> LanguageCodes:
        """ Get default language code """
        return self._default_language_code

    @property
    def session(self) -> aiohttp.ClientSession:
        """ Get aiohttp session """
        return self._session

    def __repr__(self) -> str:
        return f'DictionaryApiClient(default_language_code={self._default_language_code!r})'

    async def close(self) -> None:
        """ Close dictionary API client """
        await self._session.close()

    async def fetch_word(self, word: str, language_code: Optional[LanguageCodes] = None) -> Word:
        """

        :param word:
        :type word:
        :param language_code:
        :type language_code:
        :return:
        :rtype:
        """

        language_code = self._default_language_code if language_code is None else language_code

        url = ApiUrl(word, language_code=language_code).get_url()

        response: aiohttp.ClientResponse
        async with self._session.get(url) as response:
            response_code = response.status

            if response_code != HTTPStatus.OK:
                error = API_ERRORS_MAPPER.get(response_code, DictionaryApiError)

                message = 'error'

                raise error(message)
            else:
                data = await response.json()

        parser = DictionaryApiParser(data)
        word = parser.word

        return word
