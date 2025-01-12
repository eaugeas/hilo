# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: hilo_rpc/proto/tests.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='hilo_rpc/proto/tests.proto',
  package='hilo_rpc.proto',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=b'\n\x1ahilo_rpc/proto/tests.proto\x12\x0ehilo_rpc.proto\"\xe8\x04\n\x0bTestMessage\x12.\n\x04\x65num\x18\x01 \x01(\x0b\x32 .hilo_rpc.proto.TestMessage.Enum\x12\x32\n\x06params\x18\x02 \x01(\x0b\x32\".hilo_rpc.proto.TestMessage.Params\x12\x39\n\x07mapping\x18\x03 \x03(\x0b\x32(.hilo_rpc.proto.TestMessage.MappingEntry\x12\x17\n\x0fstring_repeated\x18\x04 \x03(\t\x12;\n\x0fparams_repeated\x18\x05 \x03(\x0b\x32\".hilo_rpc.proto.TestMessage.Params\x12>\n\nparams_map\x18\x06 \x03(\x0b\x32*.hilo_rpc.proto.TestMessage.ParamsMapEntry\x1aG\n\x06Params\x12\x12\n\nbool_param\x18\x01 \x01(\x08\x12\x13\n\x0bint32_param\x18\x02 \x01(\x05\x12\x14\n\x0cstring_param\x18\x03 \x01(\t\x1aU\n\x04\x45num\x12\x13\n\tbool_enum\x18\x01 \x01(\x08H\x00\x12\x14\n\nint32_enum\x18\x02 \x01(\x05H\x00\x12\x15\n\x0bstring_enum\x18\x03 \x01(\tH\x00\x42\x0b\n\ttype_enum\x1a.\n\x0cMappingEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\x1aT\n\x0eParamsMapEntry\x12\x0b\n\x03key\x18\x01 \x01(\x05\x12\x31\n\x05value\x18\x02 \x01(\x0b\x32\".hilo_rpc.proto.TestMessage.Params:\x02\x38\x01\x62\x06proto3'
)




_TESTMESSAGE_PARAMS = _descriptor.Descriptor(
  name='Params',
  full_name='hilo_rpc.proto.TestMessage.Params',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='bool_param', full_name='hilo_rpc.proto.TestMessage.Params.bool_param', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='int32_param', full_name='hilo_rpc.proto.TestMessage.Params.int32_param', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='string_param', full_name='hilo_rpc.proto.TestMessage.Params.string_param', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=371,
  serialized_end=442,
)

_TESTMESSAGE_ENUM = _descriptor.Descriptor(
  name='Enum',
  full_name='hilo_rpc.proto.TestMessage.Enum',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='bool_enum', full_name='hilo_rpc.proto.TestMessage.Enum.bool_enum', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='int32_enum', full_name='hilo_rpc.proto.TestMessage.Enum.int32_enum', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='string_enum', full_name='hilo_rpc.proto.TestMessage.Enum.string_enum', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
    _descriptor.OneofDescriptor(
      name='type_enum', full_name='hilo_rpc.proto.TestMessage.Enum.type_enum',
      index=0, containing_type=None, fields=[]),
  ],
  serialized_start=444,
  serialized_end=529,
)

_TESTMESSAGE_MAPPINGENTRY = _descriptor.Descriptor(
  name='MappingEntry',
  full_name='hilo_rpc.proto.TestMessage.MappingEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='hilo_rpc.proto.TestMessage.MappingEntry.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='value', full_name='hilo_rpc.proto.TestMessage.MappingEntry.value', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=b'8\001',
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=531,
  serialized_end=577,
)

_TESTMESSAGE_PARAMSMAPENTRY = _descriptor.Descriptor(
  name='ParamsMapEntry',
  full_name='hilo_rpc.proto.TestMessage.ParamsMapEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='hilo_rpc.proto.TestMessage.ParamsMapEntry.key', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='value', full_name='hilo_rpc.proto.TestMessage.ParamsMapEntry.value', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=b'8\001',
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=579,
  serialized_end=663,
)

_TESTMESSAGE = _descriptor.Descriptor(
  name='TestMessage',
  full_name='hilo_rpc.proto.TestMessage',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='enum', full_name='hilo_rpc.proto.TestMessage.enum', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='params', full_name='hilo_rpc.proto.TestMessage.params', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='mapping', full_name='hilo_rpc.proto.TestMessage.mapping', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='string_repeated', full_name='hilo_rpc.proto.TestMessage.string_repeated', index=3,
      number=4, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='params_repeated', full_name='hilo_rpc.proto.TestMessage.params_repeated', index=4,
      number=5, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='params_map', full_name='hilo_rpc.proto.TestMessage.params_map', index=5,
      number=6, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_TESTMESSAGE_PARAMS, _TESTMESSAGE_ENUM, _TESTMESSAGE_MAPPINGENTRY, _TESTMESSAGE_PARAMSMAPENTRY, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=47,
  serialized_end=663,
)

