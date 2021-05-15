"""
Contains tests for clients.

.. class:: TestAsyncDictionaryApiClient
.. class:: TestDictionaryApiClient
"""

import pytest

from dictionaryapi.clients import (
    AsyncDictionaryApiClient,
    DictionaryApiClient
)
from dictionaryapi.errors import API_ERRORS_MAPPER


class TestAsyncDictionaryApiClient:
    """
    Contains tests for
        * async API client (``AsyncDictionaryApiClient``).

    Checking that API client raises according errors.
    """

    # fixtures ---------------------------------------------------------------------------------------------------------

    @pytest.fixture(name='client')
    async def fixture_client(self) -> AsyncDictionaryApiClient:
        """ Get instance of async API client """
        client = AsyncDictionaryApiClient()
        yield client
        await client.close()

    # tests ------------------------------------------------------------------------------------------------------------

    def test_error_raising_on_wrong_language_argument(self):
        # wrong_language_argument is not instance of languages.LanguageCodes
        wrong_language_argument = 'EN'
        with pytest.raises(TypeError) as raised_error:
            _ = AsyncDictionaryApiClient(default_language_code=wrong_language_argument)

    @pytest.mark.asyncio
    async def test_404_error_raising_on_nonexistent_word_searching(self, client: AsyncDictionaryApiClient):
        error = API_ERRORS_MAPPER.get(404)
        with pytest.raises(error) as raised_error:
            nonexistent_word = 'blablablabla'

            # _ = client._fetch_json()
            _ = await client.fetch_parser(nonexistent_word)
            # _ = client.fetch_word()


class TestDictionaryApiClient:
    """
    Contains tests for
        * sync API client (``DictionaryApiClient``).

    Checking that API client raises according errors.
    """

    # fixtures ---------------------------------------------------------------------------------------------------------

    @pytest.fixture(name='client')
    def fixture_client(self) -> DictionaryApiClient:
        """ Get instance of sync API client """
        client = DictionaryApiClient()
        yield client
        client.close()

    # tests ------------------------------------------------------------------------------------------------------------

    def test_error_raising_on_wrong_language_argument(self):
        # wrong_language_argument is not instance of languages.LanguageCodes
        wrong_language_argument = 'EN'
        with pytest.raises(TypeError) as raised_error:
            _ = AsyncDictionaryApiClient(default_language_code=wrong_language_argument)

    def test_404_error_raising_on_nonexistent_word_searching(self, client: AsyncDictionaryApiClient):
        error = API_ERRORS_MAPPER.get(404)
        with pytest.raises(error) as raised_error:
            nonexistent_word = 'blablablabla'

            # _ = client._fetch_json()
            _ = client.fetch_parser(nonexistent_word)
            # _ = client.fetch_word()
