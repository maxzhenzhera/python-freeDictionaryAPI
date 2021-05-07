"""
Contains phonetic type.

.. class Phonetic(ParsedObject)
    Implements phonetic type (info about phonetic)
"""

from .base import ParsedObject


__all__ = ['Phonetic']


class Phonetic(ParsedObject):
    """
    Implements the object of API json response
    that consists of phonetics data:
        * text - transcription;
        * audio - links on pronunciation (mp3 audio file).

    .. property:: text(self) -> str:
    .. property:: audio(self) -> str
            aliases of the properties above
    .. property:: transcription(self) -> str
    .. property:: link_on_audio_with_pronunciation(self) -> str
    """

    def __repr__(self) -> str:
        return f'Phonetic(text={self.text!r}, audio={self.audio!r})'

    @property
    def text(self) -> str:
        """ Get text of phonetic """
        text: str = self._data.get('text')

        return text

    @property
    def audio(self) -> str:
        """ Get link of audio (mp3) of phonetic """
        audio: str = self._data.get('audio')

        return audio

    # aliases ----------------------------------------------------------------------------------------------------------

    @property
    def transcription(self) -> str:
        """ Alias of ``text`` property """
        return self.text

    @property
    def link_on_audio_with_pronunciation(self) -> str:
        """ Alias of ``audio`` property """
        return self.audio
