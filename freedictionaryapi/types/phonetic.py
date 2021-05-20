"""
Contains phonetic type.

.. class Phonetic(ParsedObject)
"""

from .base import ParsedObject


__all__ = ['Phonetic']


class Phonetic(ParsedObject):
    """
    Implements the object of API json response
    that consists of phonetics data:

        * text - transcription;
        * audio - links on pronunciation (mp3 audio file).
    """

    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        return f'{class_name}(text={self.text!r}, audio={self.audio!r})'

    @property
    def text(self) -> str:
        """
        :return: text of phonetic (transcription)
        :rtype: :obj:`str`
        """
        text: str = self._data.get('text')

        return text

    @property
    def audio(self) -> str:
        """
        :return: audio of phonetic (link on audio .mp3)
        :rtype: :obj:`str`
        """

        audio: str = self._data.get('audio')

        return audio

    # aliases ----------------------------------------------------------------------------------------------------------

    @property
    def transcription(self) -> str:
        """
        Alias of :obj:`Phonetic.text` property

        :return: transcription
        :rtype: :obj:`str`
        """

        return self.text

    @property
    def link_on_audio_with_pronunciation(self) -> str:
        """
        Alias of :obj:`Phonetic.audio` property

        :return: link on audio (.mp3) with pronunciation
        :rtype: :obj:`str`
        """

        return self.audio
