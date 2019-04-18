"""
Provide constants.
"""
from remme.models.utils.family_name import RemmeFamilyName
from remme.utils import sha512_hexdigest


CONSENSUS_ADDRESS = f'{sha512_hexdigest(RemmeFamilyName.CONSENSUS_ACCOUNT.value)[:6]}{"0" * 64}'
