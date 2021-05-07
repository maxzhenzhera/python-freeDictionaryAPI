"""
Contains dictionary API parser.

.. class:: DictionaryApiParser
    Implements dictionary API parser
"""

import reprlib

from .types import (
    Definition,
    Phonetic,
    Meaning,
    Word
)


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
    .. attr:: _data dict: actually data of API json response (element from list)
    .. attr:: _word Word: ``Word`` object

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

    def __init__(self, response: list) -> None:
        """
        Parse API response that loaded in python object (json.load/s).

        ``response`` has type ``list``
        since in response we have such format
        and simpler would be just
        with the web library do like this:
        ``response.json()`` -  to get python object loaded from json.

        :param response: API json response in python representation
        :type response: list
        """

        self._response: list = response
        self._data: dict = self._response[0]

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
