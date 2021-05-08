"""
Contains dictionary API parsers.

.. class:: DictionaryApiParser
    Implements dictionary API parser
.. class:: DictionaryApiErrorParser
    Implements dictionary API error parser
"""

import reprlib
from typing import Union

from .types import (
    Definition,
    Error,
    Phonetic,
    Meaning,
    Word
)


__all__ = ['DictionaryApiParser', 'DictionaryApiErrorParser']


class DictionaryApiParser:
    """
    Implements dictionary API parser.
    Parses from API json response in ``ParsedObject`` types.

    For getting data like from simple API response
    but with fields hinting: get ``Word`` object with ``word`` property
    and navigate through.

    For getting some sample data quickly
    it is possible to use some of prepared methods and properties.


    .. attr:: _response list: API json response in python representation
    .. attr:: _data dict: data for parsing actually
    .. attr:: _word Word: parsed object that contains word info

    .. property:: word(self) -> Word
    .. property:: phonetics(self) -> list[Phonetic]
    .. property:: meanings(self) -> list[Meaning]

    .. method:: _get_all_definitions_as_parsed_objects(self) -> list[Definition]
        Get definitions as parsed objects (for DRY in getting examples, synonyms and definitions actually)

    .. method:: get_transcription(self) -> str
        Get transcription (if few fetched return first)
    .. method:: get_all_transcriptions(self) -> list[str]
        Get all transcriptions
    .. method:: get_link_on_audio_with_pronunciation(self) -> str
        Get link on audio with pronunciation (if few fetched return first)
    .. method:: get_all_parts_of_speech(self) -> list[str]
        Get all parts of speech
    .. method:: get_all_definitions(self) -> list[str]
        Get all definitions (sentences, phrases that express meaning of the word)
    .. method:: get_all_examples(self) -> list[str]
        Get all examples of word usage
    .. method:: get_all_synonyms(self) -> list[str]
        Get all synonyms
    """

    def __init__(self, response: Union[dict, list]) -> None:
        """
        Parse API response that loaded in python object (json.load/s).

        ``response`` has type ``list``
        since in response we have such format
        and simpler would be just
        with the web library do like this:
        ``response.json()`` -  to get python object loaded from json.

        :param response: API json response in python representation
        :type response: Union[dict, list]
        """

        self._response: Union[dict, list] = response

        if isinstance(self._response, list):
            self._data: dict = self._response[0]
        elif isinstance(self._response, dict):
            self._data: dict = self._response
        else:
            message = (
                'API json response contains unsupported type. '
                'Expected to get <list> or <dict>! '
                f'Got {self._response!r}'
            )
            raise TypeError(message)

        #
        # assert 'word' in self._data
        #

        self._word: Word = Word(self._data)

    def __repr__(self) -> str:
        return f'DictionaryApiParser(response={reprlib.repr(self._response)})'

    @property
    def word(self) -> Word:
        """ Get word object """
        return self._word

    @property
    def phonetics(self) -> list[Phonetic]:
        """ Get phonetics data. Shortcut for ``word.phonetics`` """
        return self._word.phonetics

    @property
    def meanings(self) -> list[Meaning]:
        """ Get meanings data. Shortcut for ``word.meanings`` """
        return self._word.meanings

    def _get_all_definitions_as_parsed_objects(self) -> list[Definition]:
        """ Get list of all definitions (as parsed object) """
        definitions = [
            definition
            for meaning in self.meanings
            for definition in meaning.definitions
        ]

        return definitions

    # Phonetic section -------------------------------------------------------------------------------------------------

    def get_transcription(self) -> str:
        """ Get transcription. If in response fetched few then return first """
        phonetic = self.phonetics[0]
        transcription = phonetic.text

        return transcription

    def get_all_transcriptions(self) -> list[str]:
        """ Get all transcriptions that fetched in response """
        transcriptions = [phonetic.text for phonetic in self.phonetics]

        return transcriptions

    def get_link_on_audio_with_pronunciation(self) -> str:
        """
        Get link on audio with pronunciation. If in response fetched few return first.
        For more detailed (get few links) use ``phonetics`` property - it`ll be more convenient and simple.
        """

        phonetic = self.phonetics[0]
        link_on_audio = phonetic.audio

        return link_on_audio

    # Meaning section --------------------------------------------------------------------------------------------------

    def get_all_parts_of_speech(self) -> list[str]:
        """ Get all parts of speech """
        parts_of_speech = [meaning.part_of_speech for meaning in self.meanings]

        return parts_of_speech

    def get_all_definitions(self) -> list[str]:
        """ Get all definitions [phrases that telling meaning of the word] """
        definitions = [definition.definition for definition in self._get_all_definitions_as_parsed_objects()]

        return definitions

    def get_all_examples(self) -> list[str]:
        """ Get all examples of word usage """
        examples = [definition.example for definition in self._get_all_definitions_as_parsed_objects()]

        return examples

    def get_all_synonyms(self) -> list[str]:
        """ Get all synonyms """
        # create synonyms with ``set`` to get unique synonyms
        synonyms = {
            synonym
            for definition in self._get_all_definitions_as_parsed_objects()
            if definition.synonyms
            for synonym in definition.synonyms
        }
        # convert in list for simplicity
        synonyms = list(synonyms)

        return synonyms


class DictionaryApiErrorParser:
    """
    Implements dictionary API error parser.

    Contains useful ``get_formatted_error_message`` that
    return pretty formatted error message.

    .. attrs:: _status_code int: response status code
    .. attrs:: _response dict: API json response in python representation
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
        Parse API error response.

        :param status_code: http status code
        :type status_code: int
        :param response: API json response in python representation
        :type response: dict
        """

        self._status_code = status_code
        self._response = response
        # For the same behaviour as in the ``DictionaryApiParser``
        # where in API response returned list, we save some attrs:
        # * response - loaded json response;
        # * data - actually data for parsing (supposed to be simple ``dict``).
        # In case of ``DictionaryApiParser`` we have to get first element of returned list.
        # Here we just repeat the same behaviour.
        self._data = self._response

        self._error = Error(self._data)

    def __repr__(self) -> str:
        return f'DictionaryApiErrorParser(status_code={self._status_code})'

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
