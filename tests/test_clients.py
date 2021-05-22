"""
Contains tests for clients.

.. class:: TestAsyncDictionaryApiClient
.. class:: TestDictionaryApiClient
"""

import pytest

from freedictionaryapi.clients.async_client import AsyncDictionaryApiClient
from freedictionaryapi.clients.sync_client import DictionaryApiClient
from freedictionaryapi.errors import API_ERRORS_MAPPER


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
        # wrong_language_argument is not an instance of languages.LanguageCodes
        wrong_language_argument = 'EN'
        with pytest.raises(TypeError) as raised_error:
            _ = AsyncDictionaryApiClient(default_language_code=wrong_language_argument)

    def test_error_raising_on_wrong_session_argument(self):
        # wrong_session_argument is not an instance of aiohttp.ClientSession
        wrong_session_argument = 'I am not aiohttp client session'
        with pytest.raises(TypeError) as raised_error:
            _ = AsyncDictionaryApiClient(session=wrong_session_argument)

    @pytest.mark.asyncio
    async def test_404_error_raising_on_nonexistent_word_searching(self, client: AsyncDictionaryApiClient):
        error = API_ERRORS_MAPPER.get(404)
        with pytest.raises(error) as raised_error:
            nonexistent_word = 'blablablabla'

            # _ = client.fetch_json()
            _ = await client.fetch_parser(nonexistent_word)
            # _ = client.fetch_word()

    @pytest.mark.asyncio
    async def test_client_fetch_parser(self, client: AsyncDictionaryApiClient):
        existent_word = 'hello'
        status_that_parser_has_been_fetched_without_error_occurring = True

        _ = await client.fetch_parser(existent_word)

        assert status_that_parser_has_been_fetched_without_error_occurring

    @pytest.mark.asyncio
    async def test_client_fetch_word(self, client: AsyncDictionaryApiClient):
        existent_word = 'hello'
        status_that_word_has_been_fetched_without_error_occurring = True

        _ = await client.fetch_word(existent_word)

        assert status_that_word_has_been_fetched_without_error_occurring

    @pytest.mark.asyncio
    async def test_client_fetched_parser_word(self, client: AsyncDictionaryApiClient):
        existent_word = 'hello'

        parser = await client.fetch_parser(existent_word)
        parser_word = parser.word

        word = await client.fetch_word(existent_word)

        assert parser_word == word


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
        # wrong_language_argument is not an instance of languages.LanguageCodes
        wrong_language_argument = 'EN'
        with pytest.raises(TypeError) as raised_error:
            _ = DictionaryApiClient(default_language_code=wrong_language_argument)

    def test_error_raising_on_wrong_client_argument(self):
        # wrong_client_argument is not an instance of httpx.Client
        wrong_client_argument = 'I am not httpx client'
        with pytest.raises(TypeError) as raised_error:
            _ = DictionaryApiClient(client=wrong_client_argument)

    def test_404_error_raising_on_nonexistent_word_searching(self, client: DictionaryApiClient):
        error = API_ERRORS_MAPPER.get(404)
        with pytest.raises(error) as raised_error:
            nonexistent_word = 'blablablabla'

            # _ = client.fetch_json()
            _ = client.fetch_parser(nonexistent_word)
            # _ = client.fetch_word()

    def test_client_fetch_parser(self, client: DictionaryApiClient):
        existent_word = 'hello'
        status_that_parser_has_been_fetched_without_error_occurring = True

        _ = client.fetch_parser(existent_word)

        assert status_that_parser_has_been_fetched_without_error_occurring

    def test_client_fetch_word(self, client: DictionaryApiClient):
        existent_word = 'hello'
        status_that_word_has_been_fetched_without_error_occurring = True

        _ = client.fetch_word(existent_word)

        assert status_that_word_has_been_fetched_without_error_occurring

    def test_client_fetched_parser_word(self, client: DictionaryApiClient):
        existent_word = 'hello'

        parser = client.fetch_parser(existent_word)
        parser_word = parser.word

        word = client.fetch_word(existent_word)

        assert parser_word == word
