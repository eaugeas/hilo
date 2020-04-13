# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: hilo_rpc/proto/connector.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='hilo_rpc/proto/connector.proto',
  package='hilo_rpc.proto',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=b'\n\x1ehilo_rpc/proto/connector.proto\x12\x0ehilo_rpc.proto\"\x1f\n\x0fLocalFileConfig\x12\x0c\n\x04path\x18\x01 \x01(\t\"\x1c\n\x0cSqliteConfig\x12\x0c\n\x04path\x18\x01 \x01(\t\"R\n\x0f\x43onnectorConfig\x12\x35\n\nlocal_file\x18\x01 \x01(\x0b\x32\x1f.hilo_rpc.proto.LocalFileConfigH\x00\x42\x08\n\x06\x63onfigb\x06proto3'
)




_LOCALFILECONFIG = _descriptor.Descriptor(
  name='LocalFileConfig',
  full_name='hilo_rpc.proto.LocalFileConfig',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='path', full_name='hilo_rpc.proto.LocalFileConfig.path', index=0,
      number=1, type=9, cpp_type=9, label=1,
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
  serialized_start=50,
  serialized_end=81,
)


_SQLITECONFIG = _descriptor.Descriptor(
  name='SqliteConfig',
  full_name='hilo_rpc.proto.SqliteConfig',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='path', full_name='hilo_rpc.proto.SqliteConfig.path', index=0,
      number=1, type=9, cpp_type=9, label=1,
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
  serialized_start=83,
  serialized_end=111,
)


_CONNECTORCONFIG = _descriptor.Descriptor(
  name='ConnectorConfig',
  full_name='hilo_rpc.proto.ConnectorConfig',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='local_file', full_name='hilo_rpc.proto.ConnectorConfig.local_file', index=0,
      number=1, type=11, cpp_type=10, label=1,
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
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
    _descriptor.OneofDescriptor(
      name='config', full_name='hilo_rpc.proto.ConnectorConfig.config',
      index=0, containing_type=None, fields=[]),
  ],
  serialized_start=113,
  serialized_end=195,
)

_CONNECTORCONFIG.fields_by_name['local_file'].message_type = _LOCALFILECONFIG
_CONNECTORCONFIG.oneofs_by_name['config'].fields.append(
  _CONNECTORCONFIG.fields_by_name['local_file'])
_CONNECTORCONFIG.fields_by_name['local_file'].containing_oneof = _CONNECTORCONFIG.oneofs_by_name['config']
DESCRIPTOR.message_types_by_name['LocalFileConfig'] = _LOCALFILECONFIG
DESCRIPTOR.message_types_by_name['SqliteConfig'] = _SQLITECONFIG
DESCRIPTOR.message_types_by_name['ConnectorConfig'] = _CONNECTORCONFIG
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

LocalFileConfig = _reflection.GeneratedProtocolMessageType('LocalFileConfig', (_message.Message,), {
  'DESCRIPTOR' : _LOCALFILECONFIG,
  '__module__' : 'hilo_rpc.proto.connector_pb2'
  # @@protoc_insertion_point(class_scope:hilo_rpc.proto.LocalFileConfig)
  })
_sym_db.RegisterMessage(LocalFileConfig)

SqliteConfig = _reflection.GeneratedProtocolMessageType('SqliteConfig', (_message.Message,), {
  'DESCRIPTOR' : _SQLITECONFIG,
  '__module__' : 'hilo_rpc.proto.connector_pb2'
  # @@protoc_insertion_point(class_scope:hilo_rpc.proto.SqliteConfig)
  })
_sym_db.RegisterMessage(SqliteConfig)

ConnectorConfig = _reflection.GeneratedProtocolMessageType('ConnectorConfig', (_message.Message,), {
  'DESCRIPTOR' : _CONNECTORCONFIG,
  '__module__' : 'hilo_rpc.proto.connector_pb2'
  # @@protoc_insertion_point(class_scope:hilo_rpc.proto.ConnectorConfig)
  })
_sym_db.RegisterMessage(ConnectorConfig)


# @@protoc_insertion_point(module_scope)
