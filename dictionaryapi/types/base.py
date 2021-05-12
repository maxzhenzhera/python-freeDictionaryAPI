"""
Contains base types.

.. class:: ParsedObject(abc.ABC)
    Implements base parsed object (part of API json response)
"""

import abc


__all__ = ['ParsedObject']


class ParsedObject(abc.ABC):
    """
    Implements base parsed object.
    Means part of API json response that is structured by category and has inner fields.

    Class gives convenient base for inheriting
    and creating more concrete types,
    so inherited classes parse more detailed information.

    Must be inherited since it is abstract.

    For example, in response of dictionary API it might be:
        - phonetics;
        - meanings;
        - definitions.

    Considering that simple response might look like that (copied from https://dictionaryapi.dev/):
    ```json
    [
        {
          "word": "hello",
          "phonetics": [
            {
              "text": "/həˈloʊ/",
              "audio": "https://lex-audio.useremarkable.com/mp3/hello_us_1_rr.mp3"
            },
            {
              "text": "/hɛˈloʊ/",
              "audio": "https://lex-audio.useremarkable.com/mp3/hello_us_2_rr.mp3"
            }
          ],
          "meanings": [
            {
              "partOfSpeech": "exclamation",
              "definitions": [
                {
                  "definition": "Used as a greeting or to begin a phone conversation.",
                  "example": "hello there, Katie!"
                }
              ]
            },
            {
              "partOfSpeech": "noun",
              "definitions": [
                {
                  "definition": "An utterance of “hello”; a greeting.",
                  "example": "she was getting polite nods and hellos from people",
                  "synonyms": [
                    "greeting",
                    "welcome",
                    "salutation",
                    "saluting",
                    "hailing",
                    "address",
                    "hello",
                    "hallo"
                  ]
                }
              ]
            },
            {
              "partOfSpeech": "intransitive verb",
              "definitions": [
                {
                  "definition": "Say or shout “hello”; greet someone.",
                  "example": "I pressed the phone button and helloed"
                }
              ]
            }
          ]
        }
    ]
    ```

    .. attr:: _data dict: part of API json response
    """

    def __init__(self, data: dict) -> None:
        """
        Get data presented in python ``dict`` and set it in instance (with ``_data`` param).

        :param data: part of API json response
        :type data: dict
        """

        self._data = data

    def __eq__(self, other: 'ParsedObject') -> bool:
        if not isinstance(other, ParsedObject):
            class_name = self.__class__.__name__
            raise TypeError(f'{class_name} can not be compared with instance of the other type: {other!r}')

        equality = self._data == other._data

        return equality
