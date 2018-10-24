import hashlib
import base64
import math
import random


def hex_to_bytes(_hex_string):
    print(f"functions; hex_to_bytes args: {_hex_string}")
    result = bytes.fromhex(_hex_string)
    print(f"functions; hex_to_bytes result: {result}")
    return result


def bytes_to_hex(_bytes):
    print(f"functions; bytes_to_hex args: {_bytes}")
    result = utf8_to_bytes(_bytes).hex()
    print(f"functions; bytes_to_hex result: {result}")
    return result


def base64_to_dict(_base64):
    return eval(base64.b64decode(_base64))


def dict_to_base64(_dict):
    return base64.b64encode(str(_dict).encode('utf-8'))


def utf8_to_bytes(_string):
    return _string if isinstance(_string, bytes) else _string.encode('UTF-8')


def to_hex(_string):
    return utf8_to_bytes(_string).hex()


def to_hex_string(_byte_array):
    raise NotImplementedError


def to_utf8_array(_string):
    raise NotImplementedError


def certificate_to_pem(certificate):
    raise NotImplementedError


def certificate_from_pem(certificate):
    raise NotImplementedError


def public_key_to_pem(public_key):
    raise NotImplementedError


def public_key_from_pem(public_key):
    raise NotImplementedError


def generate_address(_family_name, _public_key_to):
    print(f"utils; generate_address args: {_family_name}  ,  {_public_key_to}")
    family_name_o = hashlib.sha512(utf8_to_bytes(_family_name))
    data_o = hashlib.sha512(utf8_to_bytes(_public_key_to))
    result = "" + family_name_o.hexdigest()[slice(0, 6)] + data_o.hexdigest()[slice(0, 64)]
    print(f"utils; generate_address result: {result}")
    return result


def create_nonce():
    print(f"utils; generate nonce")
    hash_o = hashlib.sha512(str(math.floor(1000 * random.random())).encode('UTF-8'))
    result = hash_o.hexdigest()
    print(f"utils; generate nonce result: {result}")
    return result


def sha512_hexdigest(_value):
    hash_o = hashlib.sha512(str(_value).encode('UTF-8'))
    return hash_o.hexdigest()
