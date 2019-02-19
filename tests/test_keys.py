"""
Provide tests for Remme keys implementation.
"""
import pytest
import re

from remme.keys import RemmeKeys as keys
from remme.models.general.patterns import RemmePatterns
from remme.models.keys.ecdsa import ECDSA
from remme.models.keys.eddsa import EdDSA
from remme.models.keys.rsa import RSA
from remme.models.keys.key_type import KeyType
from tests.utils import (
    PRIVATE_KEY_HEX_ECDSA,
    PRIVATE_KEY_HEX_EDDSA,
    PRIVATE_KEY_HEX_RSA,
    PUBLIC_KEY_HEX_ECDSA,
    PUBLIC_KEY_HEX_EDDSA,
    PUBLIC_KEY_HEX_RSA,
)


@pytest.mark.parametrize('key_type', [
    KeyType.RSA, KeyType.ECDSA, KeyType.EdDSA,
])
def test_generate_key_pair(key_type):
    """
    Case: generate key pair for RSA, ECDSA (secp256k1), EdDSA (ed25519).
    Expect: key pair in bytes.
    """
    private_key, public_key = keys.generate_key_pair(key_type=key_type)

    assert isinstance(private_key, bytes) and isinstance(public_key, bytes)


@pytest.mark.parametrize('key_type, public_key', [
    (KeyType.RSA, PUBLIC_KEY_HEX_RSA),
    (KeyType.ECDSA, PUBLIC_KEY_HEX_ECDSA),
    (KeyType.EdDSA, PUBLIC_KEY_HEX_EDDSA),
])
def test_get_address_from_public_key(key_type, public_key):
    """
    Case: get address from public key hex by RSA, ECDSA (secp256k1), EdDSA (ed25519).
    Expect: address (hex format) in blockchain generated from public key.
    """
    address = keys.get_address_from_public_key(key_type=key_type, public_key=public_key)

    assert isinstance(address, str) and re.match(RemmePatterns.ADDRESS.value, address) is not None


@pytest.mark.parametrize('key_type, class_type', [
    (KeyType.RSA, RSA),
    (KeyType.ECDSA, ECDSA),
    (KeyType.EdDSA, EdDSA),
])
def test_construct_without_keys(key_type, class_type):
    """
    Case: construct without RSA, ECDSA (secp256k1), EdDSA (ed25519) keys.
    Expect: key object.
    """
    remme_keys_object = keys.construct(key_type=key_type)

    assert isinstance(remme_keys_object, class_type)


@pytest.mark.parametrize('key_type, class_type, private_key, public_key', [
    (KeyType.RSA, RSA, PRIVATE_KEY_HEX_RSA, PUBLIC_KEY_HEX_RSA),
    (KeyType.ECDSA, ECDSA, PRIVATE_KEY_HEX_ECDSA, PUBLIC_KEY_HEX_ECDSA),
    (KeyType.EdDSA, EdDSA, PRIVATE_KEY_HEX_EDDSA, PUBLIC_KEY_HEX_EDDSA),
])
def test_construct_with_keys(key_type, class_type, private_key, public_key):
    """
    Case: construct with RSA, ECDSA (secp256k1), EdDSA (ed25519) keys.
    Expect: key object.
    """
    remme_keys_object = keys.construct(key_type=key_type)

    assert isinstance(remme_keys_object, class_type)


@pytest.mark.parametrize('key_type, class_type, private_key', [
    (KeyType.RSA, RSA, PRIVATE_KEY_HEX_RSA),
    (KeyType.ECDSA, ECDSA, PRIVATE_KEY_HEX_ECDSA),
    (KeyType.EdDSA, EdDSA, PRIVATE_KEY_HEX_EDDSA),
])
def test_construct_with_private_key(key_type, class_type, private_key):
    """
    Case: construct with RSA, ECDSA (secp256k1), EdDSA (ed25519) private key.
    Expect: key object.
    """
    remme_keys_object = keys.construct(key_type=key_type)

    assert isinstance(remme_keys_object, class_type)


@pytest.mark.parametrize('key_type, class_type, public_key', [
    (KeyType.RSA, RSA, PUBLIC_KEY_HEX_RSA),
    (KeyType.ECDSA, ECDSA, PUBLIC_KEY_HEX_ECDSA),
    (KeyType.EdDSA, EdDSA, PUBLIC_KEY_HEX_EDDSA),
])
def test_construct_with_public_key(key_type, class_type, public_key):
    """
    Case: construct with RSA, ECDSA (secp256k1), EdDSA (ed25519) public key.
    Expect: key object.
    """
    remme_keys_object = keys.construct(key_type=key_type)

    assert isinstance(remme_keys_object, class_type)
