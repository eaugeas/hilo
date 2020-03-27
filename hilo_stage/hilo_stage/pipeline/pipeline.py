from typing import Any, Dict, List, Text

from tfx.orchestration.pipeline import Pipeline as TfxPipeline
from tfx.components.base.base_component import BaseComponent

from hilo_stage.metadata.build import metadata_store_from_config
from hilo_stage.source.source import Source
from hilo_stage.stage.stage import Stage
from hilo_rpc.proto.pipeline_pb2 import Pipeline as PipelineDescriptor
from hilo_rpc.argparse.argparse import create_object_from_dict


class Pipeline(object):
    def __init__(self, descriptor: PipelineDescriptor):
        self._descriptor = descriptor

    @property
    def descriptor(self) -> PipelineDescriptor:
        return self._descriptor

    def _get_enable_cache(self) -> bool:
        if 'enable_cache' in self._descriptor.config.params:
            if isinstance(self._descriptor.config.params['enable_cache'],
                          bool):
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
            if level not in values:
                raise ValueError(
                    'invalid input {0} provided for stage'.format(input))
            values = values[level]

        return values

    @staticmethod
    def _load_object_param(o: Dict[str, Any]) -> Any:
        if len(o) != 1:
            raise ValueError(
                'Objects to be deserialized to protobuf messages '
                ' must have a single property. Received {0}'.format(o))
        for key in o:
            return create_object_from_dict(o[key], key)

    @staticmethod
    def _load_list_param(l: List[Any]) -> List[Any]:
        results = []
        for el in l:
            results.append(Pipeline._load_value_from_param(el))
        return results

    @staticmethod
    def _load_value_from_param(s: Text) -> Any:
        import json

        if s == 'False':
            return False
        elif s == 'True':
            return True

        try:
            return int(s)
        except ValueError:
            pass

        try:
            return float(s)
        except ValueError:
            pass

        try:
            value = json.loads(s.replace('\'', '"'))
            if isinstance(value, dict):
                return Pipeline._load_object_param(value)
            elif isinstance(value, list):
                return Pipeline._load_list_param(value)
            else:
                raise ValueError('Unknown property type {0}'.format(s))
        except json.decoder.JSONDecodeError:
            pass

        # at this point assume that it is just a string
        return s

    @staticmethod
    def _get_stage_params(params: Dict[str, str]) -> Dict[str, Any]:
        results: Dict[str, Any] = {}
        for key in params:
            results[key] = Pipeline._load_value_from_param(params[key])
        return results

    @staticmethod
    def _merge_dicts(
            d1: Dict[str, Any],
            d2: Dict[str, Any],
            error_on_collision=False,
    ) -> Dict[str, Any]:
        for key in d2:
            if error_on_collision and key in d1:
                raise KeyError(
                    'Key {0} with value {1} already'
                    ' present with value {2}'.format(
                        key, d1[key], d2[key]))
            d1[key] = d2[key]
        return d1

    def build(self) -> TfxPipeline:
        source = Source(self._descriptor.config.source)
        stages: List[BaseComponent] = []
        context = {'$$source': source.channel()}

        for stage_descriptor in self._descriptor.config.stages:
            if stage_descriptor.id in context:
                raise KeyError('stage with id {0} already exists'.format(
                    stage_descriptor.id))

            inputs = {}
            for input in stage_descriptor.config.inputs:
                inputs[input] = Pipeline._get_input_from_context(
                    stage_descriptor.config.inputs[input], context)

            stage_builder = Stage(stage_descriptor)
            params = Pipeline._get_stage_params(stage_descriptor.config.params)
            inputs = Pipeline._merge_dicts(inputs, params)
            print('inputs for stage: ', inputs)
            stage = stage_builder.build(**inputs)
            context[stage_descriptor.id] = {'outputs': {}}
            for output in stage_descriptor.config.outputs:
                context[stage_descriptor.id]['outputs'][output] = (
                    stage.outputs[output])
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
