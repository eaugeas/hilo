from typing import List

from tfx.orchestration.pipeline import Pipeline as TfxPipeline
from tfx.components.base.base_component import BaseComponent

from hilo_stage.metadata.build import metadata_store_from_config
from hilo_stage.source.source import Source
from hilo_stage.stage.stage import Stage
from hilo_rpc.proto.pipeline_pb2 import Pipeline as PipelineDescriptor


class Pipeline(object):
    def __init__(self, descriptor: PipelineDescriptor):
        self._descriptor = descriptor

    @property
    def descriptor(self) -> PipelineDescriptor:
        return self._descriptor

    def _get_enable_cache(self) -> bool:
        if 'enable_cache' in self._descriptor.config.params:
            if isinstance(self._descriptor.config.params['enable_cache'], bool):
                return self._descriptor.config.params['enable_cache']
        return False

    @staticmethod
    def _get_input_from_context(input, context):
        if not isinstance(input, str):
            raise ValueError(
                'stage input must be specified as'
                ' a string. Found {0}'.format(input))

        values = context
        levels = input.split('.')

        for level in levels:
            print ('check level: ', level)
            if level not in values:
                raise ValueError('invalid input {0} provided for stage'.format(input))
            values = values[level]

        return values

    def build(self) -> TfxPipeline:
        source = Source(self._descriptor.config.source)
        stages: List[BaseComponent] = []
        context = {'$$source': source.channel()}

        for stage_descriptor in self._descriptor.config.stages:
            if stage_descriptor.id in context:
                raise KeyError('stage with id {0} already exists'.format(stage_descriptor.id))

            inputs = {}
            for input in stage_descriptor.config.inputs:
                inputs[input] = Pipeline._get_input_from_context(
                    stage_descriptor.config.inputs[input], context)

            stage_builder = Stage(stage_descriptor)
            stage = stage_builder.build(**inputs)
            context[stage_descriptor.id] = {'outputs': {}}
            for output in stage_descriptor.config.outputs:
                context[stage_descriptor.id]['outputs'][output] = stage.outputs[output]
            stages.append(stage)

        metadata_store = metadata_store_from_config(
            self._descriptor.config.metadata)

        return TfxPipeline(
            pipeline_name=self._descriptor.name,
            pipeline_root=self._descriptor.config.root_dir,
            metadata_connection_config=metadata_store.connection_config(),
            enable_cache=self._get_enable_cache(),
            components=stages
        )