_TESTMESSAGE_PARAMS.containing_type = _TESTMESSAGE
_TESTMESSAGE_ENUM.containing_type = _TESTMESSAGE
_TESTMESSAGE_ENUM.oneofs_by_name['type_enum'].fields.append(
  _TESTMESSAGE_ENUM.fields_by_name['bool_enum'])
_TESTMESSAGE_ENUM.fields_by_name['bool_enum'].containing_oneof = _TESTMESSAGE_ENUM.oneofs_by_name['type_enum']
_TESTMESSAGE_ENUM.oneofs_by_name['type_enum'].fields.append(
  _TESTMESSAGE_ENUM.fields_by_name['int32_enum'])
_TESTMESSAGE_ENUM.fields_by_name['int32_enum'].containing_oneof = _TESTMESSAGE_ENUM.oneofs_by_name['type_enum']
_TESTMESSAGE_ENUM.oneofs_by_name['type_enum'].fields.append(
  _TESTMESSAGE_ENUM.fields_by_name['string_enum'])
_TESTMESSAGE_ENUM.fields_by_name['string_enum'].containing_oneof = _TESTMESSAGE_ENUM.oneofs_by_name['type_enum']
_TESTMESSAGE_MAPPINGENTRY.containing_type = _TESTMESSAGE
_TESTMESSAGE_PARAMSMAPENTRY.fields_by_name['value'].message_type = _TESTMESSAGE_PARAMS
_TESTMESSAGE_PARAMSMAPENTRY.containing_type = _TESTMESSAGE
_TESTMESSAGE.fields_by_name['enum'].message_type = _TESTMESSAGE_ENUM
_TESTMESSAGE.fields_by_name['params'].message_type = _TESTMESSAGE_PARAMS
_TESTMESSAGE.fields_by_name['mapping'].message_type = _TESTMESSAGE_MAPPINGENTRY
_TESTMESSAGE.fields_by_name['params_repeated'].message_type = _TESTMESSAGE_PARAMS
_TESTMESSAGE.fields_by_name['params_map'].message_type = _TESTMESSAGE_PARAMSMAPENTRY
DESCRIPTOR.message_types_by_name['TestMessage'] = _TESTMESSAGE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

TestMessage = _reflection.GeneratedProtocolMessageType('TestMessage', (_message.Message,), {

  'Params' : _reflection.GeneratedProtocolMessageType('Params', (_message.Message,), {
    'DESCRIPTOR' : _TESTMESSAGE_PARAMS,
    '__module__' : 'hilo_rpc.proto.tests_pb2'
    # @@protoc_insertion_point(class_scope:hilo_rpc.proto.TestMessage.Params)
    })
  ,

  'Enum' : _reflection.GeneratedProtocolMessageType('Enum', (_message.Message,), {
    'DESCRIPTOR' : _TESTMESSAGE_ENUM,
    '__module__' : 'hilo_rpc.proto.tests_pb2'
    # @@protoc_insertion_point(class_scope:hilo_rpc.proto.TestMessage.Enum)
    })
  ,

  'MappingEntry' : _reflection.GeneratedProtocolMessageType('MappingEntry', (_message.Message,), {
    'DESCRIPTOR' : _TESTMESSAGE_MAPPINGENTRY,
    '__module__' : 'hilo_rpc.proto.tests_pb2'
    # @@protoc_insertion_point(class_scope:hilo_rpc.proto.TestMessage.MappingEntry)
    })
  ,

  'ParamsMapEntry' : _reflection.GeneratedProtocolMessageType('ParamsMapEntry', (_message.Message,), {
    'DESCRIPTOR' : _TESTMESSAGE_PARAMSMAPENTRY,
    '__module__' : 'hilo_rpc.proto.tests_pb2'
    # @@protoc_insertion_point(class_scope:hilo_rpc.proto.TestMessage.ParamsMapEntry)
    })
  ,
  'DESCRIPTOR' : _TESTMESSAGE,
  '__module__' : 'hilo_rpc.proto.tests_pb2'
  # @@protoc_insertion_point(class_scope:hilo_rpc.proto.TestMessage)
  })
_sym_db.RegisterMessage(TestMessage)
_sym_db.RegisterMessage(TestMessage.Params)
_sym_db.RegisterMessage(TestMessage.Enum)
_sym_db.RegisterMessage(TestMessage.MappingEntry)
_sym_db.RegisterMessage(TestMessage.ParamsMapEntry)


_TESTMESSAGE_MAPPINGENTRY._options = None
_TESTMESSAGE_PARAMSMAPENTRY._options = None
# @@protoc_insertion_point(module_scope)
