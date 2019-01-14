from remme.enums.key_type import KeyType
from remme.enums.remme_family_name import RemmeFamilyName
from remme.enums.remme_methods import RemmeMethods
from remme.enums.rsa_signature_padding import RsaSignaturePadding
from remme.protos.pub_key_pb2 import (
    NewPubKeyPayload,
    PubKeyMethod,
    RevokePubKeyPayload,
)
from remme.protos.transaction_pb2 import TransactionPayload
from remme.remme_utils import (
    ZERO_ADDRESS,
    generate_address,
    generate_settings_address,
    get_padding,
    public_key_address,
    validate_address,
)


class RemmePublicKeyStorage:
    """
    Class for working with public key storage.

    @example
    ```python
    from remme.enums.key_type import KeyType

    keys = await RemmeKeys.construct(KeyType.RSA)

    store_response = await remme.public_key_storage.store(
        data='store data',
        keys=keys,
        valid_from=valid_from,
        valid_to=valid_to,
    )

    async for msg in store_response.connect_to_web_socket():
        print(msg)

        key_is_valid = await remme.public_key_storage.check(keys.address)
        print(key_is_valid)  # True

        public_key_info = await remme.public_key_storage.get_info(keys.address)
        print(public_key_info)  # PublicKeyInfo

        revoke = await remme.public_key_storage.revoke(remme_keys.address)
        # You can connect_to_web_socket like in store method.
        print(revoke.batch_id)  # r"\^[a-f0-9]{128}$\"

        public_key_addresses = await remme.publicKeyStorage.get_account_public_keys(remme.account.address)
        print(public_key_addresses)  # []

        store_response.close_web_socket()
    ```
    """

    _family_name = RemmeFamilyName.PUBLIC_KEY.value
    _family_version = '0.1'

    def __init__(self, remme_api, remme_account, remme_transaction_service):
        """
        @example
        Usage without remme main package.
        ```python
        api = RemmeAPI()
        account = RemmeAccount()
        transaction = RemmeTransactionService()
        public_key_storage = RemmePublicKeyStorage(api, account, transaction)
        ```
        :param remme_api: RemmeAPI
        :param remme_account: RemmeAccount
        :param remme_transaction_service: RemmeTransactionService
        """
        self._remme_api = remme_api
        self._remme_account = remme_account
        self._remme_transaction = remme_transaction_service

    @staticmethod
    def _generate_transaction_payload(method, data):
        return TransactionPayload(method=method, data=data).SerializeToString()

    async def _create_and_send_transaction(self, inputs, outputs, payload_bytes):

        transaction = await self._remme_transaction.create(
            family_name=self._family_name,
            family_version=self._family_version,
            inputs=inputs,
            outputs=outputs,
            payload_bytes=payload_bytes,
        )
        return await self._remme_transaction.send(payload=transaction)

    async def _get_info_by_public_key(self, address):

        validate_address(address=address)

        info = await self._remme_api.send_request(
            method=RemmeMethods.PUBLIC_KEY,
            params=public_key_address(address),
        )

        if info.get('error') is None:
            info['address'] = generate_address(self._family_name, address)
            return info

        raise Exception('This public key was not found.')

    async def store(self, data, keys, valid_from, valid_to, rsa_signature_padding=RsaSignaturePadding.PSS):
        """
        Store public key with its data into REMChain.
        Send transaction to chain.
        @example
        ```python
        from remme.remme import Remme
        from remme.enums.key_type import KeyType
        from remme.enums.rsa_signature_padding import RsaSignaturePadding

        keys = Remme.keys.construct(KeyType.RSA)

        store_response = await remme.public_key_storage.store(
            data='store data',
            keys=keys,
            valid_from=valid_from,
            valid_to=valid_to,
            rsa_signature_padding=RsaSignaturePadding.PSS,
        )

        async for msg in store_response.connect_to_web_socket():
            print(msg)
            store_response.close_web_socket()
        ```
        :param data: string
        :param keys: instance of key class
        :param valid_from: timestamp
        :param valid_to: timestamp
        :param rsa_signature_padding: RsaSignaturePadding.PSS by default
        :return: information about storing public key to REMChain
        """
        entity_hash = data.encode('utf-8')
        entity_hash_signature = keys.sign(data=entity_hash, rsa_signature_padding=rsa_signature_padding)

        new_pub_key_payload = NewPubKeyPayload(
            entity_hash=entity_hash,
            entity_hash_signature=entity_hash_signature,
            valid_from=valid_from,
            valid_to=valid_to,
            hashing_algorithm=NewPubKeyPayload.HashingAlgorithm.Value('SHA256'),
        )

        if keys.key_type == KeyType.RSA:

            new_pub_key_payload_rsa = NewPubKeyPayload(
                rsa=NewPubKeyPayload.RSAConfiguration(
                    padding=get_padding(padding=rsa_signature_padding),
                    key=keys.public_key,
                ),
            )
            new_pub_key_payload.MergeFrom(new_pub_key_payload_rsa)

        if keys.key_type == KeyType.EdDSA:

            new_pub_key_payload_eddsa = NewPubKeyPayload(
                ed25519=NewPubKeyPayload.Ed25519Configuration(
                    key=keys.public_key,
                ),
            )
            new_pub_key_payload.MergeFrom(new_pub_key_payload_eddsa)

        if keys.key_type == KeyType.ECDSA:

            new_pub_key_payload_ecdsa = NewPubKeyPayload(
                ecdsa=NewPubKeyPayload.ECDSAConfiguration(
                    key=keys.public_key,
                    ec=NewPubKeyPayload.ECDSAConfiguration.EC.Value('SECP256k1'),
                ),
            )
            new_pub_key_payload.MergeFrom(new_pub_key_payload_ecdsa)

        payload_bytes = self._generate_transaction_payload(
            method=PubKeyMethod.STORE,
            data=new_pub_key_payload.SerializeToString(),
        )

        public_key_address = keys.address
        economy_enabled_address = generate_settings_address("remme.economy_enabled")

        inputs = [
            public_key_address,
            economy_enabled_address,
            ZERO_ADDRESS,
        ]

        outputs = [
            public_key_address,
            ZERO_ADDRESS,
        ]

        return await self._create_and_send_transaction(
            inputs=inputs,
            outputs=outputs,
            payload_bytes=payload_bytes,
        )

    async def check(self, address):
        """
        Check public key on validity and revocation.
        Take address of public key.
        @example
        ```python
        is_valid = await remme.public_key_storage.check(public_key_address)
        ```
        :param address: string
        :return: boolean
        """
        is_valid = self._get_info_by_public_key(address=address)

        return is_valid

    async def get_info(self, public_key_address):
        """
        Get info about this public key.
        Take address of public key.
        @example
        ```python
        info = await remme.public_key_storage.get_info(public_key_address)
        ```
        :param public_key_address: string
        :return: information about public key
        """
        return await self._get_info_by_public_key(address=public_key_address)

    async def revoke(self, public_key_address):
        """
        Revoke public key by address.

        Take address of public key. Send transaction to chain.
        @example
        ```python
        revoke_response = await remme.public_key_storage.revoke(public_key_address)
        ```
        :param public_key_address: string
        :return: information about revoked public key
        """
        validate_address(address=public_key_address)

        revoke_payload = RevokePubKeyPayload(address=public_key_address).SerializeToString()
        payload_bytes = self._generate_transaction_payload(
            method=PubKeyMethod.REVOKE,
            data=revoke_payload,
        )

        return await self._create_and_send_transaction(
            inputs=[public_key_address],
            outputs=[public_key_address],
            payload_bytes=payload_bytes,
        )

    async def get_account_public_keys(self, address):
        """
        Take account address (which describe in PATTERNS.ADDRESS).
        @example
        ```python
        remme = Remme()
        public_key_addresses = await remme.public_key_storage.get_account_public_keys(remme.account.address)
        ```
        :param address: string
        :return: list with public key addresses
        """
        validate_address(address=address)

        return await self._remme_api.send_request(
            method=RemmeMethods.USER_PUBLIC_KEY,
            params=public_key_address(address),
        )
