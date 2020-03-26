# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: hilo_rpc/proto/stage.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='hilo_rpc/proto/stage.proto',
  package='hilo_rpc.proto',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=b'\n\x1ahilo_rpc/proto/stage.proto\x12\x0ehilo_rpc.proto\x1a\x1fgoogle/protobuf/timestamp.proto\"7\n\x03Url\x12\x14\n\nclass_name\x18\x01 \x01(\tH\x00\x12\x13\n\tfull_path\x18\x02 \x01(\tH\x00\x42\x05\n\x03url\"\xea\x02\n\x0bStageConfig\x12 \n\x03url\x18\x01 \x01(\x0b\x32\x13.hilo_rpc.proto.Url\x12\x37\n\x06inputs\x18\x02 \x03(\x0b\x32\'.hilo_rpc.proto.StageConfig.InputsEntry\x12\x39\n\x07outputs\x18\x03 \x03(\x0b\x32(.hilo_rpc.proto.StageConfig.OutputsEntry\x12\x37\n\x06params\x18\x04 \x03(\x0b\x32\'.hilo_rpc.proto.StageConfig.ParamsEntry\x1a-\n\x0bInputsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\x1a.\n\x0cOutputsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\x1a-\n\x0bParamsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"\xc3\x01\n\x05Stage\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x03 \x01(\t\x12.\n\ncreated_at\x18\x04 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12.\n\nupdated_at\x18\x05 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12+\n\x06\x63onfig\x18\x06 \x01(\x0b\x32\x1b.hilo_rpc.proto.StageConfigb\x06proto3'
  ,
  dependencies=[google_dot_protobuf_dot_timestamp__pb2.DESCRIPTOR,])




_URL = _descriptor.Descriptor(
  name='Url',
  full_name='hilo_rpc.proto.Url',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='class_name', full_name='hilo_rpc.proto.Url.class_name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='full_path', full_name='hilo_rpc.proto.Url.full_path', index=1,
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
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
    _descriptor.OneofDescriptor(
      name='url', full_name='hilo_rpc.proto.Url.url',
      index=0, containing_type=None, fields=[]),
  ],
  serialized_start=79,
  serialized_end=134,
)


_STAGECONFIG_INPUTSENTRY = _descriptor.Descriptor(
  name='InputsEntry',
  full_name='hilo_rpc.proto.StageConfig.InputsEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='hilo_rpc.proto.StageConfig.InputsEntry.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='value', full_name='hilo_rpc.proto.StageConfig.InputsEntry.value', index=1,
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
  serialized_start=359,
  serialized_end=404,
)

_STAGECONFIG_OUTPUTSENTRY = _descriptor.Descriptor(
  name='OutputsEntry',
  full_name='hilo_rpc.proto.StageConfig.OutputsEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='hilo_rpc.proto.StageConfig.OutputsEntry.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='value', full_name='hilo_rpc.proto.StageConfig.OutputsEntry.value', index=1,
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
  serialized_start=406,
  serialized_end=452,
)

_STAGECONFIG_PARAMSENTRY = _descriptor.Descriptor(
  name='ParamsEntry',
  full_name='hilo_rpc.proto.StageConfig.ParamsEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='hilo_rpc.proto.StageConfig.ParamsEntry.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='value', full_name='hilo_rpc.proto.StageConfig.ParamsEntry.value', index=1,
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
  serialized_start=454,
  serialized_end=499,
)

_STAGECONFIG = _descriptor.Descriptor(
  name='StageConfig',
  full_name='hilo_rpc.proto.StageConfig',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='url', full_name='hilo_rpc.proto.StageConfig.url', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='inputs', full_name='hilo_rpc.proto.StageConfig.inputs', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='outputs', full_name='hilo_rpc.proto.StageConfig.outputs', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='params', full_name='hilo_rpc.proto.StageConfig.params', index=3,
      number=4, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_STAGECONFIG_INPUTSENTRY, _STAGECONFIG_OUTPUTSENTRY, _STAGECONFIG_PARAMSENTRY, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=137,
  serialized_end=499,
)


_STAGE = _descriptor.Descriptor(
  name='Stage',
  full_name='hilo_rpc.proto.Stage',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='hilo_rpc.proto.Stage.id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='name', full_name='hilo_rpc.proto.Stage.name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='description', full_name='hilo_rpc.proto.Stage.description', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='created_at', full_name='hilo_rpc.proto.Stage.created_at', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='updated_at', full_name='hilo_rpc.proto.Stage.updated_at', index=4,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='config', full_name='hilo_rpc.proto.Stage.config', index=5,
      number=6, type=11, cpp_type=10, label=1,
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
  ],
  serialized_start=502,
  serialized_end=697,
)

