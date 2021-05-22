Base clients
============

.. toctree::
    :maxdepth: 2
    :caption: Contents

    base_sync_client
    base_async_client


Here is 2 base API clients. Abstract clients that
might be inherited and overridden:

    1. **synchronous** :obj:`freedictionaryapi.clients.BaseDictionaryApiClient`
    2. **asynchronous** :obj:`freedictionaryapi.clients.BaseAsyncDictionaryApiClient`

All you need to implement your own
client it is to implement one method
of the chosen base:

    - :meth:`freedictionaryapi.clients.BaseDictionaryApiClient.fetch_api_response`
    - :meth:`freedictionaryapi.clients.BaseAsyncDictionaryApiClient.fetch_api_response`

Method`s goals are very simple:
    - fetch response that JSON-ized (something like ``response.json()``);
    - get response status code;
    - put it in right order in one tuple.

See notes of particular class about this method.


.. seealso:: :class:`freedictionaryapi.clients.base_client_interface.BaseDictionaryApiClientInterface`
