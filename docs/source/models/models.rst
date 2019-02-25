
******
Models
******

Atomic Swap
===========

SwapInitDto
------------

.. autoclass:: remme.models.atomic_swap.swap_init_dto.SwapInitDto

Blockchain info
===============

BlockInfo
---------

.. autoclass:: remme.models.blockchain_info.block_info.BlockInfo

.. autoclass:: remme.models.blockchain_info.network_status.NetworkStatus

.. autoclass:: remme.models.blockchain_info.query.BaseQuery

.. autoclass:: remme.models.blockchain_info.query.StateQuery

Certificate
===========

CertificateTransactionResponse
------------------------------

.. autoclass:: remme.models.certificate.certificate_transaction_response.CertificateTransactionResponse

Keys
====

ECDSA
-----

.. autoclass:: remme.models.keys.ecdsa.ECDSA

    .. automethod:: remme.models.keys.ecdsa.ECDSA.__init__

    .. automethod:: remme.models.keys.ecdsa.ECDSA.generate_key_pair

    .. automethod:: remme.models.keys.ecdsa.ECDSA.get_address_from_public_key

    .. automethod:: remme.models.keys.ecdsa.ECDSA.sign

    .. automethod:: remme.models.keys.ecdsa.ECDSA.verify

EdDSA
-----

.. autoclass:: remme.models.keys.eddsa.EdDSA

    .. automethod:: remme.models.keys.eddsa.EdDSA.__init__

    .. automethod:: remme.models.keys.eddsa.EdDSA.generate_key_pair

    .. automethod:: remme.models.keys.eddsa.EdDSA.get_address_from_public_key

    .. automethod:: remme.models.keys.eddsa.EdDSA.sign

    .. automethod:: remme.models.keys.eddsa.EdDSA.verify

RSA
---

.. autoclass:: remme.models.keys.rsa.RSA

    .. automethod:: remme.models.keys.rsa.RSA.__init__

    .. automethod:: remme.models.keys.rsa.RSA.generate_key_pair

    .. automethod:: remme.models.keys.rsa.RSA.get_address_from_public_key

    .. automethod:: remme.models.keys.rsa.RSA.sign

    .. automethod:: remme.models.keys.rsa.RSA.verify

KeyDto
------

.. autoclass:: remme.models.keys.key_dto.KeyDto

    .. automethod:: remme.models.keys.key_dto.KeyDto.address

    .. automethod:: remme.models.keys.key_dto.KeyDto.private_key

    .. automethod:: remme.models.keys.key_dto.KeyDto.public_key

    .. automethod:: remme.models.keys.key_dto.KeyDto.private_key_hex

    .. automethod:: remme.models.keys.key_dto.KeyDto.public_key_hex

    .. automethod:: remme.models.keys.key_dto.KeyDto.key_type

    .. automethod:: remme.models.keys.key_dto.KeyDto.family_name

KeyType
-------

.. autoclass:: remme.models.keys.key_type.KeyType

    .. automethod:: remme.models.keys.key_type.KeyType.RSA
    .. automethod:: remme.models.keys.key_type.KeyType.ECDSA
    .. automethod:: remme.models.keys.key_type.KeyType.EdDSA

RsaSignaturePadding
-------------------

.. autoclass:: remme.models.keys.rsa_signature_padding.RsaSignaturePadding

    .. automethod:: remme.models.keys.rsa_signature_padding.RsaSignaturePadding.PSS
    .. automethod:: remme.models.keys.rsa_signature_padding.RsaSignaturePadding.PKCS1v15

Public key storage
==================

PublicKeyInfo
-------------

.. autoclass:: remme.models.public_key_storage.public_key_info.PublicKeyInfo

Transaction service
===================

BaseTransactionResponse
-----------------------

.. autoclass:: remme.models.transaction_service.base_transaction_response.BaseTransactionResponse

    .. automethod:: remme.models.transaction_service.base_transaction_response.BaseTransactionResponse.__init__

    .. automethod:: remme.models.transaction_service.base_transaction_response.BaseTransactionResponse.batch_id

Websocket
=========

BatchInfo
---------

.. autoclass:: remme.models.websocket.batch_info.BatchInfoDto

    .. automethod:: remme.models.websocket.batch_info.BatchInfoDto.__init__

BlockInfoDto
------------

.. autoclass:: remme.models.websocket.block_info.BlockInfoDto

    .. automethod:: remme.models.websocket.block_info.BlockInfoDto.__init__

SwapInfo
--------

.. autoclass:: remme.models.websocket.swap_info.SwapInfo

TransferInfoDto
---------------

.. autoclass:: remme.models.websocket.transfer_info.TransferInfoDto

    .. automethod:: remme.models.websocket.transfer_info.TransferInfoDto.__init__

RemmeEvents
-----------

.. autoclass:: remme.models.websocket.events.RemmeEvents

    .. automethod:: remme.models.websocket.events.RemmeEvents.AtomicSwap
    .. automethod:: remme.models.websocket.events.RemmeEvents.Batch
    .. automethod:: remme.models.websocket.events.RemmeEvents.Blocks
    .. automethod:: remme.models.websocket.events.RemmeEvents.Transfer

