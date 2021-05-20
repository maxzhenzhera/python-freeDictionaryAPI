Base clients
============

.. toctree::
    :caption: Contents

    base_sync_client
    base_async_client


Here is 2 base API clients, abstract clients that
might be inherited and overridden as you wish:

    1. **synchronous** :obj:`freedictionaryapi.clients.BaseDictionaryApiClient`
    2. **asynchronous** :obj:`freedictionaryapi.clients.BaseAsyncDictionaryApiClient`

Here is list of the base clients.
All you need to implement your own
client it is to implement one method
of the chosen base
(no matter ``sync`` or ``async`` since both abstracts are prepared):

    - :obj:`freedictionaryapi.clients.BaseDictionaryApiClient.fetch_api_response`
    - :obj:`freedictionaryapi.clients.BaseAsyncDictionaryApiClient.fetch_api_response`

Method`s goals are very simple:
    - fetch response that json-ized (something like ``response.json()``);
    - get response status code;
    - put it in right order in one tuple.

See notes of particular class about this method.


.. seealso:: :class:`freedictionaryapi.clients.base_client_interface.BaseDictionaryApiClientInterface`
