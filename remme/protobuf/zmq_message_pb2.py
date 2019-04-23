# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: zmq_message.proto

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
  name='zmq_message.proto',
  package='',
  syntax='proto3',
  serialized_pb=_b('\n\x11zmq_message.proto\"1\n\x0cMessageError\x12\x13\n\x0b\x64\x65scription\x18\x01 \x01(\t\x12\x0c\n\x04\x63ode\x18\x02 \x01(\x04\"\xb5\x01\n\x07Message\x12*\n\x0cmessage_type\x18\x01 \x01(\x0e\x32\x14.Message.MessageType\x12\x16\n\x0e\x63orrelation_id\x18\x02 \x01(\t\x12\x0f\n\x07\x63ontent\x18\x03 \x01(\x0c\"U\n\x0bMessageType\x12\x17\n\x13\x43LIENT_SEAL_REQUEST\x10\x00\x12\x18\n\x14\x43LIENT_SEAL_RESPONSE\x10\x01\x12\x13\n\x0fINVALID_MESSAGE\x10\x02\x62\x06proto3')
)



_MESSAGE_MESSAGETYPE = _descriptor.EnumDescriptor(
  name='MessageType',
  full_name='Message.MessageType',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='CLIENT_SEAL_REQUEST', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CLIENT_SEAL_RESPONSE', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='INVALID_MESSAGE', index=2, number=2,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=169,
  serialized_end=254,
)
_sym_db.RegisterEnumDescriptor(_MESSAGE_MESSAGETYPE)


_MESSAGEERROR = _descriptor.Descriptor(
  name='MessageError',
  full_name='MessageError',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='description', full_name='MessageError.description', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='code', full_name='MessageError.code', index=1,
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
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=21,
  serialized_end=70,
)


_MESSAGE = _descriptor.Descriptor(
  name='Message',
  full_name='Message',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='message_type', full_name='Message.message_type', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='correlation_id', full_name='Message.correlation_id', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='content', full_name='Message.content', index=2,
      number=3, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _MESSAGE_MESSAGETYPE,
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=73,
  serialized_end=254,
)

_MESSAGE.fields_by_name['message_type'].enum_type = _MESSAGE_MESSAGETYPE
_MESSAGE_MESSAGETYPE.containing_type = _MESSAGE
DESCRIPTOR.message_types_by_name['MessageError'] = _MESSAGEERROR
DESCRIPTOR.message_types_by_name['Message'] = _MESSAGE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

MessageError = _reflection.GeneratedProtocolMessageType('MessageError', (_message.Message,), dict(
  DESCRIPTOR = _MESSAGEERROR,
  __module__ = 'zmq_message_pb2'
  # @@protoc_insertion_point(class_scope:MessageError)
  ))
_sym_db.RegisterMessage(MessageError)

Message = _reflection.GeneratedProtocolMessageType('Message', (_message.Message,), dict(
  DESCRIPTOR = _MESSAGE,
  __module__ = 'zmq_message_pb2'
  # @@protoc_insertion_point(class_scope:Message)
  ))
_sym_db.RegisterMessage(Message)


# @@protoc_insertion_point(module_scope)