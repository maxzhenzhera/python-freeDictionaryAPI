"""
Contains dictionary API response parser.

.. class:: DictionaryApiParser
"""

from typing import Union

from .base_parser import BaseDictionaryApiParser
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
    Parses from API json response in :obj:`ParsedObject` types.

    For getting data like from simple API response
    but with fields hinting: get :obj:`Word`` object with :obj:`DictionaryApiParser.word` property
    and navigate through.

    For getting some sample data quickly
    it is possible to use some of prepared methods and properties.
    """

    def __init__(self, response: Union[dict, list]) -> None:
        """
        Init dictionary API parser response intsance.
        Parse API response.

        ``response`` has type :obj:`Union[dict, list]`
        since in response we have such format
        and simpler would be just
        with the web library do like this:
        ``response.json()`` -  to get python object loaded from json.

        :param response: API json response loaded in python object
        :type response: :obj:`Union[dict, list]`
        """

        super().__init__(response)

        if isinstance(self._response, list):
            self._data: dict = self._response[0]
        elif isinstance(self._response, dict):
            # if accidentally has been passed
            # ``dict`` as response object
            # we handle this
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
        """
        :return: API response data
        :rtype: :obj:`dict`
        """
        return self._data

    @property
    def word(self) -> Word:
        """
        :return: word object
        :rtype: :obj:`Word`
        """

        return self._word

    @property
    def phonetics(self) -> list[Phonetic]:
        """
        Phonetics data. Shortcut for :obj:`Word.phonetics`

        :return: phonetics data
        :rtype: :obj:`list[Phonetic]`
        """

        return self._word.phonetics

    @property
    def meanings(self) -> list[Meaning]:
        """
        Meanings data. Shortcut for :obj:`Word.meanings`

        :return: meanings data
        :rtype: :obj:`list[Meaning]`
        """

        return self._word.meanings

    def _get_all_definitions_as_parsed_objects(self) -> list[Definition]:
        """
        Get list of all definitions (as :obj:`ParsedObject`)

        :return: list of definitions as parsed objects
        :rtype: :obj:`list[Definition]`
        """

        definitions = [
            definition
            for meaning in self.meanings
            for definition in meaning.definitions
        ]

        return definitions

    # Phonetic section -------------------------------------------------------------------------------------------------

    def get_transcription(self) -> str:
        """
        Get transcription. If in response fetched few then return first

        :return: transcription
        :rtype: :obj:`str`
        """

        phonetic = self.phonetics[0]
        transcription = phonetic.text

        return transcription

    def get_all_transcriptions(self) -> list[str]:
        """
        Get all transcriptions that fetched in response

        :return: list of transcriptions
        :rtype: :obj:`list[str]`
        """

        transcriptions = [phonetic.text for phonetic in self.phonetics]

        return transcriptions

    def get_link_on_audio_with_pronunciation(self) -> str:
        """
        Get link on audio with pronunciation. If in response fetched few return first.
        For more detailed (get few links) use :obj:`Word.phonetics` property - it`ll be more convenient and simpler.

        :return: link on audio with pronunciation
        :rtype: :obj:`str`
        """

        phonetic = self.phonetics[0]
        link_on_audio = phonetic.audio

        return link_on_audio

    # Meaning section --------------------------------------------------------------------------------------------------

    def get_all_parts_of_speech(self) -> list[str]:
        """
        Get all parts of speech

        :return: all parts of speech
        :rtype: :obj:`list[str]`
        """

        parts_of_speech = [meaning.part_of_speech for meaning in self.meanings]

        return parts_of_speech

    def get_all_definitions(self) -> list[str]:
        """
        Get all definitions (phrases that telling meaning of the word)

        :return: list of definitions
        :rtype: :obj:`list[str]`
        """

        definitions = [definition.definition for definition in self._get_all_definitions_as_parsed_objects()]

        return definitions

    def get_all_examples(self) -> list[str]:
        """
        Get all examples of word usage

        :return: list of examples
        :rtype: :obj:`list[str]`
        """

        examples = [definition.example for definition in self._get_all_definitions_as_parsed_objects()]

        return examples

    def get_all_synonyms(self) -> list[str]:
        """
        Get all synonyms

        :return: list of synonyms
        :rtype: :obj:`list[str]`
        """

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
