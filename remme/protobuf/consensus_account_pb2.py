# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: consensus_account.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='consensus_account.proto',
  package='',
  syntax='proto3',
  serialized_pb=_b('\n\x17\x63onsensus_account.proto\"@\n\x16\x43onsensusAccountMethod\"&\n\x06Method\x12\x0f\n\x0bSEND_REWARD\x10\x00\x12\x0b\n\x07GENESIS\x10\x01\"\xaf\x01\n\x10\x43onsensusAccount\x12\x12\n\npublic_key\x18\x01 \x01(\t\x12\x1b\n\x13obligatory_payments\x18\x02 \x01(\x04\x12\x12\n\nblock_cost\x18\x03 \x01(\x04\x12)\n\x04\x62\x65ts\x18\x04 \x03(\x0b\x32\x1b.ConsensusAccount.BetsEntry\x1a+\n\tBetsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\x04:\x02\x38\x01\x62\x06proto3')
)



_CONSENSUSACCOUNTMETHOD_METHOD = _descriptor.EnumDescriptor(
  name='Method',
  full_name='ConsensusAccountMethod.Method',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='SEND_REWARD', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='GENESIS', index=1, number=1,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=53,
  serialized_end=91,
)
_sym_db.RegisterEnumDescriptor(_CONSENSUSACCOUNTMETHOD_METHOD)


_CONSENSUSACCOUNTMETHOD = _descriptor.Descriptor(
  name='ConsensusAccountMethod',
  full_name='ConsensusAccountMethod',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _CONSENSUSACCOUNTMETHOD_METHOD,
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=27,
  serialized_end=91,
)


_CONSENSUSACCOUNT_BETSENTRY = _descriptor.Descriptor(
  name='BetsEntry',
  full_name='ConsensusAccount.BetsEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='ConsensusAccount.BetsEntry.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='value', full_name='ConsensusAccount.BetsEntry.value', index=1,
      number=2, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=_descriptor._ParseOptions(descriptor_pb2.MessageOptions(), _b('8\001')),
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=226,
  serialized_end=269,
)

_CONSENSUSACCOUNT = _descriptor.Descriptor(
  name='ConsensusAccount',
  full_name='ConsensusAccount',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='public_key', full_name='ConsensusAccount.public_key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='obligatory_payments', full_name='ConsensusAccount.obligatory_payments', index=1,
      number=2, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='block_cost', full_name='ConsensusAccount.block_cost', index=2,
      number=3, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='bets', full_name='ConsensusAccount.bets', index=3,
      number=4, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[_CONSENSUSACCOUNT_BETSENTRY, ],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=94,
  serialized_end=269,
)

_CONSENSUSACCOUNTMETHOD_METHOD.containing_type = _CONSENSUSACCOUNTMETHOD
_CONSENSUSACCOUNT_BETSENTRY.containing_type = _CONSENSUSACCOUNT
_CONSENSUSACCOUNT.fields_by_name['bets'].message_type = _CONSENSUSACCOUNT_BETSENTRY
DESCRIPTOR.message_types_by_name['ConsensusAccountMethod'] = _CONSENSUSACCOUNTMETHOD
DESCRIPTOR.message_types_by_name['ConsensusAccount'] = _CONSENSUSACCOUNT
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

ConsensusAccountMethod = _reflection.GeneratedProtocolMessageType('ConsensusAccountMethod', (_message.Message,), dict(
  DESCRIPTOR = _CONSENSUSACCOUNTMETHOD,
  __module__ = 'consensus_account_pb2'
  # @@protoc_insertion_point(class_scope:ConsensusAccountMethod)
  ))
_sym_db.RegisterMessage(ConsensusAccountMethod)

ConsensusAccount = _reflection.GeneratedProtocolMessageType('ConsensusAccount', (_message.Message,), dict(

  BetsEntry = _reflection.GeneratedProtocolMessageType('BetsEntry', (_message.Message,), dict(
    DESCRIPTOR = _CONSENSUSACCOUNT_BETSENTRY,
    __module__ = 'consensus_account_pb2'
    # @@protoc_insertion_point(class_scope:ConsensusAccount.BetsEntry)
    ))
  ,
  DESCRIPTOR = _CONSENSUSACCOUNT,
  __module__ = 'consensus_account_pb2'
  # @@protoc_insertion_point(class_scope:ConsensusAccount)
  ))
_sym_db.RegisterMessage(ConsensusAccount)
_sym_db.RegisterMessage(ConsensusAccount.BetsEntry)


_CONSENSUSACCOUNT_BETSENTRY.has_options = True
_CONSENSUSACCOUNT_BETSENTRY._options = _descriptor._ParseOptions(descriptor_pb2.MessageOptions(), _b('8\001'))
# @@protoc_insertion_point(module_scope)