"""
Key DTO for different kind of keys.
"""
from remme.models.utils.family_name import RemmeFamilyName


class KeyDto:

    _family_name = RemmeFamilyName.PUBLIC_KEY.value

    def __init__(self, address=None, private_key=None, public_key=None, private_key_hex=None, public_key_hex=None,
                 private_key_pem=None, public_key_pem=None, public_key_base64=None, key_type=None):
        self._address = address
        self._private_key = private_key
        self._public_key = public_key
        self._private_key_hex = private_key_hex
        self._public_key_hex = public_key_hex
        self._private_key_pem = private_key_pem
        self._public_key_pem = public_key_pem
        self._public_key_base64 = public_key_base64
        self._key_type = key_type

    @property
    def address(self):
        """
        Address of this key in blockchain.

        References:
            - https://docs.remme.io/remme-core/docs/family-account.html#addressing

        :return: {string}
        """
        return self._address

    @property
    def private_key(self):
        """
        Return private key.

        :return: {string}
        """
        if not self._private_key:
            raise Exception("You didn't provide a private key.")

        return self._private_key

    @property
    def public_key(self):
        """
        Return public key.

        :return: {string}
        """
        return self._public_key

    @property
    def private_key_hex(self):
        """
        Return private key in hex format.

        :return: {string}
        """
        if not self._private_key_hex:
            raise Exception(f"Don't supported for this key type: {self._key_type.name} or didn't provide private key.")

        return self._private_key_hex

    @property
    def public_key_hex(self):
        """
        Return public key in hex format.

        :return: {string}
        """
        if not self._public_key_hex:
            raise Exception(f"Don't supported for this key type: {self._key_type.name}.")

        return self._public_key_hex

    @property
    def private_key_pem(self):
        """
        Return private key in pem format.

        :return: {string}
        """
        if not self._private_key_pem:
            raise Exception(f"Don't supported for this key type: {self._key_type.name} or didn't provide private key.")

        return self._private_key_pem

    @property
    def public_key_pem(self):
        """
        Return public key in pem format.

        :return: {string}
        """
        if not self._public_key_pem:
            raise Exception(f"Don't supported for this key type: {self._key_type.name}.")

        return self._public_key_pem

    @property
    def key_type(self):
        """
        Return key type.

        :return: {string}
        """
        return self._key_type

    @property
    def family_name(self):
        """
        Return family name.

        :return: {RemmeFamilyName}
        """
        return self._family_name
