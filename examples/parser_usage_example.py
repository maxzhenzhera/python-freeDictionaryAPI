"""
Detailed overlook of parser and types references.
"""

import freedictionaryapi


def main():
    # Note:
    # # look at https://dictionaryapi.dev/
    # # to understand structure of the API response
    # # and eventually of implemented types

    # firstly, fetch one parser to look on it
    with freedictionaryapi.DictionaryApiClient() as client:
        parser: freedictionaryapi.parsers.DictionaryApiParser = client.fetch_parser('hello')

    # simple navigating throw the API response
    # with implemented types
    word: freedictionaryapi.types.Word = parser.word

    # if you need wor object exactly - use .fetch_word() method

    # ---------------------------------------------------------

    # so, word:

    # # actually, word
    word_name: str = word.word
    print('{:*^20}'.format(' Word '))
    print(f'word = {word_name}')

    # # Phonetics section
    print('{:*^20}'.format(' Phonetic '))
    phonetics: list[freedictionaryapi.types.Phonetic] = word.phonetics
    for index, phonetic in enumerate(phonetics):
        index += 1

        text: str = phonetic.text
        # alias of the `text` - `transcription`
        audio: str = phonetic.audio
        # alias of the `audio` - `link_on_audio_with_pronunciation`
        print(f'{index}. text = {text}; audio = {audio}')

    # # Meanings section
    print('{:*^20}'.format(' Meaning '))
    meanings: list[freedictionaryapi.types.Meaning] = word.meanings
    for index_m, meaning in enumerate(meanings):
        index_m += 1

        part_of_speech: str = meaning.part_of_speech

        print(f'{index_m}. part of speech = {part_of_speech}')

        # # Definitions section
        definitions: list[freedictionaryapi.types.Definition] = meaning.definitions
        for index_d, definition in enumerate(definitions):
            index_d += 1
            # definition_= definition phrase that telling about meaning
            # naming is repeated by API response :)
            definition_: str = definition.definition
            synonyms: list[str] = definition.synonyms
            synonyms_joined_in_string = ', '.join(synonyms) if synonyms is not None else ''
            example: str = definition.example

            message = (
                f'\t{index_m}.{index_d}. '
                f'definition = {definition_}; synonyms = {synonyms_joined_in_string!r}; example = {example!r}'
            )
            print(message)

    # ---------------------------------------------------------

    # so, parser...

    # # we have some shortcuts
    phonetics: list[freedictionaryapi.types.Phonetic] = parser.phonetics    # parser.word.phonetics
    meanings: list[freedictionaryapi.types.Meaning] = parser.meanings      # # parser.word.meanings

    # # parser methods
    print('{:*^20}'.format(' Parser methods '))

    # # # some methods for phonetic section
    transcription: str = parser.get_transcription()
    print(f'.get_transcription() - {transcription!r}')
    all_transcriptions: list[str] = parser.get_all_transcriptions()
    print(f'.get_all_transcriptions() - {all_transcriptions!r}')
    link_on_audio_with_pronunciation: str = parser.get_link_on_audio_with_pronunciation()
    print(f'.get_link_on_audio_with_pronunciation() - {link_on_audio_with_pronunciation!r}')

    # # # some methods for meaning section
    all_parts_of_speech: list[str] = parser.get_all_parts_of_speech()
    print(f'.get_all_parts_of_speech() - {all_parts_of_speech!r}')
    all_definitions: list[str] = parser.get_all_definitions()
    print(f'.get_all_definitions() - {all_definitions!r}')
    all_examples: list[str] = parser.get_all_examples()
    print(f'.get_all_examples() - {all_examples!r}')
    all_synonyms: list[str] = parser.get_all_synonyms()
    print(f'.get_all_synonyms() - {all_synonyms!r}')


if __name__ == '__main__':
    main()
