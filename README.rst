Welcome to python-freeDictionaryAPI!
====================================

.. image:: https://img.shields.io/pypi/v/python-freeDictionaryAPI?style=flat-square
    :target: https://pypi.org/project/python-freeDictionaryAPI/
    :alt: PyPI

.. image:: https://img.shields.io/pypi/pyversions/python-freeDictionaryAPI?style=flat-square
    :target: https://pypi.org/project/python-freeDictionaryAPI/
    :alt: PyPI - Python Version

.. image:: https://img.shields.io/pypi/dm/python-freeDictionaryAPI?style=flat-square
    :target: https://pypi.org/project/python-freeDictionaryAPI/
    :alt: PyPI - Downloads

.. image:: https://img.shields.io/readthedocs/python-freedictionaryapi?style=flat-square
    :target: https://python-freedictionaryapi.readthedocs.io/
    :alt: Read the Docs

.. image:: https://img.shields.io/website?down_message=API%60s%20failed&style=flat-square&up_message=API%60s%20working&url=https%3A%2F%2Fdictionaryapi.dev%2F
    :target: https://dictionaryapi.dev/
    :alt: API`s working

.. image:: https://img.shields.io/pypi/l/python-freeDictionaryAPI?style=flat-square
    :target: https://pypi.org/project/python-freeDictionaryAPI/
    :alt: PyPI - License

.. image:: https://img.shields.io/github/issues/Max-Zhenzhera/python-freeDictionaryAPI?style=flat-square
    :target: https://github.com/Max-Zhenzhera/python-freeDictionaryAPI/issues
    :alt: GitHub issues


**python-freeDictionaryAPI** is a wrapper for `Free Dictionary API <https://dictionaryapi.dev/>`_.

Library is simple, light and uses very cool fully free dictionary API.

Library components can be used with high level API (clients)
or if you wish so
you can use only some implemented parts that you`re interested in (like URL generating, parsers, ...).

Implemented synchronous and asynchronous clients
that powered with
`httpx <https://pypi.org/project/httpx/>`_
and
`aiohttp <https://pypi.org/project/aiohttp/>`_
accordingly.

If you do not prefer to use implemented clients
and want to use some other web lib.
So, it is synchronous and asynchronous base clients for inheriting.
All you need it is to implement one method that makes
**HTTP request**.

You can `read the docs here <https://python-freedictionaryapi.readthedocs.io/>`_.


Installation
^^^^^^^^^^^^

.. code-block:: bash

        $ pip install python-freeDictionaryAPI

To install package with extra requirements for **one of the client**:

    - for synchronous client that uses ``httpx``:

    .. code-block:: bash

        $ pip install python-freeDictionaryAPI[sync-client]

    - for asynchronous client that uses ``aiohttp``:

    .. code-block:: bash

        $ pip install python-freeDictionaryAPI[async-client]


Super Quick Start
^^^^^^^^^^^^^^^^^

.. code-block:: python

    >>> from freedictionaryapi.clients.sync_client import DictionaryApiClient
    >>> with DictionaryApiClient() as client:
    ...     parser = client.fetch_parser('hello')
    >>> word = parser.word
    >>> word.word
    'hello'
    >>> word.phonetics
    [Phonetic(text='/həˈloʊ/', audio='https://lex-audio.useremarkable.com/mp3/hello_us_1_rr.mp3'), Phonetic(text='/hɛˈloʊ/', audio='https://lex-audio.useremarkable.com/mp3/hello_us_2_rr.mp3')]
    >>> for meaning in word.meanings:
    ...     print(meaning.part_of_speech)
    ...     for definition in meaning.definitions:
    ...             orint(definition)
    ...     print()
    noun
    Definition(definition='An utterance of “hello”; a greeting.', example='she was getting polite nods and hellos from people', synonyms=['greeting', 'welcome', 'salutation', 'saluting', 'hailing', 'address', 'hello', 'hallo'])

    intransitive verb
    Definition(definition='Say or shout “hello”; greet someone.', example='I pressed the phone button and helloed', synonyms=None)

    exclamation
    Definition(definition='Used as a greeting or to begin a phone conversation.', example='hello there, Katie!', synonyms=None)
    >>> parser.get_transcription()
    '/həˈloʊ/'
    >>> parser.get_link_on_audio_with_pronunciation()
    'https://lex-audio.useremarkable.com/mp3/hello_us_1_rr.mp3'
    >>> parser.get_all_definitions()
    ['An utterance of “hello”; a greeting.', 'Say or shout “hello”; greet someone.', 'Used as a greeting or to begin a phone conversation.']
    >>> parser.get_all_synonyms()
    ['hello', 'hailing', 'welcome', 'address', 'salutation', 'hallo', 'saluting', 'greeting']
    >>> parser.get_all_examples()
    ['she was getting polite nods and hellos from people', 'I pressed the phone button and helloed', 'hello there, Katie!']


API note
^^^^^^^^

`API that used in this library <https://dictionaryapi.dev/>`_
does not provide present of all fields in response.

So, **be aware**, when response is parsed
and some of the fields are empty in result -
in code they`ll be returning ``None``.


Developer
^^^^^^^^^
**Good luck!**
