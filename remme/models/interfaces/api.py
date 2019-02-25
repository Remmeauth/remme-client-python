import abc


class IRemmeAPI(metaclass=abc.ABCMeta):

    @staticmethod
    @abc.abstractmethod
    def send_request(method, params):
        """
        Make and send request with given method and payload.
        Create url from given network config
        Get JSON-RPC method and create request config in correspond specification.

        Args:
            method (RemmeMethods): enum
            params (dict): payload

        References::
            - https://www.jsonrpc.org/specification.
        """
        pass