_URL.oneofs_by_name['url'].fields.append(
  _URL.fields_by_name['class_name'])
_URL.fields_by_name['class_name'].containing_oneof = _URL.oneofs_by_name['url']
_URL.oneofs_by_name['url'].fields.append(
  _URL.fields_by_name['full_path'])
_URL.fields_by_name['full_path'].containing_oneof = _URL.oneofs_by_name['url']
_STAGECONFIG_INPUTSENTRY.containing_type = _STAGECONFIG
_STAGECONFIG_OUTPUTSENTRY.containing_type = _STAGECONFIG
_STAGECONFIG_PARAMSENTRY.containing_type = _STAGECONFIG
_STAGECONFIG.fields_by_name['url'].message_type = _URL
_STAGECONFIG.fields_by_name['inputs'].message_type = _STAGECONFIG_INPUTSENTRY
_STAGECONFIG.fields_by_name['outputs'].message_type = _STAGECONFIG_OUTPUTSENTRY
_STAGECONFIG.fields_by_name['params'].message_type = _STAGECONFIG_PARAMSENTRY
_STAGE.fields_by_name['created_at'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_STAGE.fields_by_name['updated_at'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_STAGE.fields_by_name['config'].message_type = _STAGECONFIG
DESCRIPTOR.message_types_by_name['Url'] = _URL
DESCRIPTOR.message_types_by_name['StageConfig'] = _STAGECONFIG
DESCRIPTOR.message_types_by_name['Stage'] = _STAGE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Url = _reflection.GeneratedProtocolMessageType('Url', (_message.Message,), {
  'DESCRIPTOR' : _URL,
  '__module__' : 'hilo_rpc.proto.stage_pb2'
  # @@protoc_insertion_point(class_scope:hilo_rpc.proto.Url)
  })
_sym_db.RegisterMessage(Url)

StageConfig = _reflection.GeneratedProtocolMessageType('StageConfig', (_message.Message,), {

  'InputsEntry' : _reflection.GeneratedProtocolMessageType('InputsEntry', (_message.Message,), {
    'DESCRIPTOR' : _STAGECONFIG_INPUTSENTRY,
    '__module__' : 'hilo_rpc.proto.stage_pb2'
    # @@protoc_insertion_point(class_scope:hilo_rpc.proto.StageConfig.InputsEntry)
    })
  ,

  'OutputsEntry' : _reflection.GeneratedProtocolMessageType('OutputsEntry', (_message.Message,), {
    'DESCRIPTOR' : _STAGECONFIG_OUTPUTSENTRY,
    '__module__' : 'hilo_rpc.proto.stage_pb2'
    # @@protoc_insertion_point(class_scope:hilo_rpc.proto.StageConfig.OutputsEntry)
    })
  ,

  'ParamsEntry' : _reflection.GeneratedProtocolMessageType('ParamsEntry', (_message.Message,), {
    'DESCRIPTOR' : _STAGECONFIG_PARAMSENTRY,
    '__module__' : 'hilo_rpc.proto.stage_pb2'
    # @@protoc_insertion_point(class_scope:hilo_rpc.proto.StageConfig.ParamsEntry)
    })
  ,
  'DESCRIPTOR' : _STAGECONFIG,
  '__module__' : 'hilo_rpc.proto.stage_pb2'
  # @@protoc_insertion_point(class_scope:hilo_rpc.proto.StageConfig)
  })
_sym_db.RegisterMessage(StageConfig)
_sym_db.RegisterMessage(StageConfig.InputsEntry)
_sym_db.RegisterMessage(StageConfig.OutputsEntry)
_sym_db.RegisterMessage(StageConfig.ParamsEntry)

Stage = _reflection.GeneratedProtocolMessageType('Stage', (_message.Message,), {
  'DESCRIPTOR' : _STAGE,
  '__module__' : 'hilo_rpc.proto.stage_pb2'
  # @@protoc_insertion_point(class_scope:hilo_rpc.proto.Stage)
  })
_sym_db.RegisterMessage(Stage)


_STAGECONFIG_INPUTSENTRY._options = None
_STAGECONFIG_OUTPUTSENTRY._options = None
_STAGECONFIG_PARAMSENTRY._options = None
# @@protoc_insertion_point(module_scope)