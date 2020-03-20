# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: proto/pipeline.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='proto/pipeline.proto',
  package='hilo_rpc.proto',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=b'\n\x14proto/pipeline.proto\x12\x0ehilo_rpc.proto\"\x83\x01\n\x13TrainPipelineConfig\x12\x11\n\tdata_root\x18\x01 \x01(\t\x12\x15\n\rmetadata_path\x18\x02 \x01(\t\x12\x15\n\rpipeline_name\x18\x03 \x01(\t\x12\x15\n\rpipeline_root\x18\x04 \x01(\t\x12\x14\n\x0c\x65nable_cache\x18\x05 \x01(\x08\"R\n\x0ePipelineConfig\x12\x34\n\x05train\x18\x01 \x01(\x0b\x32#.hilo_rpc.proto.TrainPipelineConfigH\x00\x42\n\n\x08pipelineb\x06proto3'
)




_TRAINPIPELINECONFIG = _descriptor.Descriptor(
  name='TrainPipelineConfig',
  full_name='hilo_rpc.proto.TrainPipelineConfig',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='data_root', full_name='hilo_rpc.proto.TrainPipelineConfig.data_root', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='metadata_path', full_name='hilo_rpc.proto.TrainPipelineConfig.metadata_path', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='pipeline_name', full_name='hilo_rpc.proto.TrainPipelineConfig.pipeline_name', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='pipeline_root', full_name='hilo_rpc.proto.TrainPipelineConfig.pipeline_root', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='enable_cache', full_name='hilo_rpc.proto.TrainPipelineConfig.enable_cache', index=4,
      number=5, type=8, cpp_type=7, label=1,
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
  serialized_start=41,
  serialized_end=172,
)


_PIPELINECONFIG = _descriptor.Descriptor(
  name='PipelineConfig',
  full_name='hilo_rpc.proto.PipelineConfig',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='train', full_name='hilo_rpc.proto.PipelineConfig.train', index=0,
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
      name='pipeline', full_name='hilo_rpc.proto.PipelineConfig.pipeline',
      index=0, containing_type=None, fields=[]),
  ],
  serialized_start=174,
  serialized_end=256,
)

_PIPELINECONFIG.fields_by_name['train'].message_type = _TRAINPIPELINECONFIG
_PIPELINECONFIG.oneofs_by_name['pipeline'].fields.append(
  _PIPELINECONFIG.fields_by_name['train'])
_PIPELINECONFIG.fields_by_name['train'].containing_oneof = _PIPELINECONFIG.oneofs_by_name['pipeline']
DESCRIPTOR.message_types_by_name['TrainPipelineConfig'] = _TRAINPIPELINECONFIG
DESCRIPTOR.message_types_by_name['PipelineConfig'] = _PIPELINECONFIG
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

TrainPipelineConfig = _reflection.GeneratedProtocolMessageType('TrainPipelineConfig', (_message.Message,), {
  'DESCRIPTOR' : _TRAINPIPELINECONFIG,
  '__module__' : 'proto.pipeline_pb2'
  # @@protoc_insertion_point(class_scope:hilo_rpc.proto.TrainPipelineConfig)
  })
_sym_db.RegisterMessage(TrainPipelineConfig)

PipelineConfig = _reflection.GeneratedProtocolMessageType('PipelineConfig', (_message.Message,), {
  'DESCRIPTOR' : _PIPELINECONFIG,
  '__module__' : 'proto.pipeline_pb2'
  # @@protoc_insertion_point(class_scope:hilo_rpc.proto.PipelineConfig)
  })
_sym_db.RegisterMessage(PipelineConfig)


# @@protoc_insertion_point(module_scope)