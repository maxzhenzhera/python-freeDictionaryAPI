"""
Contains tests for parsing.

.. class:: TestResponseParsing
.. class:: TestErrorResponseParsing
"""

import json
import typing

import pytest

from freedictionaryapi.parsers import (
    DictionaryApiParser,
    DictionaryApiErrorParser
)
from freedictionaryapi.types import (
    Definition,
    Error,
    Meaning,
    Phonetic,
    Word
)

from .settings import DATA_DIR


class TestResponseParsing:
    """
    Contains tests for
        * response parser (``DictionaryApiParser``);
        * types (``Word``, ``Phonetic``, ``Meaning``, ``Definition``).

    Checking that parser and types data
    equal real data that loaded from response json.
    """

    # fixtures----------------------------------------------------------------------------------------------------------

    @pytest.fixture(name='response', scope='class')
    def fixture_api_response_of_the_hello_word(self) -> list:
        """ API response (word=hello) loaded in python object """
        # for json data is used result of the API request with ``hello`` word
        # actually, dump is taken from example in web page
        # https://dictionaryapi.dev/
        json_file_path = DATA_DIR / 'word_hello_API_response.json'
        with open(json_file_path, 'r', encoding='utf-8') as file:
            response = json.load(file)

        return response

    @pytest.fixture(name='data', scope='class')
    def fixture_data_from_response(self, response: list) -> dict:
        """ Data of the API response """
        # API json response firstly is enveloped by ``list``
        # so we get ``dict`` object from this
        data = response[0]

        return data

    @pytest.fixture(name='parser', scope='class')
    def fixture_parser_from_response(self, response: list) -> DictionaryApiParser:
        """ Parser object init-ed with API response """
        parser = DictionaryApiParser(response)

        return parser

    @pytest.fixture(name='word_from_data', scope='class')
    def fixture_word_from_data(self, data: dict) -> Word:
        """ Word object init-ed with API response data """
        word = Word(data)

        return word

    @pytest.fixture(name='phonetics_from_word', scope='class')
    def fixture_phonetics_from_word(self, word_from_data: Word) -> typing.List[Phonetic]:
        """ List of phonetics from word """
        phonetics = word_from_data.phonetics

        return phonetics

    @pytest.fixture(name='meanings_from_word', scope='class')
    def fixture_meanings_from_word(self, word_from_data: Word) -> typing.List[Meaning]:
        """ List of meanings from word  """
        meanings = word_from_data.meanings

        return meanings

    @pytest.fixture(name='definitions_from_meanings', scope='class')
    def fixture_definitions_from_meanings(self, meanings_from_word: typing.List[Meaning]
                                          ) -> typing.List[typing.List[Definition]]:
        """ List of definition list from word meanings """
        definitions = [meaning.definitions for meaning in meanings_from_word]

        return definitions

    # tests ------------------------------------------------------------------------------------------------------------

    # # parsers.DictionaryApiParser ------------------------------------------------------------------------------------

    def test_parser_word(self, word_from_data: Word, parser: DictionaryApiParser):
        word_from_parser = parser.word

        assert word_from_parser == word_from_data

    def test_parser_word_phonetics(self, word_from_data: Word, parser: DictionaryApiParser):
        phonetics_from_word = word_from_data.phonetics
        phonetics_from_parser = parser.phonetics

        assert phonetics_from_parser == phonetics_from_word

    def test_parser_word_meanings(self, word_from_data: Word, parser: DictionaryApiParser):
        meanings_from_word = word_from_data.meanings
        meanings_from_parser = parser.meanings

        assert meanings_from_parser == meanings_from_word

    def test_parser_word_definitions_as_parsed_objects(self, word_from_data: Word, parser: DictionaryApiParser):
        definitions_from_word = [
            definition
            for meaning in word_from_data.meanings
            for definition in meaning.definitions
        ]
        definitions_from_parser = parser._get_all_definitions_as_parsed_objects()

        assert definitions_from_parser == definitions_from_word

    def test_parser_word_transcription(self, word_from_data: Word, parser: DictionaryApiParser):
        transcription_from_word = word_from_data.phonetics[0].transcription
        transcription_from_parser = parser.get_transcription()

        assert transcription_from_parser == transcription_from_word

    def test_parser_word_all_transcriptions(self, word_from_data: Word, parser: DictionaryApiParser):
        transcriptions_from_word = [phonetic.transcription for phonetic in word_from_data.phonetics]
        transcriptions_from_parser = parser.get_all_transcriptions()

        assert transcriptions_from_word == transcriptions_from_parser

    def test_parser_word_link_on_audio_with_pronunciation(self, word_from_data: Word, parser: DictionaryApiParser):
        link_on_audio_with_pronunciation_from_word = word_from_data.phonetics[0].audio
        link_on_audio_with_pronunciation_from_parser = parser.get_link_on_audio_with_pronunciation()

        assert link_on_audio_with_pronunciation_from_parser == link_on_audio_with_pronunciation_from_word

    def test_parser_word_all_parts_of_speech(self, word_from_data: Word, parser: DictionaryApiParser):
        all_parts_of_speech_from_word = [meaning.part_of_speech for meaning in word_from_data.meanings]
        all_parts_of_speech_from_parser = parser.get_all_parts_of_speech()

        assert all_parts_of_speech_from_parser == all_parts_of_speech_from_word

    def test_parser_word_all_definitions(self, word_from_data: Word, parser: DictionaryApiParser):
        all_definitions_from_word = [
            definition.definition
            for meaning in word_from_data.meanings
            for definition in meaning.definitions
        ]
        all_definitions_from_parser = parser.get_all_definitions()

        assert all_definitions_from_parser == all_definitions_from_word

    def test_parser_word_all_examples(self, word_from_data: Word, parser: DictionaryApiParser):
        all_examples_from_word = [
            definition.example
            for meaning in word_from_data.meanings
            for definition in meaning.definitions
        ]
        all_examples_from_parser = parser.get_all_examples()

        assert all_examples_from_parser == all_examples_from_word

    def test_parser_word_all_synonyms(self, word_from_data: Word, parser: DictionaryApiParser):
        all_synonyms_from_word = list({
            synonym
            for meaning in word_from_data.meanings
            for definition in meaning.definitions
            if definition.synonyms
            for synonym in definition.synonyms
        })
        all_synonyms_from_parser = parser.get_all_synonyms()

        assert all_synonyms_from_parser == all_synonyms_from_word

    # # types.Word -----------------------------------------------------------------------------------------------------

    def test_word_type_word(self, data: dict, word_from_data: Word):
        word_from_data_ = data['word']
        word_from_word_type = word_from_data.word

        assert word_from_word_type == word_from_data_

    def test_word_type_phonetics(self, data: dict, word_from_data: Word):
        phonetics_from_data = [Phonetic(phonetic_data) for phonetic_data in data['phonetics']]
        phonetics_from_word_type = word_from_data.phonetics

        assert phonetics_from_word_type == phonetics_from_data

    def test_word_type_meanings(self, data: dict, word_from_data: Word):
        meanings_from_data = [Meaning(meaning_data) for meaning_data in data['meanings']]
        meanings_from_word_type = word_from_data.meanings

        assert meanings_from_word_type == meanings_from_data

    # # types.Phonetic -------------------------------------------------------------------------------------------------

    def test_phonetic_type_text(self, data: dict, phonetics_from_word: typing.List[Phonetic]):
        texts_from_data = [phonetic_data['text'] for phonetic_data in data['phonetics']]
        texts_from_phonetic_type = [phonetic.text for phonetic in phonetics_from_word]

        assert texts_from_phonetic_type == texts_from_data

    def test_phonetic_type_audio(self, data: dict, phonetics_from_word: typing.List[Phonetic]):
        audios_from_data = [phonetic_data['audio'] for phonetic_data in data['phonetics']]
        audios_from_phonetic_type = [phonetic.audio for phonetic in phonetics_from_word]

        assert audios_from_phonetic_type == audios_from_data

    # # types.Meaning  -------------------------------------------------------------------------------------------------

    def test_meaning_type_part_of_speech(self, data: dict, meanings_from_word: typing.List[Meaning]):
        parts_of_speech_from_data = [meaning_data['partOfSpeech'] for meaning_data in data['meanings']]
        parts_of_speech_from_meaning_type = [meaning.part_of_speech for meaning in meanings_from_word]

        assert parts_of_speech_from_meaning_type == parts_of_speech_from_data

    def test_meaning_type_definitions(self, data: dict, meanings_from_word: typing.List[Meaning]):
        definitions_from_data = [
            [
                Definition(definition_data) for definition_data in meaning_data['definitions']
            ]
            for meaning_data in data['meanings']
        ]
        definitions_from_meaning_type = [meaning.definitions for meaning in meanings_from_word]

        assert definitions_from_meaning_type == definitions_from_data

    # # types.Definition  ----------------------------------------------------------------------------------------------

    def test_definition_type_definition(self, data: dict,
                                        definitions_from_meanings: typing.List[typing.List[Definition]]
                                        ):
        definitions_from_data = [
            definition['definition']
            for meaning in data['meanings']
            for definition in meaning['definitions']
        ]
        definitions_from_definition_type = [
            definition.definition
            for definitions in definitions_from_meanings
            for definition in definitions
        ]

        assert definitions_from_definition_type == definitions_from_data

    def test_definition_type_synonyms(self, data: dict, definitions_from_meanings: typing.List[typing.List[Definition]]
                                      ):
        synonyms_from_data = [
            definition.get('synonyms')
            for meaning in data['meanings']
            for definition in meaning['definitions']
        ]
        synonyms_from_definition_type = [
            definition.synonyms
            for definitions in definitions_from_meanings
            for definition in definitions
        ]

        assert synonyms_from_definition_type == synonyms_from_data

    def test_definition_type_example(self, data: dict, definitions_from_meanings: typing.List[typing.List[Definition]]):
        examples_from_data = [
            definition.get('example')
            for meaning in data['meanings']
            for definition in meaning['definitions']
        ]
        examples_from_definition_type = [
            definition.example
            for definitions in definitions_from_meanings
            for definition in definitions
        ]

        assert examples_from_definition_type == examples_from_data

    # Absolute value from json response == property value from parser or type-------------------------------------------

    def test_hello_word_type_word(self, word_from_data: Word):
        expected = 'hello'
        fact = word_from_data.word

        assert fact == expected

    def test_hello_phonetics_type_text(self, phonetics_from_word: typing.List[Phonetic]):
        expected = [phonetic.text for phonetic in phonetics_from_word]
        fact = [
            '/həˈloʊ/',
            '/hɛˈloʊ/'
        ]

        assert fact == expected

    def test_hello_phonetics_type_audio(self, phonetics_from_word: typing.List[Phonetic]):
        expected = [phonetic.audio for phonetic in phonetics_from_word]
        fact = [
            'https://lex-audio.useremarkable.com/mp3/hello_us_1_rr.mp3',
            'https://lex-audio.useremarkable.com/mp3/hello_us_2_rr.mp3'
        ]

        assert fact == expected

    def test_hello_meanings_type_part_of_speech(self, meanings_from_word: typing.List[Meaning]):
        expected = [meaning.part_of_speech for meaning in meanings_from_word]
        fact = [
            'exclamation',
            'noun',
            'intransitive verb'
        ]

        assert fact == expected

    def test_hello_definition_type_definition(self, definitions_from_meanings: typing.List[typing.List[Definition]]):
        expected = [
            definition.definition
            for meanings_definition in definitions_from_meanings
            for definition in meanings_definition
        ]
        fact = [
            'Used as a greeting or to begin a phone conversation.',
            'An utterance of “hello”; a greeting.',
            'Say or shout “hello”; greet someone.'
        ]

        assert fact == expected

    def test_hello_definition_type_example(self, definitions_from_meanings: typing.List[typing.List[Definition]]):
        expected = [
            definition.example
            for meanings_definition in definitions_from_meanings
            for definition in meanings_definition
        ]
        fact = [
            'hello there, Katie!',
            'she was getting polite nods and hellos from people',
            'I pressed the phone button and helloed'
        ]

        assert fact == expected

    def test_hello_definition_type_synonyms(self, definitions_from_meanings: typing.List[typing.List[Definition]]):
        expected = [
            definition.synonyms
            for meanings_definition in definitions_from_meanings
            for definition in meanings_definition
        ]
        fact = [
            None,
            [
                'greeting',
                'welcome',
                'salutation',
                'saluting',
                'hailing',
                'address',
                'hello',
                'hallo',
            ],
            None
        ]

        assert fact == expected


