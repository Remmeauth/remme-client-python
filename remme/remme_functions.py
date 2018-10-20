import hashlib


def hex_to_bytes(_string):
    raise NotImplementedError


def bytes_to_hex(_uint8arr):
    raise NotImplementedError


def base64_to_array_buffer(_base64):
    raise NotImplementedError


def utf8_to_bytes(_string):
    raise NotImplementedError


def to_hex(_string):
    raise NotImplementedError


def get_address_from_data(_family_name, _data):
    print(f"get_address_from_data args: {_family_name}  ,  {_data}")
    _family_name = _family_name if isinstance(_family_name, bytes) else _family_name.encode('UTF-8')
    _data = _data if isinstance(_data, bytes) else _data.encode('UTF-8')
    family_name_o = hashlib.sha512(_family_name)
    data_o = hashlib.sha512(_data)
    result = "" + family_name_o.hexdigest()[slice(0, 6)] + data_o.hexdigest()[slice(0, 64)]
    print(f"get_address_from_data result: {result}")
    return result


def to_hex_string(_byte_array):
    raise NotImplementedError


def to_utf8_array(_string):
    raise NotImplementedError
