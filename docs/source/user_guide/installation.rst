Installation Guide
==================

Using PIP
^^^^^^^^^

    .. code-block:: bash

        $ pip install python-freeDictionaryAPI

    To install package with extra requirements for **one of the client**:

        - for synchronous client that uses ``httpx``:

        .. code-block:: bash

            $ pip install python-freeDictionaryAPI[sync-client]

        - for asynchronous client that uses ``aiohttp``:

        .. code-block:: bash

            $ pip install python-freeDictionaryAPI[async-client]

Using Pipenv
^^^^^^^^^^^^

    .. code-block:: bash

        $ pipenv install python-freeDictionaryAPI
        $ pipenv install python-freeDictionaryAPI[sync-client]
        $ pipenv install python-freeDictionaryAPI[async-client]


.. note::

    To import package use ``freedictionaryapi``.