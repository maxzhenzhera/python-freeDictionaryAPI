"""
Contains tests for API url generation.

.. class:: TestApiUrlGeneration
"""

import pytest

from freedictionaryapi.languages import LanguageCodes
from freedictionaryapi.urls import ApiUrl


class TestApiUrlGeneration:
    """
    Contains tests for
        * API url generator (``ApiUrl``).

    Checking that API url generator
    correctly init instance and generate url.
    """

    # fixtures ---------------------------------------------------------------------------------------------------------

    @pytest.fixture(name='data_list', scope='class')
    def fixture_data_list(self) -> list[dict]:
        """ Get ``list`` of ``dict`` that contains arguments for ``ApiUrl`` instances """
        data_list = [
            {
                'word': 'hello',
                'language_code': LanguageCodes.ENGLISH_US
            },
            {
                'word': 'Olá',
                'language_code': LanguageCodes.BRAZILIAN_PORTUGUESE
            }
        ]

        return data_list

    # tests ------------------------------------------------------------------------------------------------------------

    def test_error_raising_on_empty_word(self):
        empty_word = '          '

        with pytest.raises(ValueError) as raised_error:
            _ = ApiUrl(empty_word)

    def test_generated_url_with_some_data(self, data_list: list[dict]):
        for data in data_list:
            word = data['word']
            language = data['language_code']

            fact_url = f'https://api.dictionaryapi.dev/api/v2/entries/{language.value}/{word.strip()}'
            expected_url = ApiUrl(**data).get_url()

            assert expected_url == fact_url
