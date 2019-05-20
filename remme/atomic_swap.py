import re

from remme.models.atomic_swap.swap_init_dto import SwapInitDto
from remme.models.general.methods import RemmeMethods
from remme.models.general.patterns import RemmePatterns
from remme.models.interfaces.atomic_swap import IRemmeSwap
from remme.models.utils.constants import (
    BLOCK_INFO_CONFIG_ADDRESS,
    BLOCK_INFO_NAMESPACE_ADDRESS,
    CONSENSUS_ADDRESS,
    ZERO_ADDRESS,
)
from remme.models.utils.family_name import RemmeFamilyName
from remme.models.websocket.swap_info import SwapInfo
from remme.protobuf.atomic_swap_pb2 import (
    AtomicSwapApprovePayload,
    AtomicSwapClosePayload,
    AtomicSwapExpirePayload,
    AtomicSwapInitPayload,
    AtomicSwapMethod,
    AtomicSwapSetSecretLockPayload,
)
from remme.protobuf.transaction_pb2 import TransactionPayload
from remme.utils import (
    generate_address,
    generate_settings_address,
)

ATOMIC_SWAP_METHODS = [
    AtomicSwapMethod.INIT,
    AtomicSwapMethod.EXPIRE,
    AtomicSwapMethod.CLOSE,
    AtomicSwapMethod.SET_SECRET_LOCK,
    AtomicSwapMethod.APPROVE,
]


