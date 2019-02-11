from remme.enums.key_type import KeyType
from remme.enums.remme_family_name import RemmeFamilyName
from remme.enums.remme_methods import RemmeMethods
from remme.enums.rsa_signature_padding import RsaSignaturePadding
from remme.protos.pub_key_pb2 import (
    NewPubKeyPayload,
    NewPubKeyStoreAndPayPayload,
    PubKeyMethod,
    RevokePubKeyPayload,
)
from remme.protos.transaction_pb2 import TransactionPayload
from remme.remme_keys.remme_keys import RemmeKeys
from remme.remme_public_key_storage.interface import IRemmePublicKeyStorage
from remme.remme_public_key_storage.models.public_key_info import PublicKeyInfo
from remme.remme_utils import (
    ZERO_ADDRESS,
    check_sha,
    generate_address,
    generate_settings_address,
    get_padding,
    hex_to_bytes,
    public_key_address,
    sha512_hexdigest,
    validate_address,
)


class RemmePublicKeyStorage(IRemmePublicKeyStorage):
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
    _settings_address = generate_settings_address(key='remme.economy_enabled')

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
            return PublicKeyInfo(data=info)

        raise Exception('This public key was not found.')

    @staticmethod
    async def _construct_address_from_payload(payload):

        entity_hash, entity_hash_signature = str(payload.get('entity_hash')), payload.get('entity_hash_signature')

        check_sha(data=entity_hash)

        key_type = payload.configuration

        x = {}
        x['key'] = public_key = payload[key_type]

        keys = await RemmeKeys.construct(
            key_type,
            public_key,
        )

        if not keys.verify(data=entity_hash, signature=entity_hash_signature.hex()):
            raise Exception('Signature not valid.')

        return keys.address

    @staticmethod
    async def _verify_payload_owner(owner_public_key, signature_by_owner, pub_key_payload):

        account_key = await RemmeKeys.construct(
            key_type=KeyType.ECDSA,
            public_key=owner_public_key,
        )

        payload = NewPubKeyPayload(pub_key_payload).SerializeToString()

        if not account_key.verify(data=payload, signature=signature_by_owner.hex()):
            raise Exception('Owner signature not valid.')

    def create(self, data=None):
        """
        # optional !!!

        rsaSignaturePadding?: RSASignaturePadding
        signature?: string
        doOwnerPay?: boolean

        :param data:
        :return:
           *      data: sha512(data),
     *      keysFromPublic,
     *      signature,
     *      rsaSignaturePadding: RSASignaturePadding.PSS,
     *      validFrom: Math.round(Date.now() / 1000),
     *      validTo: Math.round(Date.now() / 1000 + 1000),
     *      doOwnerPay: false
        """
        from remme.enums.rsa_signature_padding import RsaSignaturePadding
        from datetime import datetime, timedelta
        CURRENT_TIMESTAMP = int(datetime.now().timestamp())
        CURRENT_TIMESTAMP_PLUS_YEAR = int(CURRENT_TIMESTAMP + timedelta(365).total_seconds())

        keys = RemmeKeys.construct(KeyType.RSA)
        from remme.remme_keys.ecdsa import ECDSA
        d = ECDSA.generate_key_pair()
        print(d)
        print(dir(d))

        data = {
            'data': 'store_data',
            'keys': keys,
            'rsa_signature_padding': RsaSignaturePadding.PSS,
            'valid_from': CURRENT_TIMESTAMP,
            'valid_to': CURRENT_TIMESTAMP_PLUS_YEAR,
            'do_owner_pay': False,
        }

        keys = data.get('keys')

        public_key, key_type = keys.public_key, keys.key_type

        signature = data.get('signature')

        message = data.get('data') if signature else sha512_hexdigest(data=data.get('data'))

        rsa_signature_padding = data.get('rsa_signature_padding')

        if not signature:
            signature = keys.sign(data=message, rsa_signature_padding=rsa_signature_padding)

        entity_hash = hex_to_bytes(message)
        entity_hash_signature = signature

        valid_from, valid_to = data.get('valid_from'), data.get('valid_to')

        pub_key_payload = NewPubKeyPayload(
            entity_hash=entity_hash,
            entity_hash_signature=entity_hash_signature,
            valid_from=valid_from,
            valid_to=valid_to,
            hashing_algorithm=NewPubKeyPayload.HashingAlgorithm.Value('SHA256'),
        )

        if key_type == KeyType.RSA:

            pub_key_payload_rsa = NewPubKeyPayload(
                rsa=NewPubKeyPayload.RSAConfiguration(
                    padding=NewPubKeyPayload.RSAConfiguration.Padding.Value('PSS'),
                    key=public_key,
                ),
            )
            pub_key_payload.MergeFrom(pub_key_payload_rsa)

        if key_type == KeyType.EdDSA:

            pub_key_payload_eddsa = NewPubKeyPayload(
                ed25519=NewPubKeyPayload.Ed25519Configuration(key=public_key),
            )
            pub_key_payload.MergeFrom(pub_key_payload_eddsa)

        if key_type == KeyType.ECDSA:

            pub_key_payload_ecdsa = NewPubKeyPayload(
                ecdsa=NewPubKeyPayload.ECDSAConfiguration(
                    key=public_key,
                    ec=NewPubKeyPayload.ECDSAConfiguration.EC.Value('SECP256k1'),
                ),
            )
            pub_key_payload.MergeFrom(pub_key_payload_ecdsa)

        if data.get('do_owner_pay'):
            return pub_key_payload.SerializeToString()

        signature_by_owner_hex = self._remme_account.sign(transaction=pub_key_payload.SerializeToString())

        print(self._remme_account.public_key)
        print(type(self._remme_account.public_key))

        x = NewPubKeyStoreAndPayPayload(
            pub_key_payload=pub_key_payload,
            owner_public_key=self._remme_account.public_key,
            signature_by_owner=hex_to_bytes(message=signature_by_owner_hex),
        ).SerializeToString()
        # print(x)

    async def store(self, data):
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
        owner_payload = NewPubKeyStoreAndPayPayload.ParseFromString(data)

        message = owner_payload if owner_payload.pub_key_payload.entity_hash else NewPubKeyPayload.ParseFromString(data)

        if isinstance(message, NewPubKeyPayload):
            pub_key_address = await self._construct_address_from_payload(payload=message)

        elif isinstance(message, NewPubKeyStoreAndPayPayload):
            owner_public_key, signature_by_owner, pub_key_payload = message

            await self._verify_payload_owner(
                owner_public_key=owner_public_key,
                signature_by_owner=signature_by_owner,
                pub_key_payload=pub_key_payload,
            )

            pub_key_address = await self._construct_address_from_payload(payload=pub_key_payload)

            owner_address = generate_address(
                _family_name=RemmeFamilyName.ACCOUNT.value,
                _public_key_to=owner_public_key.hex(),
            )

        else:
            raise Exception('Invalid payload.')

        inputs_and_outputs = [
            pub_key_address,
            ZERO_ADDRESS,
            self._settings_address
        ]

        if owner_address:
            inputs_and_outputs.append(owner_address)

        payload_bytes = self._generate_transaction_payload(
            method= PubKeyMethod.STORE_AND_PAY if owner_address else PubKeyMethod.STORE,
            data=data,
        )

        return self._create_and_send_transaction(
            inputs=inputs_and_outputs,
            outputs=inputs_and_outputs,
            payload_bytes=payload_bytes,
        )

    async def create_and_store(self, **data):
        """
        Create public key payload bytes and store public key with its data into REMChain.
        Send transaction to chain with private key.
        :param data: dict
        :return:
        """
        payload_bytes = self.create(data=data)
        return await self.store(data=payload_bytes)

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
