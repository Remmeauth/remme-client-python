import base64
import codecs
import hashlib
import json
import math
import random
import re

from Crypto.Hash import keccak
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

from remme.models.general.patterns import RemmePatterns
from remme.models.keys.rsa_signature_padding import RsaSignaturePadding
from remme.protobuf.pub_key_pb2 import NewPubKeyPayload

HEX = re.compile(r'^[0-9a-f]+$')


def validate_amount(amount):
    """
    Validate amount.
    """
    if not amount:
        raise Exception('Amount was not provided, please set the amount.')

    if not isinstance(amount, int):
        raise Exception('Given amount is not in integer type.')

    if amount <= 0:
        raise Exception('Given amount must be higher than 0.')


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


def check_sha256(data):

    if re.match(RemmePatterns.SHA256.value, data) is None:
        raise Exception('Value should be SHA-256.')


def check_sha512(data):

    if re.match(RemmePatterns.SHA512.value, data) is None:
        raise Exception('Value should be SHA-512.')


def check_sha(data):

    if re.match(RemmePatterns.SHA256.value, data) is None \
            and re.match(RemmePatterns.SHA512.value, data) is None:
        raise Exception('Value should be SHA-256 or SHA-512.')


def validate_node_config(network_config):

    node_address, ssl_mode = network_config.get('node_address'), network_config.get('ssl_mode')

    if re.match(RemmePatterns.PROTOCOL.value, node_address) is None:
        raise Exception('You try construct with invalid `node_address`, remove protocol and try again.')

    elif not isinstance(ssl_mode, bool):
        raise Exception('You try construct with invalid `ssl_mode`, `ssl_mode` should has boolean type.')


def sha512_hexdigest(data):
    return hashlib.sha512(data.encode('utf-8') if isinstance(data, str) else data).hexdigest()


def sha256_hexdigest(data):
    return hashlib.sha256(data.encode('utf-8') if isinstance(data, str) else data).hexdigest()


def is_hex(data):
    return HEX.search(data) is not None


def remove_0x_prefix(value):
    if value.startswith('0x'):
        return value[2:]
    return value


def web3_hash(data):
    if len(data) % 2:
        data = '0x0' + remove_0x_prefix(data)

    data = codecs.decode(remove_0x_prefix(data), 'hex')
    keccak_hash = keccak.new(digest_bits=256)
    keccak_hash.update(data)
    return keccak_hash.hexdigest()


def generate_address(_family_name, _public_key_to):
    return f'{sha512_hexdigest(_family_name)[:6]}{sha512_hexdigest(_public_key_to)[:64]}'


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


def private_key_to_der(private_key):
    """
    Convert private key object to DER format.
    :param private_key
    :return: DER bytes format
    """
    return private_key.private_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption(),
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


def private_key_der_to_object(private_key):
    """
    Convert private key in DER format to RSA object.
    :param private_key: RSA private key in bytes
    :return: private key object
    """
    return serialization.load_der_private_key(
        data=private_key,
        password=None,
        backend=default_backend(),
    )


def public_key_der_to_object(public_key):
    """
    Convert public key in DER format to RSA object.
    :param public_key: RSA public key in bytes
    :return: public key object
    """
    return serialization.load_der_public_key(
        data=public_key,
        backend=default_backend(),
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


def certificate_to_pem(certificate):
    """
    Convert certificate object to PEM format.
    :param certificate: object
    :return: certificate in PEM format: string
    """
    try:
        return certificate.public_bytes(encoding=serialization.Encoding.PEM)
    except Exception:
        return "Given certificate is not a valid"


def certificate_from_pem(certificate):
    """
    Convert certificate in PEM format to certificate object.
    :param certificate: string
    :return: certificate: object
    """
    try:
        return x509.load_pem_x509_certificate(certificate, default_backend())
    except Exception:
        return "Given certificate is not a valid"


def get_namespace_params(type, parser):
    """
    Get namespace parameters.
    :param type: string
    :param parser: bytes
    :return: dict
    """
    return {
        'type': type,
        'parser': parser,
    }


def dict_to_pretty_json(data):
    """
    Convert dictionary to string with indents as human readable text.
    """
    return json.dumps(data, indent=4, sort_keys=True)
