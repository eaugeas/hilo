# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: hilo_rpc/proto/pipeline.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from hilo_rpc.proto import metadata_pb2 as hilo__rpc_dot_proto_dot_metadata__pb2
from hilo_rpc.proto import sink_pb2 as hilo__rpc_dot_proto_dot_sink__pb2
from hilo_rpc.proto import source_pb2 as hilo__rpc_dot_proto_dot_source__pb2
from hilo_rpc.proto import stage_pb2 as hilo__rpc_dot_proto_dot_stage__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='hilo_rpc/proto/pipeline.proto',
  package='hilo_rpc.proto',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=b'\n\x1dhilo_rpc/proto/pipeline.proto\x12\x0ehilo_rpc.proto\x1a\x1dhilo_rpc/proto/metadata.proto\x1a\x19hilo_rpc/proto/sink.proto\x1a\x1bhilo_rpc/proto/source.proto\x1a\x1ahilo_rpc/proto/stage.proto\"\xa3\x02\n\x0ePipelineConfig\x12\x10\n\x08root_dir\x18\x01 \x01(\t\x12\x35\n\x06params\x18\x02 \x01(\x0b\x32%.hilo_rpc.proto.PipelineConfig.Params\x12&\n\x06source\x18\x03 \x01(\x0b\x32\x16.hilo_rpc.proto.Source\x12\"\n\x04sink\x18\x04 \x01(\x0b\x32\x14.hilo_rpc.proto.Sink\x12\x35\n\x08metadata\x18\x05 \x01(\x0b\x32#.hilo_rpc.proto.MetadataStoreConfig\x12%\n\x06stages\x18\x06 \x03(\x0b\x32\x15.hilo_rpc.proto.Stage\x1a\x1e\n\x06Params\x12\x14\n\x0c\x65nable_cache\x18\x01 \x01(\x08\"T\n\x08Pipeline\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12.\n\x06\x63onfig\x18\x03 \x01(\x0b\x32\x1e.hilo_rpc.proto.PipelineConfigb\x06proto3'
  ,
  dependencies=[hilo__rpc_dot_proto_dot_metadata__pb2.DESCRIPTOR,hilo__rpc_dot_proto_dot_sink__pb2.DESCRIPTOR,hilo__rpc_dot_proto_dot_source__pb2.DESCRIPTOR,hilo__rpc_dot_proto_dot_stage__pb2.DESCRIPTOR,])




_PIPELINECONFIG_PARAMS = _descriptor.Descriptor(
  name='Params',
  full_name='hilo_rpc.proto.PipelineConfig.Params',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='enable_cache', full_name='hilo_rpc.proto.PipelineConfig.Params.enable_cache', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
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
  serialized_start=426,
  serialized_end=456,
)

_PIPELINECONFIG = _descriptor.Descriptor(
  name='PipelineConfig',
  full_name='hilo_rpc.proto.PipelineConfig',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='root_dir', full_name='hilo_rpc.proto.PipelineConfig.root_dir', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='params', full_name='hilo_rpc.proto.PipelineConfig.params', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='source', full_name='hilo_rpc.proto.PipelineConfig.source', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='sink', full_name='hilo_rpc.proto.PipelineConfig.sink', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='metadata', full_name='hilo_rpc.proto.PipelineConfig.metadata', index=4,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='stages', full_name='hilo_rpc.proto.PipelineConfig.stages', index=5,
      number=6, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_PIPELINECONFIG_PARAMS, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=165,
  serialized_end=456,
)


_PIPELINE = _descriptor.Descriptor(
  name='Pipeline',
  full_name='hilo_rpc.proto.Pipeline',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='hilo_rpc.proto.Pipeline.id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='name', full_name='hilo_rpc.proto.Pipeline.name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='config', full_name='hilo_rpc.proto.Pipeline.config', index=2,
      number=3, type=11, cpp_type=10, label=1,
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
  serialized_start=458,
  serialized_end=542,
)

_PIPELINECONFIG_PARAMS.containing_type = _PIPELINECONFIG
_PIPELINECONFIG.fields_by_name['params'].message_type = _PIPELINECONFIG_PARAMS
_PIPELINECONFIG.fields_by_name['source'].message_type = hilo__rpc_dot_proto_dot_source__pb2._SOURCE
_PIPELINECONFIG.fields_by_name['sink'].message_type = hilo__rpc_dot_proto_dot_sink__pb2._SINK
_PIPELINECONFIG.fields_by_name['metadata'].message_type = hilo__rpc_dot_proto_dot_metadata__pb2._METADATASTORECONFIG
_PIPELINECONFIG.fields_by_name['stages'].message_type = hilo__rpc_dot_proto_dot_stage__pb2._STAGE
_PIPELINE.fields_by_name['config'].message_type = _PIPELINECONFIG
DESCRIPTOR.message_types_by_name['PipelineConfig'] = _PIPELINECONFIG
DESCRIPTOR.message_types_by_name['Pipeline'] = _PIPELINE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

PipelineConfig = _reflection.GeneratedProtocolMessageType('PipelineConfig', (_message.Message,), {

  'Params' : _reflection.GeneratedProtocolMessageType('Params', (_message.Message,), {
    'DESCRIPTOR' : _PIPELINECONFIG_PARAMS,
    '__module__' : 'hilo_rpc.proto.pipeline_pb2'
    # @@protoc_insertion_point(class_scope:hilo_rpc.proto.PipelineConfig.Params)
    })
  ,
  'DESCRIPTOR' : _PIPELINECONFIG,
  '__module__' : 'hilo_rpc.proto.pipeline_pb2'
  # @@protoc_insertion_point(class_scope:hilo_rpc.proto.PipelineConfig)
  })
_sym_db.RegisterMessage(PipelineConfig)
_sym_db.RegisterMessage(PipelineConfig.Params)

Pipeline = _reflection.GeneratedProtocolMessageType('Pipeline', (_message.Message,), {
  'DESCRIPTOR' : _PIPELINE,
  '__module__' : 'hilo_rpc.proto.pipeline_pb2'
  # @@protoc_insertion_point(class_scope:hilo_rpc.proto.Pipeline)
  })
_sym_db.RegisterMessage(Pipeline)


# @@protoc_insertion_point(module_scope)