RemmeWebSocketMethods
---------------------

.. autoclass:: remme.models.websocket.methods.RemmeWebSocketMethods

    .. automethod:: remme.models.websocket.methods.RemmeWebSocketMethods.Subscribe
    .. automethod:: remme.models.websocket.methods.RemmeWebSocketMethods.Unsubscribe

RemmeRequestParams
------------------

.. autoclass:: remme.models.websocket.request_params.request_params.RemmeRequestParams

General enums
=============

BatchStatus
-----------

.. autoclass:: remme.models.general.batch_status.BatchStatus

    .. automethod:: remme.models.general.batch_status.BatchStatus.UNKNOWN
    .. automethod:: remme.models.general.batch_status.BatchStatus.INVALID
    .. automethod:: remme.models.general.batch_status.BatchStatus.PENDING
    .. automethod:: remme.models.general.batch_status.BatchStatus.COMMITTED

RemmeMethods
------------

.. autoclass:: remme.models.general.methods.RemmeMethods

    .. automethod:: remme.models.general.methods.RemmeMethods.PUBLIC_KEY
    .. automethod:: remme.models.general.methods.RemmeMethods.TOKEN
    .. automethod:: remme.models.general.methods.RemmeMethods.BATCH_STATUS
    .. automethod:: remme.models.general.methods.RemmeMethods.ATOMIC_SWAP
    .. automethod:: remme.models.general.methods.RemmeMethods.ATOMIC_SWAP_PUBLIC_KEY
    .. automethod:: remme.models.general.methods.RemmeMethods.USER_PUBLIC_KEY
    .. automethod:: remme.models.general.methods.RemmeMethods.NODE_KEY
    .. automethod:: remme.models.general.methods.RemmeMethods.NODE_CONFIG
    .. automethod:: remme.models.general.methods.RemmeMethods.NODE_PRIVATE_KEY
    .. automethod:: remme.models.general.methods.RemmeMethods.TRANSACTION
    .. automethod:: remme.models.general.methods.RemmeMethods.NETWORK_STATUS
    .. automethod:: remme.models.general.methods.RemmeMethods.BLOCK_INFO
    .. automethod:: remme.models.general.methods.RemmeMethods.BLOCKS
    .. automethod:: remme.models.general.methods.RemmeMethods.FETCH_BLOCK
    .. automethod:: remme.models.general.methods.RemmeMethods.BATCHES
    .. automethod:: remme.models.general.methods.RemmeMethods.FETCH_BATCH
    .. automethod:: remme.models.general.methods.RemmeMethods.TRANSACTIONS
    .. automethod:: remme.models.general.methods.RemmeMethods.FETCH_TRANSACTION
    .. automethod:: remme.models.general.methods.RemmeMethods.STATE
    .. automethod:: remme.models.general.methods.RemmeMethods.FETCH_STATE
    .. automethod:: remme.models.general.methods.RemmeMethods.PEERS
    .. automethod:: remme.models.general.methods.RemmeMethods.RECEIPTS

RemmeFamilyName
---------------

.. autoclass:: remme.models.utils.family_name.RemmeFamilyName

    .. automethod:: remme.models.utils.family_name.RemmeFamilyName.ACCOUNT
    .. automethod:: remme.models.utils.family_name.RemmeFamilyName.PUBLIC_KEY
    .. automethod:: remme.models.utils.family_name.RemmeFamilyName.SWAP

RemmeNamespace
--------------

.. autoclass:: remme.models.utils.namespace.RemmeNamespace

    .. automethod:: remme.models.utils.namespace.RemmeNamespace.ACCOUNT
    .. automethod:: remme.models.utils.namespace.RemmeNamespace.PUBLIC_KEY
    .. automethod:: remme.models.utils.namespace.RemmeNamespace.SWAP

Interfaces
==========

IRemmeAPI
---------

.. autoclass:: remme.models.interfaces.api.IRemmeAPI

    .. automethod:: remme.models.interfaces.api.IRemmeAPI.send_request

IRemmeSwap
----------

.. autoclass:: remme.models.interfaces.atomic_swap.IRemmeSwap

    .. automethod:: remme.models.interfaces.atomic_swap.IRemmeSwap.init

    .. automethod:: remme.models.interfaces.atomic_swap.IRemmeSwap.approve

    .. automethod:: remme.models.interfaces.atomic_swap.IRemmeSwap.expire

    .. automethod:: remme.models.interfaces.atomic_swap.IRemmeSwap.set_secret_lock

    .. automethod:: remme.models.interfaces.atomic_swap.IRemmeSwap.close

    .. automethod:: remme.models.interfaces.atomic_swap.IRemmeSwap.get_info

    .. automethod:: remme.models.interfaces.atomic_swap.IRemmeSwap.get_public_key

IRemmeBlockchainInfo
--------------------

