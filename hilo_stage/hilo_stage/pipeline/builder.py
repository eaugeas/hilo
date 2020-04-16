from functools import reduce
from typing import List, Optional, Text, Union

from tfx.components.base.base_node import BaseNode
from tfx.orchestration.pipeline import Pipeline as TfxPipeline

from hilo_stage.metadata.builder import MetadataStoreBuilder
from hilo_stage.metadata.utils import is_metadata_store_defined
from hilo_rpc.proto.pipeline_pb2 import (Pipeline as ProtoPipeline,
                                         PipelineConfig as ProtoPipelineConfig)
from hilo_rpc.proto.stage_pb2 import Stage as ProtoStage
from hilo_stage.source.builder import Builder as SourceBuilder
from hilo_stage.stage.builder import Context, Builder as StageBuilder


class _StepBuilder(object):
    def __init__(self):
        pass

    def build(self, parent: Context) -> List[BaseNode]:
        raise NotImplementedError()


def _add_inputs_to_context(inputs: ProtoPipelineConfig.Input,
                           context: Context):
    for input in inputs:
        if input.WhichOneof('input') == 'source':
            source_channel = SourceBuilder(input.source).build()
            context.put('inputs/{0}'.format(input.source.id), source_channel)
        elif input.WhichOneof('input') == 'channel':
            context.put('inputs/{0}'.format(input.channel.id),
                        context.get(input.channel.url))

        elif input.WhichOneof('input') is None:
            raise ValueError('No input set for pipeline {0}'.format(
                context.abs_current))
        else:
            raise ValueError('Unknown input type {0} for pipeline {1}'.format(
                input.WhichOneof('input'), context.abs_current))


def _add_outputs_to_context(outputs: ProtoPipelineConfig.Output,
                            context: Context):
    for output in outputs:
        if output.WhichOneof('output') == 'sink':
            context.put('outputs/{0}'.format(output.sink.id),
                        context.get(output.sink))

        elif output.WhichOneof('output') == 'channel':
            context.put('outputs/{0}'.format(output.channel.id),
                        context.get(output.channel.url))
        elif output.WhichOneof('output') is None:
            raise ValueError('No input set for pipeline {0}'.format(
                context.abs_current_url_friendly))
        else:
            raise ValueError('Unknown input type {0} for pipeline {1}'.format(
                output.WhichOneof('output'), context.abs_current_url_friendly))


def _create_step_builders(steps: Union[List[ProtoPipelineConfig.Step],
                                       ProtoPipelineConfig.Step],
                          step: ProtoPipelineConfig.Step):
    if step.WhichOneof('step') == 'sequence_path':
        steps.append(_SequencePathBuilder(step.sequence_path))
    elif step.WhichOneof('step') == 'sequence':
        steps.append(_SequenceBuilder(step.sequence))
    elif step.WhichOneof('step') == 'stage':
        if len(steps) > 0 and isinstance(steps[-1], _StagesBuilder):
            steps[-1].append(step.stage)
        else:
            steps.append(_StagesBuilder([step.stage]))
    elif step.WhichOneof('step') is None:
        raise ValueError('step for pipeline not defined')
    else:
        raise ValueError('Unknown step {0}'.format(step.WhichOneof('step')))
    return steps


class _StagesBuilder(_StepBuilder):
    def __init__(self, stages: Optional[List[ProtoStage]] = None):
        super().__init__()
        self._stages = stages or []

    def append(self, stage: ProtoStage):
        self._stages.append(stage)

    def build(self, parent: Context) -> List[BaseNode]:
        return [
            StageBuilder(stage).build(
                parent.child('stages/{0}'.format(stage.id)))
            for stage in self._stages
        ]


class _SequenceBuilder(_StepBuilder):
    def __init__(
        self,
        sequence: Optional[ProtoPipelineConfig.Sequence] = None,
    ):
        super().__init__()
        self._sequence = sequence or ProtoPipelineConfig.Sequence()

    def build(self, parent: Context) -> List[BaseNode]:
        context = parent.child('sequence/{0}'.format(self._sequence.id))

        _add_inputs_to_context(self._sequence.config.inputs, context)
        step_builders: List[_StepBuilder] = reduce(_create_step_builders,
                                                   self._sequence.config.steps,
                                                   [])
        pipelines: List[List[BaseNode]] = reduce(
            lambda a, b: a + [b],  # type: ignore
            [
                step_builders[i].build(context)
                for i in range(0, len(step_builders))
            ],
            [])

        components = reduce(lambda a, b: a + b, pipelines)
        _add_outputs_to_context(self._sequence.config.outputs, context)
        return components


class _SequencePathBuilder(_SequenceBuilder):
    def __init__(self, path: Text):
        from hilo_rpc.serialize.yaml import deserialize_from_file
        sequence = deserialize_from_file(path, ProtoPipelineConfig.Sequence)

        super().__init__(sequence)


class Builder(object):
    def __init__(self, pipeline: Optional[ProtoPipeline] = None):
        self._pipeline = pipeline or ProtoPipeline()

    @staticmethod
    def from_yaml(path: Text) -> 'Builder':
        from hilo_rpc.serialize.yaml import deserialize_from_file
        deserialized = deserialize_from_file(path, ProtoPipeline)
        return Builder(deserialized)

    def build(self, context: Optional[Context] = None) -> TfxPipeline:
        import os

        context = context or Context('/pipelines/{0}'.format(self._pipeline.id
                                                             or 'global'))

        _add_inputs_to_context(self._pipeline.config.inputs, context)
        if is_metadata_store_defined(self._pipeline.config.metadata):
            metadata_store_config = MetadataStoreBuilder(
                self._pipeline.config.metadata).build()
            context.put('config/metadata', metadata_store_config)

        if self._pipeline.config.params.enable_cache is not None:
            context.put('config/cache/enable',
                        self._pipeline.config.params.enable_cache)

        if self._pipeline.config.root_dir:
            context.put('config/root', self._pipeline.config.root_dir)
        else:
            context.put('config/root',
                        context.get('config/root', default=os.getcwd()))

        step_builders: List[_StepBuilder] = reduce(_create_step_builders,
                                                   self._pipeline.config.steps,
                                                   [])
        pipelines: List[List[BaseNode]] = reduce(
            lambda a, b: a + [b],  # type: ignore
            [
                step_builders[i].build(context)
                for i in range(0, len(step_builders))
            ],
            [])

        components = reduce(lambda a, b: a + b, pipelines)
        _add_outputs_to_context(self._pipeline.config.outputs, context)

        pipeline_root = os.path.join(context.get('config/root'),
                                     context.abs_current_url_friendly)

        return TfxPipeline(
            pipeline_name=context.abs_current_url_friendly,
            pipeline_root=pipeline_root,
            metadata_connection_config=context.get('config/metadata'),
            enable_cache=context.get('config/cache/enable'),
            components=components  # type: ignore
        )
