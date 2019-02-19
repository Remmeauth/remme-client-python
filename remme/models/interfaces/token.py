import abc


class IRemmeToken(metaclass=abc.ABCMeta):

    @staticmethod
    @abc.abstractmethod
    def transfer(address_to, amount):
        """
        Transfer tokens from signed address (remme.account.address) to given address.
        Send transaction to REMChain.
        :param address_to: string
        :param amount: integer
        """
        pass

    @staticmethod
    @abc.abstractmethod
    def get_balance(address):
        """
        Get balance on given account address.
        :param address: string
        """
        pass