.. autoclass:: remme.models.interfaces.blockchain_info.IRemmeBlockchainInfo

    .. automethod:: remme.models.interfaces.blockchain_info.IRemmeBlockchainInfo.get_transactions

    .. automethod:: remme.models.interfaces.blockchain_info.IRemmeBlockchainInfo.get_transaction_by_id

    .. automethod:: remme.models.interfaces.blockchain_info.IRemmeBlockchainInfo.parse_transaction_payload

    .. automethod:: remme.models.interfaces.blockchain_info.IRemmeBlockchainInfo.get_blocks

    .. automethod:: remme.models.interfaces.blockchain_info.IRemmeBlockchainInfo.get_block_by_id

    .. automethod:: remme.models.interfaces.blockchain_info.IRemmeBlockchainInfo.get_block_info

    .. automethod:: remme.models.interfaces.blockchain_info.IRemmeBlockchainInfo.get_batches

    .. automethod:: remme.models.interfaces.blockchain_info.IRemmeBlockchainInfo.get_batches_by_id

    .. automethod:: remme.models.interfaces.blockchain_info.IRemmeBlockchainInfo.get_batch_status

    .. automethod:: remme.models.interfaces.blockchain_info.IRemmeBlockchainInfo.get_state

    .. automethod:: remme.models.interfaces.blockchain_info.IRemmeBlockchainInfo.get_state_by_address

    .. automethod:: remme.models.interfaces.blockchain_info.IRemmeBlockchainInfo.parse_state_data

    .. automethod:: remme.models.interfaces.blockchain_info.IRemmeBlockchainInfo.get_peers

    .. automethod:: remme.models.interfaces.blockchain_info.IRemmeBlockchainInfo.get_network_status

IRemmeCertificate
-----------------

.. autoclass:: remme.models.interfaces.certificate.IRemmeCertificate

    .. automethod:: remme.models.interfaces.certificate.IRemmeCertificate.create

    .. automethod:: remme.models.interfaces.certificate.IRemmeCertificate.create_and_store

    .. automethod:: remme.models.interfaces.certificate.IRemmeCertificate.store

    .. automethod:: remme.models.interfaces.certificate.IRemmeCertificate.check

    .. automethod:: remme.models.interfaces.certificate.IRemmeCertificate.revoke

    .. automethod:: remme.models.interfaces.certificate.IRemmeCertificate.get_info

    .. automethod:: remme.models.interfaces.certificate.IRemmeCertificate.sign

    .. automethod:: remme.models.interfaces.certificate.IRemmeCertificate.verify

IRemmeKeys
----------

.. autoclass:: remme.models.interfaces.keys.IRemmeKeys

    .. automethod:: remme.models.interfaces.keys.IRemmeKeys.sign

    .. automethod:: remme.models.interfaces.keys.IRemmeKeys.verify

IRemmePublicKeyStorage
----------------------

.. autoclass:: remme.models.interfaces.public_key_storage.IRemmePublicKeyStorage

    .. automethod:: remme.models.interfaces.public_key_storage.IRemmePublicKeyStorage.create

    .. automethod:: remme.models.interfaces.public_key_storage.IRemmePublicKeyStorage.store

    .. automethod:: remme.models.interfaces.public_key_storage.IRemmePublicKeyStorage.create_and_store

    .. automethod:: remme.models.interfaces.public_key_storage.IRemmePublicKeyStorage.check

    .. automethod:: remme.models.interfaces.public_key_storage.IRemmePublicKeyStorage.revoke

    .. automethod:: remme.models.interfaces.public_key_storage.IRemmePublicKeyStorage.get_info

    .. automethod:: remme.models.interfaces.public_key_storage.IRemmePublicKeyStorage.get_account_public_keys

IRemmeToken
-----------

.. autoclass:: remme.models.interfaces.token.IRemmeToken

    .. automethod:: remme.models.interfaces.token.IRemmeToken.get_balance

    .. automethod:: remme.models.interfaces.token.IRemmeToken.transfer

IRemmeTransactionService
------------------------

.. autoclass:: remme.models.interfaces.transaction_service.IRemmeTransactionService

    .. automethod:: remme.models.interfaces.transaction_service.IRemmeTransactionService.create

    .. automethod:: remme.models.interfaces.transaction_service.IRemmeTransactionService.send

IRemmeWebSocket
---------------

.. autoclass:: remme.models.interfaces.websocket.IRemmeWebSocket

    .. automethod:: remme.models.interfaces.websocket.IRemmeWebSocket.connect_to_web_socket

    .. automethod:: remme.models.interfaces.websocket.IRemmeWebSocket.close_web_socket

IRemmeWebSocketsEvents
----------------------

.. autoclass:: remme.models.interfaces.websocket_events.IRemmeWebSocketsEvents

    .. automethod:: remme.models.interfaces.websocket_events.IRemmeWebSocketsEvents.subscribe

    .. automethod:: remme.models.interfaces.websocket_events.IRemmeWebSocketsEvents.unsubscribe
