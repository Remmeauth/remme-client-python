import abc


class IRemmeToken(metaclass=abc.ABCMeta):

    @staticmethod
    @abc.abstractmethod
    def transfer(address_to, amount):
        """
        Transfer tokens from signed address (remme.account.address) to given address.
        Send transaction to REMChain.

        Args:
            address_to (string): given address
            amount (integer): amount of tokens
        """
        pass

    @staticmethod
    @abc.abstractmethod
    def get_balance(address):
        """
        Get balance on given account address.

        Args:
            address (string): account address
        """
        pass
