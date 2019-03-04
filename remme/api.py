from random import random

import aiohttp_json_rpc

from remme.models.general.methods import RemmeMethods
from remme.models.interfaces.api import IRemmeAPI
from remme.utils import validate_node_config

DEFAULT_NETWORK_CONFIG = {
    'node_address': 'localhost:8080',
    'ssl_mode': False,
}


class RemmeAPI(IRemmeAPI):
    """
    Main class that send requests to our REMME protocol.

    Reference to the JSON-RPC API specification::
        - https://bit.ly/2DZ7iOG

    To use:
        .. code-block:: python

            from remme.api import RemmeAPI
            from remme.models.general.methods import RemmeMethods

            remme_api = await RemmeAPI({
                'node_address': 'localhost:8080',
                'ssl_mode': False
            })

            response = await remme_api.send_request(RemmeMethods.FETCH_BLOCK)
            print('response')
    """

    def __init__(self, network_config=DEFAULT_NETWORK_CONFIG):
        """
        Constructor can implement with different sets of params.

        By default params for constructor are: ``node_address = 'localhost:8080'``, ``ssl_mode = False``

        Args:
            network_config (dict): node_address (string), ssl_mode (boolean)

        To use:
            Implementation with all params.

            .. code-block:: python

                from remme.api import RemmeAPI
                remme_api = await RemmeAPI({
                    'node_address': 'localhost:8080',
                    'ssl_mode': False
                })

            Implementation with one param.

            .. code-block:: python

                from remme.api import RemmeAPI
                remme_api = await RemmeAPI({
                    'node_address': 'localhost:8080',
                })

            Implementation without params.

            .. code-block:: python

                from remme.api import RemmeAPI
                remme_api = await RemmeAPI()
        """
        if not network_config.get('node_address'):
            network_config['node_address'] = 'localhost:8080'

        if not network_config.get('ssl_mode'):
            network_config['ssl_mode'] = False

        validate_node_config(network_config=network_config)
        self._network_config = network_config

        self._rpc_client = aiohttp_json_rpc.JsonRpcClient()

    def _get_url_for_request(self):

        node_address, ssl_mode = self._network_config.get('node_address'), self._network_config.get('ssl_mode')
        return f'{"https://" if ssl_mode else "http://"}{node_address}'

    @staticmethod
    def _get_request_config(method, payload):

        options = {
            'method': method.value,
            'params': payload,
            'id': round(random() * 100),
        }

        if payload:
            options.update({'params': payload})

        return options

    @property
    def network_config(self):
        """
        Return network config object which contain domain name, port and ssl.
        """
        return self._network_config

    async def send_request(self, method, params=None):
        """
        Make and send request with given method and payload.
        Create url from given network config.
        Get JSON-RPC method and create request config in correspond specification.

        References::
            - https://www.jsonrpc.org/specification.

        Args:
            method (RemmeMethods): enum
            params (dict): payload

        Returns:
            Promise.
        """
        if params is None:
            params = {}

        if not isinstance(method, RemmeMethods):
            raise Exception('Invalid RPC method given.')

        url = self._get_url_for_request()
        request_data = self._get_request_config(method=method, payload=params)

        try:
            await self._rpc_client.connect_url(url=url)
        except Exception:
            raise Exception(f'Please check if your node running at {url}.')

        try:
            return await self._rpc_client.call(**request_data)
        finally:
            await self._rpc_client.disconnect()