class TestErrorResponseParsing:
    """
    Contains tests for
        * error response parser (``DictionaryApiErrorParser``);
        * types (``Error``).

    Checking that parser and types data
    equal real data that loaded from response json.
    """

    # fixtures----------------------------------------------------------------------------------------------------------

    @pytest.fixture(name='response', scope='class')
    def fixture_api_error_404_response(self) -> dict:
        """ API error response with 404 status loaded in python object """
        # for json data is used result of the API request with nonexistent word
        # (like: 'blablablablabla')
        json_file_path = DATA_DIR / 'error_404_API_response.json'
        with open(json_file_path, 'r', encoding='utf-8') as file:
            response = json.load(file)

        return response

    @pytest.fixture(name='data', scope='class')
    def fixture_data_from_response(self, response: dict) -> dict:
        """ Data of the API response """
        # for base response parsing behaviour repetition
        # here is also used ``data`` property
        data = response

        return data

    @pytest.fixture(name='parser', scope='class')
    def fixture_parser_from_response(self, response: dict) -> DictionaryApiErrorParser:
        """ Data of the API response """
        # indicate 404 Not Found error as error argument for parser
        parser = DictionaryApiErrorParser(404, response)

        return parser

    @pytest.fixture(name='error', scope='class')
    def fixture_error_from_data(self, data: dict) -> Error:
        """ Data of the API response """
        error = Error(data)

        return error

    # tests ------------------------------------------------------------------------------------------------------------

    # # parsers.DictionaryApiErrorParser--------------------------------------------------------------------------------

    def test_parser_error_title(self, parser: DictionaryApiErrorParser, error: Error):
        error_title_from_error = error.title
        error_title_from_parser = parser.title

        assert error_title_from_error == error_title_from_error

    def test_parser_error_message(self, parser: DictionaryApiErrorParser, error: Error):
        error_message_from_error = error.message
        error_message_from_parser = parser.message

        assert error_message_from_parser == error_message_from_error

    def test_parser_error_resolution(self, parser: DictionaryApiErrorParser, error: Error):
        error_resolution_from_error = error.resolution
        error_resolution_from_parser = parser.resolution

        assert error_resolution_from_parser == error_resolution_from_error

    # # types.Error ----------------------------------------------------------------------------------------------------

    def test_error_type_title(self, error: Error, data: dict):
        title_from_data = data.get('title')
        title_from_error = error.title

        assert title_from_error == title_from_data

    def test_error_type_message(self, error: Error, data: dict):
        message_from_data = data.get('message')
        message_from_error = error.message

        assert message_from_error == message_from_data

    def test_error_type_resolution(self, error: Error, data: dict):
        resolution_from_data = data.get('resolution')
        resolution_from_error = error.resolution

        assert resolution_from_error == resolution_from_data

    # Absolute value from json response == property value from parser or type-------------------------------------------

    def test_404_error_title(self, error: Error):
        fact = 'No Definitions Found'
        expected = error.title

        assert expected == fact

    def test_404_error_message(self, error: Error):
        fact = "Sorry pal, we couldn't find definitions for the word you were looking for."
        expected = error.message

        assert expected == fact

    def test_404_error_resolution(self, error: Error):
        fact = 'You can try the search again at later time or head to the web instead.'
        expected = error.resolution

        assert expected == fact
