import base64
import hashlib
import math
import random
import re

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

from remme.enums.remme_patterns import RemmePatterns
from remme.enums.rsa_signature_padding import RsaSignaturePadding
from remme.protos.pub_key_pb2 import NewPubKeyPayload


def validate_amount(amount):
    """
    Validate amount.
    """
    if not isinstance(amount, int):
        raise Exception('Given amount is not in integer type.')

    if amount <= 0:
        raise Exception('Given amount is not valid for operations.')


def validate_public_key(public_key):
    """
    Validate public key.
    """
    if public_key == '':
        raise Exception('Public key was not provided, please set the public key.')

    if len(public_key) != 66:
        raise Exception('Length of the given public key is not valid.')

    if not re.match(pattern=RemmePatterns.PUBLIC_KEY.value, string=public_key):
        raise Exception('Given public key is not in hexadecimal string format.')


def validate_address(address):
    """
    Validate address.
    """
    if address == '':
        raise Exception('Address was not provided, please set the address.')

    if len(address) != 70:
        raise Exception('Length of the given address is not valid.')

    if not re.match(pattern=RemmePatterns.ADDRESS.value, string=address):
        raise Exception('Given address is not in hexadecimal string format.')


def is_valid_batch_id(_batch_id):
    return re.match(RemmePatterns.HEADER_SIGNATURE.value, _batch_id) is not None


def bytes_to_hex(_bytes):
    return utf8_to_bytes(_bytes).hex()


def base64_to_dict(_base64):
    return eval(base64.b64decode(_base64))


def dict_to_base64(_dict):
    return base64.b64encode(str(_dict).encode('utf-8'))


def utf8_to_bytes(_string):
    return _string.encode('UTF-8')


def bytes_to_utf8(_bytes):
    return _bytes.decode('UTF-8')


def is_string_or_bytes(message):
    return isinstance(message, str) or isinstance(message, bytes)


def is_valid_hex_string(message):
    return isinstance(message, str) and is_hex(message)


def hex_to_bytes(message):
    if isinstance(message, bytes):
        return message
    if is_valid_hex_string(message):
        return bytes.fromhex(message)
    raise Exception("Invalid type of message given. Expected hex string or bytes.")


def create_nonce():
    hash_o = hashlib.sha512(str(math.floor(1000 * random.random())).encode('UTF-8'))
    result = hash_o.hexdigest()
    return result


def sha512_hexdigest(data):
    return hashlib.sha512(data.encode('utf-8') if isinstance(data, str) else data).hexdigest()


def sha256_hexdigest(data):
    return hashlib.sha256(data.encode('utf-8') if isinstance(data, str) else data).hexdigest()


def is_hex(data):
    try:
        int(data, 16)
        return True
    except ValueError:
        return False


def generate_address(_family_name, _public_key_to):
    return "" + sha512_hexdigest(_family_name)[:6] + sha512_hexdigest(_public_key_to)[:64]


def generate_settings_address(key):
    key_parts = key.split(".")[:4]
    address_parts = [sha256_hexdigest(x)[0:16] for x in key_parts]
    while (4 - len(address_parts)) != 0:
        address_parts.append(sha256_hexdigest("")[0:16])
    return "000000" + "".join(address_parts)


def public_key_address(value):
    return {'public_key_address': value}


def public_key_to_der(public_key):
    """
    Convert public key object to DER format.
    :param public_key
    :return: DER bytes format
    """
    return public_key.public_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )


def public_key_to_pem(public_key):
    """
    Convert public key object to PEM format.
    :param public_key
    :return: PEM string format
    """
    return public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )


def private_key_to_pem(private_key):
    """
    Convert private key object to PEM format.
    :param private_key
    :return: PEM string format
    """
    return private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )


def private_key_pem_to_object(private_key):
    """
    Convert private key in PEM format to RSA object.
    :param private_key: RSA private key
    :return: private key object
    """
    return serialization.load_pem_private_key(
        data=private_key,
        password=None,
        backend=default_backend(),
    )


def public_key_pem_to_object(public_key):
    """
    Convert public key in PEM format to RSA object.
    :param public_key: RSA public key
    :return: public key object
    """
    return serialization.load_pem_public_key(
        data=public_key,
        backend=default_backend(),
    )


def get_padding(padding):

    if padding == RsaSignaturePadding.PSS:
        return NewPubKeyPayload.RSAConfiguration.Padding.Value('PSS')

    if padding == RsaSignaturePadding.PKCS1v15:
        return NewPubKeyPayload.RSAConfiguration.Padding.Value('PKCS1v15')


def get_hashing_algorithm(padding):
    if padding == RsaSignaturePadding.PSS:
        return NewPubKeyPayload.HashingAlgorithm.Value('SHA256')

    if padding == RsaSignaturePadding.PKCS1v15:
        return  NewPubKeyPayload.HashingAlgorithm.Value('SHA512')


def generate_rsa_payload(
        message, keys, public_key, valid_from, valid_to, rsa_signature_padding=RsaSignaturePadding.PSS
):
    entity_hash = message.encode('utf-8')
    entity_hash_signature = keys.sign(data=entity_hash, rsa_signature_padding=rsa_signature_padding)

    return NewPubKeyPayload(
        entity_hash=entity_hash,
        entity_hash_signature=entity_hash_signature,
        valid_from=valid_from,
        valid_to=valid_to,
        rsa=NewPubKeyPayload.RSAConfiguration(
            padding=get_padding(padding=rsa_signature_padding),
            key=public_key,
        ),
        hashing_algorithm=get_hashing_algorithm(padding=rsa_signature_padding),
    )


def generate_eddsa_payload(message, keys, public_key, valid_from, valid_to):

    entity_hash = message.encode('utf-8')
    entity_hash_signature = keys.sign(data=entity_hash)

    return NewPubKeyPayload(
        entity_hash=entity_hash,
        entity_hash_signature=entity_hash_signature,
        valid_from=valid_from,
        valid_to=valid_to,
        ed25519=NewPubKeyPayload.Ed25519Configuration(
            key=public_key,
        ),
        hashing_algorithm=NewPubKeyPayload.HashingAlgorithm.Value('SHA512'),
    )


def generate_ecdsa_payload(message, keys, public_key, valid_from, valid_to):

    entity_hash = message.encode('utf-8')
    entity_hash_signature = keys.sign(data=entity_hash)

    return NewPubKeyPayload(
        entity_hash=entity_hash,
        entity_hash_signature=entity_hash_signature,
        valid_from=valid_from,
        valid_to=valid_to,
        ecdsa=NewPubKeyPayload.ECDSAConfiguration(
            key=public_key,
            ec=NewPubKeyPayload.ECDSAConfiguration.EC.Value('SECP256k1'),
        ),
        hashing_algorithm=NewPubKeyPayload.HashingAlgorithm.Value('SHA256'),
    )
