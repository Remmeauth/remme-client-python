from remme.enums.key_type import KeyType
from remme.keys.ecdsa import ECDSA
from remme.keys.eddsa import EdDSA
from remme.keys.interface import IRemmeKeys
from remme.keys.rsa import RSA


class RemmeKeys(IRemmeKeys):
    """
    Class that works with different types of keys.
    For now it is RSA, ECDSA (secp256k1), EdDSA (ed25519).
    """

    def __init__(self, key_type=KeyType.RSA, private_key=None, public_key=None):
        """
        @example
        If you have private key. You can construct RemmeKeys based on private key.
        ```python
        from remme.enums.key_type import KeyType
        from remme.remme_utils import

        private_key = "-----BEGIN RSA PRIVATE KEY-----\r\nMIIEowIBAAKCAQEAkhdw64WKrvXCWtGsNeVTPKDPpcHN0kcF4acvfPauDE8TpIFu\r\n8rFQdnGdBldJMo+iHC4VkEc7SqP0Z7bynBXZze6YAsi7VUggO+5kDuJnKrg0VJ5s\r\nwfV/Jdvj9ev1iG1TeVTAyp1Uvjmek9uAh6DgobdtWM/VpVYsbBcMT4XXpzmuv0qk\r\nEf9YmR3kJ5SBGdkb6jaOnjJWO0O6kOUO54y06wr0BXqYWWQTnGC3DJf2iqu68Ceo\r\nZsg/dRNs1zXP4x00GyOW7OdnmMUsySquf//KHUlnD3Oa1TyWzjF6NcMWv0PgDg6u\r\n8q4739X0ueBNDpXJyiMMpQUZ/8YbW/Ijdfv7DQIDAQABAoIBADRnHCYfXMOte+2/\r\n0Bn1DIpu1I0Mm5uVxlJO+gXFJmFb7BvSIc4ENGyIDF896A+u3eNl1G5QXsBDV2Ps\r\nh9HdNKddskEtZ6ULniRhOprsMz1rnbnMqg5Y1SbrXTXVUdmB/bND53PGQ6OIX42B\r\n6vS7jFf1x89XnbcU1hJfohbUV6qvwr+hyrvrV859LM80rErCKGXXi6gtiRBiTYA3\r\n2qgO+F/ntmoU638XDzeIhKNjCP+KcWcQX1TRlrcuKfPKfCttHTb1MCGWnrOqy56w\r\nU628Iz4lKfjCOOdAXvyDRBEFSPKfriuB5JQQ67cZ9w783/2ZChhAY4wzBqvgnnlo\r\np6cPXDECgYEA+shoBswhqkA81RHxdkMoM9/iGwfkdFwxr9TqHGN7+L0hRXJlysKP\r\npBFX7Wg6GWF3BDHQzLoWQCEox0NgHbAVTC5DBxjIEjRemmlYEeAPqVRTub1lfp37\r\nYcK8BqsllDgXsqlQQNKqqVj4V2y/PO6NzlHWN9inJrp8ZZKSKPSamq8CgYEAlSF7\r\nDB0STde20E+ZPzQZi7zLWl59yM29mlKujlRktp2vl3foRJgQsndOAIc6k4+ImXR8\r\ngtfwpCYrXTQhJE4GHO/E/52vuwkVVz9qN5ZmgzR13yzlicCVmfZ7aaZ6jblNiQ1G\r\ngnIx1chcb8Vl5fncmaoa9SgefwWciPERNg31RQMCgYEApH1SjjLSWgMsY20Tfchq\r\n1Cui+Kviktft1zDGJbyzEeGrswtn7OhUov6lN5jHkuI02FF8bOwZsBKP1rNAlfhq\r\n377wQ/VjNV2YN5ulIoRegWhISmoJ6lThD6xU++LCEUgBczRO6VXEjrNGoME5ZlPq\r\nO0u+QH8gk+x5r33F1Isr5Q0CgYBHrmEjsHGU4wPnWutROuywgx3HoTWaqHHjVKy8\r\nkwoZ0O+Owb7uAZ28+qWOkXFxbgN9p0UV60+qxwH++ciYV7yOeh1ZtGS8ZSBR4JRg\r\nhbVeiX/CtyTZsqz15Ujqvm+X4aLIJo5msxcLKBRuURaqlRAY+G+euRr3eS4FkMHy\r\nFoF3GwKBgFDNeJc7VfbQq2toRSxCNuUTLXoZPrPfQrV+mA9umGCep44Ea02xIKQu\r\nbYpYghpdbASOp6fJvBlwjI8LNX3dC/PfUpbIG84bVCokgBCMNJQ+/DBuPBt7L29A\r\n7Ra1poXMbXt0nF3LgAtZHveRmVDtcr52dZ/6Yd2km5mAHj+4yPZo\r\n-----END RSA PRIVATE KEY-----\r\n"

        keys = Remme.Keys(KeyType.RSA, private_key)  # Our chain works only with RSA now
        ```

        If you have public key. You can construct RemmeKeys based on public key.
        ```python
        from remme.enums.key_type import KeyType
        from remme.remme_utils import

        public_key = "-----BEGIN PUBLIC KEY-----\r\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAkhdw64WKrvXCWtGsNeVT\r\nPKDPpcHN0kcF4acvfPauDE8TpIFu8rFQdnGdBldJMo+iHC4VkEc7SqP0Z7bynBXZ\r\nze6YAsi7VUggO+5kDuJnKrg0VJ5swfV/Jdvj9ev1iG1TeVTAyp1Uvjmek9uAh6Dg\r\nobdtWM/VpVYsbBcMT4XXpzmuv0qkEf9YmR3kJ5SBGdkb6jaOnjJWO0O6kOUO54y0\r\n6wr0BXqYWWQTnGC3DJf2iqu68CeoZsg/dRNs1zXP4x00GyOW7OdnmMUsySquf//K\r\nHUlnD3Oa1TyWzjF6NcMWv0PgDg6u8q4739X0ueBNDpXJyiMMpQUZ/8YbW/Ijdfv7\r\nDQIDAQAB\r\n-----END PUBLIC KEY-----\r\n";

        keys = Remme.Keys(KeyType.RSA, public_key)  # Our chain works only with RSA now
        ```
        :param key_type: KeyType
        :param private_key: string or bytes
        :param public_key: string or bytes
        """
        if private_key is None and public_key is None:
            raise Exception('Can\'t construct without private or public keys')

        if key_type == KeyType.RSA:
            self._keys = RSA(private_key=private_key, public_key=public_key)

        if key_type == KeyType.ECDSA:
            self._keys = ECDSA(private_key=private_key, public_key=public_key)

        if key_type == KeyType.EdDSA:
            self._keys = EdDSA(private_key=private_key, public_key=public_key)

    @staticmethod
    def generate_key_pair(key_type, options=None):
        """
        Generate key pair and get instance of RemmeKeys.

        @example
        If you don't have key pair you can generate it.
        ```python
        from remme.enums.key_type import KeyType

        keys = Remme.Keys.genarate_key_pair(KeyType.RSA)  # Our chain works only with RSA now
        ```
        :param key_type: KeyType
        :param options: integer
        :return: key pair
        """
        if key_type == KeyType.RSA:
            return RSA.generate_key_pair(options=options)

        if key_type == KeyType.ECDSA:
            return ECDSA.generate_key_pair()

        if key_type == KeyType.EdDSA:
            return EdDSA.generate_key_pair()

    @staticmethod
    def get_address_from_public_key(key_type, public_key):
        """
        Get address from public key.

        @example
        If you have public key. You can get an address for it.
        ```python
        from remme.enums.key_type import KeyType

        public_key = "-----BEGIN PUBLIC KEY-----\r\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAkhdw64WKrvXCWtGsNeVT\r\nPKDPpcHN0kcF4acvfPauDE8TpIFu8rFQdnGdBldJMo+iHC4VkEc7SqP0Z7bynBXZ\r\nze6YAsi7VUggO+5kDuJnKrg0VJ5swfV/Jdvj9ev1iG1TeVTAyp1Uvjmek9uAh6Dg\r\nobdtWM/VpVYsbBcMT4XXpzmuv0qkEf9YmR3kJ5SBGdkb6jaOnjJWO0O6kOUO54y0\r\n6wr0BXqYWWQTnGC3DJf2iqu68CeoZsg/dRNs1zXP4x00GyOW7OdnmMUsySquf//K\r\nHUlnD3Oa1TyWzjF6NcMWv0PgDg6u8q4739X0ueBNDpXJyiMMpQUZ/8YbW/Ijdfv7\r\nDQIDAQAB\r\n-----END PUBLIC KEY-----\r\n";

        address = Remme.Keys.get_address_from_public_key(KeyType.RSA, public_key)  # Our chain works only with RSA now
        ```
        :param key_type: KeyType
        :param public_key: in pem format
        :return: string: address in blockchain generated from public key
        """
        if key_type == KeyType.RSA:
            return RSA.get_address_from_public_key(public_key=public_key)

        if key_type == KeyType.ECDSA:
            return ECDSA.get_address_from_public_key(public_key=public_key)

        if key_type == KeyType.EdDSA:
            return EdDSA.get_address_from_public_key(public_key=public_key)

    def sign(self, data, rsa_signature_padding=None):
        """
        Sign data based on private key.
        @example
        ```python
        from remme.enums.key_type import KeyType

        # If you don't have private key you can generate it
        keys = Remme.Keys.genarate_key_pair(KeyType.RSA)  # Our chain works only with RSA now

        # If you have private key you can construct RemmeKeys based on it
        from remme.remme_utils import

        private_key = "-----BEGIN RSA PRIVATE KEY-----\r\nMIIEowIBAAKCAQEAkhdw64WKrvXCWtGsNeVTPKDPpcHN0kcF4acvfPauDE8TpIFu\r\n8rFQdnGdBldJMo+iHC4VkEc7SqP0Z7bynBXZze6YAsi7VUggO+5kDuJnKrg0VJ5s\r\nwfV/Jdvj9ev1iG1TeVTAyp1Uvjmek9uAh6DgobdtWM/VpVYsbBcMT4XXpzmuv0qk\r\nEf9YmR3kJ5SBGdkb6jaOnjJWO0O6kOUO54y06wr0BXqYWWQTnGC3DJf2iqu68Ceo\r\nZsg/dRNs1zXP4x00GyOW7OdnmMUsySquf//KHUlnD3Oa1TyWzjF6NcMWv0PgDg6u\r\n8q4739X0ueBNDpXJyiMMpQUZ/8YbW/Ijdfv7DQIDAQABAoIBADRnHCYfXMOte+2/\r\n0Bn1DIpu1I0Mm5uVxlJO+gXFJmFb7BvSIc4ENGyIDF896A+u3eNl1G5QXsBDV2Ps\r\nh9HdNKddskEtZ6ULniRhOprsMz1rnbnMqg5Y1SbrXTXVUdmB/bND53PGQ6OIX42B\r\n6vS7jFf1x89XnbcU1hJfohbUV6qvwr+hyrvrV859LM80rErCKGXXi6gtiRBiTYA3\r\n2qgO+F/ntmoU638XDzeIhKNjCP+KcWcQX1TRlrcuKfPKfCttHTb1MCGWnrOqy56w\r\nU628Iz4lKfjCOOdAXvyDRBEFSPKfriuB5JQQ67cZ9w783/2ZChhAY4wzBqvgnnlo\r\np6cPXDECgYEA+shoBswhqkA81RHxdkMoM9/iGwfkdFwxr9TqHGN7+L0hRXJlysKP\r\npBFX7Wg6GWF3BDHQzLoWQCEox0NgHbAVTC5DBxjIEjRemmlYEeAPqVRTub1lfp37\r\nYcK8BqsllDgXsqlQQNKqqVj4V2y/PO6NzlHWN9inJrp8ZZKSKPSamq8CgYEAlSF7\r\nDB0STde20E+ZPzQZi7zLWl59yM29mlKujlRktp2vl3foRJgQsndOAIc6k4+ImXR8\r\ngtfwpCYrXTQhJE4GHO/E/52vuwkVVz9qN5ZmgzR13yzlicCVmfZ7aaZ6jblNiQ1G\r\ngnIx1chcb8Vl5fncmaoa9SgefwWciPERNg31RQMCgYEApH1SjjLSWgMsY20Tfchq\r\n1Cui+Kviktft1zDGJbyzEeGrswtn7OhUov6lN5jHkuI02FF8bOwZsBKP1rNAlfhq\r\n377wQ/VjNV2YN5ulIoRegWhISmoJ6lThD6xU++LCEUgBczRO6VXEjrNGoME5ZlPq\r\nO0u+QH8gk+x5r33F1Isr5Q0CgYBHrmEjsHGU4wPnWutROuywgx3HoTWaqHHjVKy8\r\nkwoZ0O+Owb7uAZ28+qWOkXFxbgN9p0UV60+qxwH++ciYV7yOeh1ZtGS8ZSBR4JRg\r\nhbVeiX/CtyTZsqz15Ujqvm+X4aLIJo5msxcLKBRuURaqlRAY+G+euRr3eS4FkMHy\r\nFoF3GwKBgFDNeJc7VfbQq2toRSxCNuUTLXoZPrPfQrV+mA9umGCep44Ea02xIKQu\r\nbYpYghpdbASOp6fJvBlwjI8LNX3dC/PfUpbIG84bVCokgBCMNJQ+/DBuPBt7L29A\r\n7Ra1poXMbXt0nF3LgAtZHveRmVDtcr52dZ/6Yd2km5mAHj+4yPZo\r\n-----END RSA PRIVATE KEY-----\r\n"
        keys = Remme.Keys(KeyType.RSA, private_key)  # Our chain works only with RSA now

        # Then you can sign some data. For RSA key type you should provide RSASignaturePadding (by default PSS)
        signature = keys.sign('some data')
        ```
        :param data: string
        :param rsa_signature_padding: RSASignaturePadding
        :return: signature: hex format
        """
        if self._keys.private_key is None:
            raise Exception('You can\'t sign this data because you didn\'t provide private key for this.')

        if isinstance(self._keys, RSA):
            return self._keys.sign(data=data, rsa_signature_padding=rsa_signature_padding)

        return self._keys.sign(data=data)

    def verify(self, data, signature, rsa_signature_padding=None):
        """
        Verify signature for data based on public key.

        @example
        ```python
        from remme.enums.key_type import KeyType

        # If you have public key from private key that is signed this data you can construct RemmeKeys based on it
        from remme.remme_utils import

        public_key = "-----BEGIN PUBLIC KEY-----\r\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAkhdw64WKrvXCWtGsNeVT\r\nPKDPpcHN0kcF4acvfPauDE8TpIFu8rFQdnGdBldJMo+iHC4VkEc7SqP0Z7bynBXZ\r\nze6YAsi7VUggO+5kDuJnKrg0VJ5swfV/Jdvj9ev1iG1TeVTAyp1Uvjmek9uAh6Dg\r\nobdtWM/VpVYsbBcMT4XXpzmuv0qkEf9YmR3kJ5SBGdkb6jaOnjJWO0O6kOUO54y0\r\n6wr0BXqYWWQTnGC3DJf2iqu68CeoZsg/dRNs1zXP4x00GyOW7OdnmMUsySquf//K\r\nHUlnD3Oa1TyWzjF6NcMWv0PgDg6u8q4739X0ueBNDpXJyiMMpQUZ/8YbW/Ijdfv7\r\nDQIDAQAB\r\n-----END PUBLIC KEY-----\r\n";
        keys = Remme.Keys(KeyType.RSA, public_key)  # Our chain works only with RSA now

        print(keys.verify('some data', signature))  # true if private key for this public key is signed data else false

        :param data: string
        :param signature: hex format
        :param rsa_signature_padding: RSASignaturePadding
        :return: boolean
        """
        if isinstance(self._keys, RSA):
            return self._keys.verify(
                data=data,
                signature=signature,
                rsa_signature_padding=rsa_signature_padding,
            )

        return self._keys.verify(data=data, signature=signature)

    def get_address(self):
        """
        Address of this key in blockchain.

        References:
            - https://docs.remme.io/remme-core/docs/family-account.html#addressing
        """
        return self._keys.address

    def get_private_key(self):
        """
        Return private key.
        """
        return self._keys.private_key

    def get_public_key(self):
        """
        Return public key.
        """
        return self._keys.public_key

    def get_key_type(self):
        """
        Return key type.
        """
        return KeyType[self._keys.key_type]

    def get_private_key_pem(self):
        """
        Return private key in pem format.
        """
        return self._keys.private_key_pem

    def get_public_key_pem(self):
        """
        Return public key in pem format.
        """
        return self._keys.public_key_pem

    def get_private_key_hex(self):
        """
        Return private key in hex format.
        """
        return self._keys.private_key_hex

    def get_public_key_hex(self):
        """
        Return public key in hex format.
        """
        return self._keys.public_key_hex

    def get_family_name(self):
        """
        Return family name.
        """
        return self._keys.family_name
