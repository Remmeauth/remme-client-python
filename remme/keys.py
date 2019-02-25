from remme.models.keys.ecdsa import ECDSA
from remme.models.keys.eddsa import EdDSA
from remme.models.keys.key_type import KeyType
from remme.models.keys.rsa import RSA


class RemmeKeys:
    """
    Class that works with different types of keys.
    For now it is RSA, ECDSA (secp256k1), EdDSA (ed25519).
    """

    @staticmethod
    def generate_key_pair(key_type, options=None):
        """
        Generate key pair and get instance of RemmeKeys.

        Args:
            key_type (KeyType): enum (RSA, ECDSA, EdDSA)
            options (integer, optional): RSA key size

        Returns:
            Key pair.

        To use:
            If you don't have key pair you can generate it.

            .. code-block:: python

                from remme.models.keys.key_type import KeyType
                keys = RemmeKeys.generate_key_pair(KeyType.RSA)  # KeyType.EdDSA, KeyType.ECDSA also work.
        """
        if key_type == KeyType.RSA:
            return RSA.generate_key_pair(options=options)

        if key_type == KeyType.ECDSA:
            return ECDSA.generate_key_pair()

        if key_type == KeyType.EdDSA:
            return EdDSA.generate_key_pair(seed=options)

    @staticmethod
    def get_address_from_public_key(key_type, public_key):
        """
        Get address from public key.

        Args:
            key_type (KeyType): enum (RSA, ECDSA, EdDSA)
            public_key (bytes): public key in bytes

        Returns:
            Address (string) in blockchain generated from public key.

        To use:
            If you have public key. You can get an address for it.

            .. code-block:: python

                from remme.models.keys.key_type import KeyType
                public_key = '30820122300d06092a864886f70d01010105000382010f003082010a0282010100ad37c7475fe9d987555f8d92f0a440ebbf7bb2a87feffa3e2f229b9b782c4f7a78a1c255a687b1355fb788bef89188832d594a8f4e72d6d009d1ee56e9ff2a7c4de17cab3786bf74c9045bc30dc9475514a296faac9264c265aa4496005d17925c78f324f73a55bdfb6de2109c8ea64d75f10aea31c12f8a226deba507a57d22ad22391c066c5ce2d0072b4f18ddf97214ae3334f7ddff08d92bb6325f8f7c4d9419e7acd23abd9b9b0a3153fef0a626033719f7a9052de822c97fc54007357c8aa3dd416153a670a060edf453e61227f4e2acbb6461bbf40a948c74c4436cf5c10c3c29a42eaf6a74c4124a0f9dade599243cd9420266701254a7f4a4461fbf0203010001'
                address = RemmeKeys.get_address_from_public_key(
                    KeyType.RSA,
                    bytes.fromhex(public_key),
                )  # KeyType.EdDSA, KeyType.ECDSA also work.
        """
        if key_type == KeyType.RSA:
            return RSA.get_address_from_public_key(public_key=public_key)

        if key_type == KeyType.ECDSA:
            return ECDSA.get_address_from_public_key(public_key=public_key)

        if key_type == KeyType.EdDSA:
            return EdDSA.get_address_from_public_key(public_key=public_key)

    @staticmethod
    def construct(key_type=KeyType.RSA, private_key=None, public_key=None):
        """
        Args:
            key_type (KeyType): enum (RSA, ECDSA, EdDSA)
            private_key (bytes): private key in bytes
            public_key (bytes): public key in bytes

        Returns:
            Constructed RemmeKeys object.

        To use:
            If you have private key, you can construct RemmeKeys based on private key.

            .. code-block:: python

                from remme.models.keys.key_type import KeyType
                private_key = '30820122300d06092a864886f70d01010105000382010f003082010a0282010100ad37c7475fe9d987555f8d92f0a440ebbf7bb2a87feffa3e2f229b9b782c4f7a78a1c255a687b1355fb788bef89188832d594a8f4e72d6d009d1ee56e9ff2a7c4de17cab3786bf74c9045bc30dc9475514a296faac9264c265aa4496005d17925c78f324f73a55bdfb6de2109c8ea64d75f10aea31c12f8a226deba507a57d22ad22391c066c5ce2d0072b4f18ddf97214ae3334f7ddff08d92bb6325f8f7c4d9419e7acd23abd9b9b0a3153fef0a626033719f7a9052de822c97fc54007357c8aa3dd416153a670a060edf453e61227f4e2acbb6461bbf40a948c74c4436cf5c10c3c29a42eaf6a74c4124a0f9dade599243cd9420266701254a7f4a4461fbf0203010001'
                keys = RemmeKeys.construct(KeyType.RSA, bytes.fromhex(private_key))

            If you have public key, you can construct RemmeKeys based on public key.

            .. code-block:: python

                from remme.models.keys.key_type import KeyType
                public_key = '30820122300d06092a864886f70d01010105000382010f003082010a0282010100ad37c7475fe9d987555f8d92f0a440ebbf7bb2a87feffa3e2f229b9b782c4f7a78a1c255a687b1355fb788bef89188832d594a8f4e72d6d009d1ee56e9ff2a7c4de17cab3786bf74c9045bc30dc9475514a296faac9264c265aa4496005d17925c78f324f73a55bdfb6de2109c8ea64d75f10aea31c12f8a226deba507a57d22ad22391c066c5ce2d0072b4f18ddf97214ae3334f7ddff08d92bb6325f8f7c4d9419e7acd23abd9b9b0a3153fef0a626033719f7a9052de822c97fc54007357c8aa3dd416153a670a060edf453e61227f4e2acbb6461bbf40a948c74c4436cf5c10c3c29a42eaf6a74c4124a0f9dade599243cd9420266701254a7f4a4461fbf0203010001'
                keys = RemmeKeys.construct(KeyType.RSA, bytes.fromhex(public_key))

            If you don't have any key, you can construct RemmeKeys without keys and it
            generate keys for you with default generation options.

            .. code-block:: python

                from remme.models.keys.key_type import KeyType
                keys = RemmeKeys.construct(KeyType.RSA)

            Also you can construct RemmeKeys without any params so keyType will be RSA by default.

            .. code-block:: python

                keys = RemmeKeys.construct()
        """
        if private_key is None and public_key is None:
            private_key, public_key = RemmeKeys.generate_key_pair(key_type=key_type)

        if key_type == KeyType.RSA:
            return RSA(private_key=private_key, public_key=public_key)

        if key_type == KeyType.ECDSA:
            return ECDSA(private_key=private_key, public_key=public_key)

        if key_type == KeyType.EdDSA:
            return EdDSA(private_key=private_key, public_key=public_key)