class RemmeSwap(IRemmeSwap):
    """
    Main class for working with Atomic Swap.

    To use:
        .. code-block:: python

            swap_id = '133102e41346242476b15a3a7966eb5249271025fc7fb0b37ed3fdb4bcce3806'
            secret_key = '039eaa877ff63694f8f09c8034403f8b5165a7418812a642396d5d539f90b170'
            secret_lock = 'b605112c2d7489034bbd7beab083fb65ba02af787786bb5e3d99bb26709f4f68'
            receiver_address = '112007484def48e1c6b77cf784aeabcac51222e48ae14f3821697f4040247ba01558b1'
            sender_address_non_local = '0xe6ca0e7c974f06471759e9a05d18b538c5ced11e'

            init = await remme.swap.init(
                receiver_address=receiver_address,
                sender_address_non_local=sender_address_non_local,
                amount=100,
                swap_id=swap_id,
                secret_lock_by_solicitor=secret_lock_by_solicitor,
            )
    """

    _family_name = RemmeFamilyName.SWAP.value
    _family_version = '0.1'
    _settings_swap_comission = generate_settings_address('remme.settings.swap_comission')

    def __init__(self, remme_api, remme_transaction_service):
        """
        Args:
            remme_api: RemmeAPI
            remme_transaction_service: RemmeTransactionService

        To use:
            Usage without main remme package.

            .. code-block:: python

                remme_api = RemmeAPI()
                remme_account = RemmeAccount()
                remme_transaction = RemmeTransactionService(remme_api, remme_account)
                remme_swap = RemmeSwap(remme_api, remme_transaction)

        """
        self._remme_api = remme_api
        self._remme_transaction_service = remme_transaction_service

    def _get_addresses(self, method, swap_id, receiver_address=None):
        """
        Get addresses for inputs and outputs.

        Args:
            method (protobuf): AtomicSwapMethod
            swap_id (string): swap id
            optional receiver_address (string): receiver address

        Returns:
            Lists of addresses inputs and outputs.
        """
        addresses = [generate_address(_family_name=self._family_name, _public_key_to=swap_id)]

        inputs, outputs = None, None

        if method not in ATOMIC_SWAP_METHODS:
            inputs = outputs = addresses
            return inputs, outputs

        if method == AtomicSwapMethod.INIT:
            inputs = [
                self._settings_swap_comission,
                CONSENSUS_ADDRESS,
                ZERO_ADDRESS,
                BLOCK_INFO_CONFIG_ADDRESS,
                BLOCK_INFO_NAMESPACE_ADDRESS,
            ]
            outputs = [
                self._settings_swap_comission,
                CONSENSUS_ADDRESS,
                ZERO_ADDRESS,
            ]

        elif method == AtomicSwapMethod.EXPIRE:
            inputs = [
                CONSENSUS_ADDRESS,
                ZERO_ADDRESS,
                BLOCK_INFO_CONFIG_ADDRESS,
                BLOCK_INFO_NAMESPACE_ADDRESS,
            ]
            outputs = [
                CONSENSUS_ADDRESS,
                ZERO_ADDRESS,
            ]

        elif method == AtomicSwapMethod.CLOSE:
            inputs = [
                CONSENSUS_ADDRESS,
                ZERO_ADDRESS,
                receiver_address,
            ]
            outputs = [
                CONSENSUS_ADDRESS,
                ZERO_ADDRESS,
                receiver_address,
            ]

        elif method == AtomicSwapMethod.SET_SECRET_LOCK:
            inputs = [
                CONSENSUS_ADDRESS,
            ]
            outputs = [
                CONSENSUS_ADDRESS,
            ]

        elif method == AtomicSwapMethod.APPROVE:
            inputs = [
                CONSENSUS_ADDRESS,
            ]
            outputs = [
                CONSENSUS_ADDRESS,
            ]

        inputs.extend(addresses)
        outputs.extend(addresses)

        return inputs, outputs

    @staticmethod
    def _generate_transaction_payload(method, data):
        return TransactionPayload(method=method, data=data).SerializeToString()

    async def _create_and_send_transaction(self, inputs, outputs, payload_bytes):

        transaction = await self._remme_transaction_service.create(
            family_name=self._family_name,
            family_version=self._family_version,
            inputs=inputs,
            outputs=outputs,
            payload_bytes=payload_bytes,
        )
        return await self._remme_transaction_service.send(payload=transaction)

    @staticmethod
    def _check_parameters(**parameters):
        """
        Check parameters such as swap_id, secret_lock (optional), secret_key (optional).
        """
        for key, value in parameters.items():

            if value is None:
                raise Exception(f'The `{key}` was missing in parameters.')

            elif re.search(RemmePatterns.SWAP_ID.value, value) is None:
                raise Exception(f'Given `{key}` is not a valid.')

    async def approve(self, swap_id):
        """
        Approve swap with given id.
        Send transaction into REMChain.

        Args:
            swap_id (string): swap id

        Returns:
            Object.

        To use:
            .. code-block:: python

                approve = await remme.swap.approve(swap_id)
                print(approve.batch_id)
        """
        self._check_parameters(swap_id=swap_id)

        payload = AtomicSwapApprovePayload(swap_id=swap_id).SerializeToString()
        transaction_payload = self._generate_transaction_payload(
            method=AtomicSwapMethod.APPROVE,
            data=payload,
        )
        inputs, outputs = self._get_addresses(
            method=AtomicSwapMethod.APPROVE,
            swap_id=swap_id,
        )

        return await self._create_and_send_transaction(
            inputs=inputs,
            outputs=outputs,
            payload_bytes=transaction_payload,
        )

    async def close(self, swap_id, secret_key):
        """
        Close swap with given id and secret key for checking who can close swap.
        Send transaction into REMChain.

        Args:
            swap_id (string): swap id
            secret_key (string): secret key

        Returns:
            Object.

        To use:
            .. code-block:: python

                close = await remme.swap.close(swap_id, secret_key)
                print(close.batch_id)
        """
        self._check_parameters(swap_id=swap_id, secret_key=secret_key)

        swap_info = await self.get_info(swap_id=swap_id)

        receiver_address = swap_info.receiver_address

        payload = AtomicSwapClosePayload(swap_id=swap_id, secret_key=secret_key).SerializeToString()
        transaction_payload = self._generate_transaction_payload(
            method=AtomicSwapMethod.CLOSE,
            data=payload,
        )

        inputs, outputs = self._get_addresses(
            method=AtomicSwapMethod.CLOSE,
            swap_id=swap_id,
            receiver_address=receiver_address,
        )

        return await self._create_and_send_transaction(
            inputs=inputs,
            outputs=outputs,
            payload_bytes=transaction_payload,
        )

    async def expire(self, swap_id):
        """
        Expire swap with given id. Could be expired after 24h after initiation.
        Send transaction into REMChain.

        Args:
            swap_id (string): swap id

        Returns:
            Object

        To use:
            .. code-block:: python

                expire = await remme.swap.expire(swap_id)
                print(expire.batch_id)
        """
        self._check_parameters(swap_id=swap_id)

        payload = AtomicSwapExpirePayload(swap_id=swap_id).SerializeToString()

        transaction_payload = self._generate_transaction_payload(
            method=AtomicSwapMethod.EXPIRE,
            data=payload,
        )

        inputs, outputs = self._get_addresses(
            method=AtomicSwapMethod.EXPIRE,
            swap_id=swap_id,
        )

        return await self._create_and_send_transaction(
            inputs=inputs,
            outputs=outputs,
            payload_bytes=transaction_payload,
        )

    async def get_info(self, swap_id):
        """
        Get info about swap by given swap id.

        Args:
            swap_id (string): swap id

        Returns:
            Information about swap.

        To use:
            .. code-block:: python

                info = await remme.swap.get_info(swap_id)
                print(info)  # SwapInfo
        """
        self._check_parameters(swap_id=swap_id)

        swap_data = await self._remme_api.send_request(
            method=RemmeMethods.ATOMIC_SWAP,
            params={'swap_id': swap_id},
        )

        return SwapInfo(data=swap_data)

    async def get_public_key(self):
        """
        Get swap public key.

        Returns:
            Swap public key.

        To use:
            .. code-block:: python

                public_key = await remme.swap.get_public_key()
                print(public_key)
        """
        return await self._remme_api.send_request(method=RemmeMethods.ATOMIC_SWAP_PUBLIC_KEY)

    async def init(self, **data):
        """
        Initiation of swap.
        Send transaction into REMChain.

        Args:
            data (kwargs): swap data

        Returns:
            Object.

        To use:
            .. code-block:: python

                swap_id = '133102e41346242476b15a3a7966eb5249271025fc7fb0b37ed3fdb4bcce3806'
                # hash from secret key that will be provided in close
                secret_lock_by_solicitor = 'b605112c2d7489034bbd7beab083fb65ba02af787786bb5e3d99bb26709f4f68'
                receiver_address = '112007484def48e1c6b77cf784aeabcac51222e48ae14f3821697f4040247ba01558b1'
                sender_address_non_local = '0xe6ca0e7c974f06471759e9a05d18b538c5ced11e'

                init = await remme.swap.init(
                    receiver_address=receiver_address,
                    sender_address_non_local=sender_address_non_local,
                    amount=100,
                    swap_id=swap_id,
                    secret_lock_by_solicitor=secret_lock_by_solicitor,
                )
                print(init.batch_id)
        """
        swap_init_data = SwapInitDto(data=data)
        swap_id = swap_init_data.swap_id

        payload = AtomicSwapInitPayload(
            receiver_address=swap_init_data.receiver_address,
            sender_address_non_local=swap_init_data.sender_address_non_local,
            amount=swap_init_data.amount,
            swap_id=swap_id,
            secret_lock_by_solicitor=swap_init_data.secret_lock_by_solicitor,
            email_address_encrypted_by_initiator=swap_init_data.email_address_encrypted_by_initiator,
        ).SerializeToString()

        transaction_payload = self._generate_transaction_payload(
            method=AtomicSwapMethod.INIT,
            data=payload,
        )

        inputs, outputs = self._get_addresses(
            method=AtomicSwapMethod.INIT,
            swap_id=swap_id,
        )

        return await self._create_and_send_transaction(
            inputs=inputs,
            outputs=outputs,
            payload_bytes=transaction_payload,
        )

    async def set_secret_lock(self, swap_id, secret_lock):
        """
        Set secret lock to swap with given swap id.
        Send transaction into REMChain.

        Args:
            swap_id (string): swap id
            secret_lock (string): hash from secret key that will be provided in close

        Returns:
            Object.

        To use:
            .. code-block:: python

                swap_id = '133102e41346242476b15a3a7966eb5249271025fc7fb0b37ed3fdb4bcce3806'
                secret_lock_by_solicitor = 'b605112c2d7489034bbd7beab083fb65ba02af787786bb5e3d99bb26709f4f68'
                setting = await remme.swap.set_secret_lock(
                    swap_id=swap_id,
                    secret_lock_by_solicitor=secret_lock_by_solicitor,
                )
                print(setting.batch_id)
        """
        self._check_parameters(swap_id=swap_id, secret_lock_by_solicitor=secret_lock)

        payload = AtomicSwapSetSecretLockPayload(
            swap_id=swap_id,
            secret_lock=secret_lock,
        ).SerializeToString()

        transaction_payload = self._generate_transaction_payload(
            method=AtomicSwapMethod.SET_SECRET_LOCK,
            data=payload,
        )

        inputs, outputs = self._get_addresses(
            method=AtomicSwapMethod.SET_SECRET_LOCK,
            swap_id=swap_id,
        )

        return await self._create_and_send_transaction(
            inputs=inputs,
            outputs=outputs,
            payload_bytes=transaction_payload,
        )
