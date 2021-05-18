"""
Contains dictionary API response parser.

.. class:: DictionaryApiParser
    Implements dictionary API response parser
"""

from typing import Union

from .base import BaseDictionaryApiParser
from ..types import (
    Definition,
    Phonetic,
    Meaning,
    Word
)


__all__ = ['DictionaryApiParser']


class DictionaryApiParser(BaseDictionaryApiParser):
    """
    Implements dictionary API response parser.
    Parses from API json response in ``ParsedObject`` types.

    For getting data like from simple API response
    but with fields hinting: get ``Word`` object with ``word`` property
    and navigate through.

    For getting some sample data quickly
    it is possible to use some of prepared methods and properties.


    .. attr:: _response Union[dict, list]: API json response loaded in python object
    .. attr:: _data dict: data for parsing actually
    .. attr:: _word Word: parsed object that contains word info

    .. property:: data(self) -> dict
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
        Init dictionary API parser.
        Parse API response.

        ``response`` has type ``list``
        since in response we have such format
        and simpler would be just
        with the web library do like this:
        ``response.json()`` -  to get python object loaded from json.

        :param response: API json response loaded in python object
        :type response: Union[dict, list]
        """

        super().__init__(response)

        if isinstance(self._response, list):
            self._data: dict = self._response[0]
        elif isinstance(self._response, dict):
            # if accidentally has been passed
            # ``dict`` as response object
            # we consider this
            self._data: dict = self._response
        else:
            message = (
                'API json response contains unsupported type. '
                'Expected to get <list> or <dict>! '
                f'Got {self._response!r}'
            )
            raise TypeError(message)

        self._word: Word = Word(self._data)

    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        word_title = self._word.word

        return f'{class_name}(word={word_title})'

    @property
    def data(self) -> dict:
        """ Get ``dict`` of the API response """
        return self._data

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
