"""
`httpx` package is required.
Since synchronous client is powered by `httpx.Client`.
"""

import logging

# module is requiring external dependency:
# so it can not be set in __init__ files
# for easier importing
from freedictionaryapi.clients.sync_client import DictionaryApiClient
from freedictionaryapi.errors import DictionaryApiError
# or `from freedictionaryapi import DictionaryApiError`
from freedictionaryapi.languages import LanguageCodes
# or `from freedictionaryapi import LanguageCodes`


def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)

    # on initializing might be passed
    # # - one of supported languages (listed in LanguageCodes enum that imported above)
    # # - manually created httpx.Client
    client = DictionaryApiClient()

    # client have to be closed after all work
    # like in the same way we close our
    # web libraries` clients/sessions

    # # it might be done with try-finally block
    try:
        # before watching of client methods
        # important note:
        # # each method that under hood
        # # uses HTTP request to API
        # # might raise correspond API error
        # # if one has been occurred
        # # so, you have to handle exceptions
        # # that might be raised during processing.
        # # for this we`ve imported errors above
        # # for now, we`ll catch API errors with one
        # # the big-scaled (common for all errors) exception
        # # DictionaryApiError

        # so, go next...

        # # in client`s methods we have to pass word
        # that we actually are searching info about
        # and also
        # if word`s language not the client default one
        # we can pass it manually

        # 1. default language
        word = 'hello'

        # # do not forger about errors handling
        try:
            parser = client.fetch_parser(word)
        except DictionaryApiError:
            logger.error('Oops! Here I might do some stuff for errors handling!')
        else:
            # parser has a lot of different data
            # to explore see parser example and docs
            word_transcription = parser.get_transcription()
            print(f'Transcription of the word <{word}> is: {word_transcription}.')

        # 2. set language for the particular word
        word = 'привет'
        language = LanguageCodes.RUSSIAN

        try:
            parser = client.fetch_parser(word, language)
        except DictionaryApiError:
            logger.error('Oops! Here I might do some stuff for errors handling!')
        else:
            word_definitions = parser.get_all_definitions()
            word_definitions_formatted_string = '; '.join(word_definitions)
            print(f'Definition[s] of the word <{word}> is/are: {word_definitions_formatted_string}')

    finally:
        client.close()

    # # or with implemented context manager
    # # Note:
    # # on each usage of this context manager
    # # you init new instance -> init new web client instance
    # # so, client supposed to be created once for all program
    with DictionaryApiClient() as client:
        word = 'queue'
        try:
            # here instead of the parser
            # we fetch word object
            # that implements clear API JSON response
            word = client.fetch_word(word)
        except DictionaryApiError:
            logger.error('Oops! Here I might do some stuff for errors handling!')
        else:
            print(f'Audio links of the word <{word}>:')
            for phonetic in word.phonetics:
                print(phonetic.audio)

    # # # ---------------------------
    # so, the most important methods are:
    # - .fetch_parser() - that returns parser object
    # - .fetch_word() - that returns word object
    # also, it is some more methods
    # but there are the most often needed
    # since they implement high-level API
    # that you want to use to


if __name__ == '__main__':
    main()
