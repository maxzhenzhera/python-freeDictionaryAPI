Quick Start
===========

Let`s start:

    .. note::

    1. import client
       (here I use synchronous client for simplicity; **httpx** is required)

    .. code-block:: python

        >>> from freedictionaryapi.clients.sync_client import DictionaryApiClient

    2. init simple instance of client
       (it is possible to set manually created **httpx** client on initialization)

    .. code-block:: python

        # it is possible to set
        # default language for entire client
        # by default: American English
        >>> client = DictionaryApiClient()

    3. fetch :obj:`freedictionaryapi.parsers.response_parser.DictionaryApiParser` parser

    .. code-block:: python

        # it is also possible to set
        # language for request
        # we`ll see this some later

        # IMPORTANT:
        # each method that makes API request
        # have to be handled of API errors
        # that are raised if API response is unsuccessful
        >>> from freedictionaryapi.errors import DictionaryApiError

        # so, handle errors...
        >>> try:
        ...     parser = client.fetch_parser('hello')
        ... except DictionaryApiError:
        ...     print('API error')

    4. working with parser object and get all needed info
       (see examples of parsing features in examples section)

    .. code-block:: python

        >>> parser.get_transcription()
        '/həˈloʊ/'
        >>> parser.get_link_on_audio_with_pronunciation()
        'https://lex-audio.useremarkable.com/mp3/hello_us_1_rr.mp3'
        >>> parser.get_all_definitions()
        ['An utterance of “hello”; a greeting.', 'Say or shout “hello”; greet someone.', 'Used as a greeting or to begin a phone conversation.']
        >>> parser.get_all_synonyms()
        ['saluting', 'salutation', 'address', 'greeting', 'hello', 'hailing', 'welcome', 'hallo']
        # here we get :obj:`freedictionaryapi.types.word.Word` object
        >>> word = parser.word
        # and now we can just navigate throw word object properties
        >>> word.word
        'hello'
        >>> for phonetic in word.phonetics:
        ...     print(phonetic)
        Phonetic(text='/həˈloʊ/', audio='https://lex-audio.useremarkable.com/mp3/hello_us_1_rr.mp3')
        Phonetic(text='/hɛˈloʊ/', audio='https://lex-audio.useremarkable.com/mp3/hello_us_2_rr.mp3')
        >>> for meaning in word.meanings:
        ...     print(meaning.part_of_speech)
        ...     for definition in meaning.definitions:
        ...             print(definition)
        noun
        Definition(definition='An utterance of “hello”; a greeting.', example='she was getting polite nods and hellos from people', synonyms=['greeting', 'welcome', 'salutation', 'saluting', 'hailing', 'address', 'hello', 'hallo'])

        intransitive verb
        Definition(definition='Say or shout “hello”; greet someone.', example='I pressed the phone button and helloed', synonyms=None)

        exclamation
        Definition(definition='Used as a greeting or to begin a phone conversation.', example='hello there, Katie!', synonyms=None)

    5. or if you wish we can immediately get word object

    .. code-block:: python

        # here is also possible
        # to set language for request
        >>> try:
        ...     word = client.fetch_word('small')
        ... except DictionaryApiError:
        ...     print('API error')
        ... else:
        ...     for phonetic in word.phonetics:
        ...         print(phonetic)
        Phonetic(text='/smɔl/', audio='https://lex-audio.useremarkable.com/mp3/small_us_6.mp3')

    6. about other language usage

    .. code-block:: python

        # let`s learn Italian some :)
        >>> from freedictionaryapi.languages import LanguageCodes
        # supported languages:
        >>> for language in LanguageCodes:
        ...     print(language)
        LanguageCodes.ARABIC
        LanguageCodes.BRAZILIAN_PORTUGUESE
        LanguageCodes.ENGLISH_UK
        LanguageCodes.ENGLISH_US
        LanguageCodes.FRENCH
        LanguageCodes.GERMAN
        LanguageCodes.HINDI
        LanguageCodes.ITALIAN
        LanguageCodes.JAPANESE
        LanguageCodes.KOREAN
        LanguageCodes.RUSSIAN
        LanguageCodes.SPANISH
        LanguageCodes.TURKISH
        # and request with new language...
        # do not forget to handle errors!
        >>> parser = client.fetch_parser('ciao', LanguageCodes.ITALIAN)
        >>> parser.get_transcription()
        'cià·o'
        >>> parser.get_all_definitions()
        ['Voce confidenziale di saluto; anche come s.m. ( invar. ).']

    7. do not forget to close client

    .. code-block:: python

        >>> client.close()

