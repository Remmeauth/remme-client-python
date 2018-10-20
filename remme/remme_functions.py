import hashlib
import base64


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


def base64_to_byte_array(_base64):
    base64.b64decode(_base64)
    raise NotImplementedError


def utf8_to_bytes(_string):
    return _string if isinstance(_string, bytes) else _string.encode('UTF-8')


def to_hex(_string):
    return utf8_to_bytes(_string).hex()


def get_address_from_data(_family_name, _data):
    print(f"functions; get_address_from_data args: {_family_name}  ,  {_data}")
    family_name_o = hashlib.sha512(utf8_to_bytes(_family_name))
    data_o = hashlib.sha512(utf8_to_bytes(_data))
    result = "" + family_name_o.hexdigest()[slice(0, 6)] + data_o.hexdigest()[slice(0, 64)]
    print(f"functions; get_address_from_data result: {result}")
    return result


def to_hex_string(_byte_array):
    raise NotImplementedError


def to_utf8_array(_string):
    raise NotImplementedError

