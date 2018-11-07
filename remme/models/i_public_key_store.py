from remme.constants.pub_key_type import PubKeyType
from remme.constants.entity_type import EntityType


class IPublicKeyStore:
    """
    Interface that take method store in publicKeyStorage
    """

    _data = None
    _public_key = None
    _valid_from = None
    _valid_to = None
    _private_key = None
    _public_key_type = None
    _entity_type = None

    def __init__(self, data, public_key, valid_from, valid_to, private_key,
                 public_key_type=PubKeyType.RSA.value, entity_type=EntityType.PERSONAL.value):
        """
        :param data: {string}
        :param public_key: {node-forge.pki.Key | node-forge.pki.PEM}
        :param valid_from: {node-forge.pki.Key | node-forge.pki.PEM}
        :param valid_to: {integer}
        :param private_key: {integer}
        :param public_key_type: {NewPubKeyPayload.PubKeyType}
        :param entity_type: {NewPubKeyPayload.EntityType}
        """
        self._data = data
        self._public_key = public_key
        self._valid_from = valid_from
        self._valid_to = valid_to
        self._private_key = private_key
        self._public_key_type = public_key_type
        self._entity_type = entity_type
