from functools import reduce
from typing import List, Optional, Text, Union

from tfx.orchestration import pipeline as tfx_pipeline

from hilo_stage.metadata.builder import MetadataStoreBuilder
from hilo_stage.metadata.utils import is_metadata_store_defined
from hilo_rpc.proto.pipeline_pb2 import (
    Pipeline as ProtoPipeline, PipelineConfig as ProtoPipelineConfig)
from hilo_rpc.proto.stage_pb2 import Stage as ProtoStage
from hilo_stage.source.builder import Builder as SourceBuilder
from hilo_stage.source.utils import is_source_defined
from hilo_stage.stage.builder import Context, Builder as StageBuilder
from hilo_stage.pipeline.pipeline import Pipeline


class _StepBuilder(object):
    def __init__(self):
        pass

    def build(self, context: Context) -> List[tfx_pipeline.Pipeline]:
        raise NotImplementedError()


class _StagesBuilder(_StepBuilder):
    def __init__(self, stages: Optional[List[ProtoStage]] = None):
        super().__init__()
        self._stages = stages or []

    def append(self, stage: ProtoStage):
        self._stages.append(stage)

    def build(self, context: Context) -> List[tfx_pipeline.Pipeline]:
        import os
        stages = [
            StageBuilder(stage).build(context.for_stage(stage.id))
            for stage in self._stages
        ]

        return [tfx_pipeline.Pipeline(
            pipeline_name=context.id,
            pipeline_root=os.path.join(context.get('root'), context.id),
            metadata_connection_config=context.get('metadata.config'),
            enable_cache=context.get('cache.enable'),
            components=stages  # type: ignore
        )]


class _PipelinePathBuilder(_StepBuilder):
    def __init__(self, path: Text):
        super().__init__()
        self._path = path

    def build(self, context: Context) -> List[tfx_pipeline.Pipeline]:
        return Builder.from_yaml(self._path).build(context).pipelines


class _PipelineBuilder(_StepBuilder):
    def __init__(self, pipeline: Optional[ProtoPipeline] = None):
        super().__init__()
        self._pipeline = pipeline or ProtoPipeline()

    def build(self, context: Context) -> List[tfx_pipeline.Pipeline]:
        return Builder(self._pipeline).build(context).pipelines


class Builder(object):
    def __init__(self, pipeline: Optional[ProtoPipeline] = None):
        self._pipeline = pipeline or ProtoPipeline()

    @staticmethod
    def from_yaml(path: Text) -> 'Builder':
        from hilo_rpc.serialize.yaml import deserialize_from_file
        return Builder(deserialize_from_file(path, ProtoPipeline))

    @staticmethod
    def _create_step_builders(
            steps: Union[
                List[ProtoPipelineConfig.Step], ProtoPipelineConfig.Step],
            step: ProtoPipelineConfig.Step
    ):
        if step.WhichOneof('step') == 'pipeline_path':
            steps.append(_PipelinePathBuilder(step.pipeline_path))
        elif step.WhichOneof('step') == 'pipeline':
            steps.append(_PipelineBuilder(step.pipeline))
        elif step.WhichOneof('step') == 'stage':
            if len(steps) > 0 and isinstance(steps[-1], _StagesBuilder):
                steps[-1].append(step.stage)
            else:
                steps.append(_StagesBuilder([step.stage]))
        elif step.WhichOneof('step') is None:
            raise ValueError('step for pipeline not defined')
        else:
            raise ValueError(
                'Unknown step {0}'.format(step.WhichOneof('step')))

        return steps

    def build(self, context: Optional[Context] = None) -> Pipeline:
        import os

        context = context or Context(self._pipeline.id or 'global')

        if is_source_defined(self._pipeline.config.source):
            source_channel = SourceBuilder(
                self._pipeline.config.source).build()
            context.put_self('source.channel', source_channel)

        if is_metadata_store_defined(self._pipeline.config.metadata):
            metadata_store_config = MetadataStoreBuilder(
                self._pipeline.config.metadata).build()
            context.put_self('metadata.config', metadata_store_config)

        if self._pipeline.config.params.enable_cache is not None:
            context.put_self(
                'cache.enable', self._pipeline.config.params.enable_cache)

        if self._pipeline.config.root_dir:
            context.put_self('root', self._pipeline.config.root_dir)
        else:
            context.put_self('root', context.get('root', default=os.getcwd()))

        step_builders: List[_StepBuilder] = reduce(
            Builder._create_step_builders,
            self._pipeline.config.steps, [])
        pipelines = reduce(
            lambda a, b: a + b,
            [
                step_builders[i].build(
                    context.for_stage('pipeline{0}'.format(i)))
                for i in range(0, len(step_builders))
            ]
        )

        return Pipeline(pipelines)
