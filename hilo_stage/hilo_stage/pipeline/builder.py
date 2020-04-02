from typing import List, Optional

from tfx.orchestration import pipeline as tfx_pipeline
from tfx.components.base.base_component import BaseComponent

from hilo_stage.metadata.builder import MetadataStoreBuilder
from hilo_rpc.proto.pipeline_pb2 import Pipeline
from hilo_stage.source.builder import Builder as SourceBuilder
from hilo_stage.stage.builder import Context, Builder as StageBuilder


class Builder(object):
    def __init__(self, pipeline: Optional[Pipeline] = None):
        self._pipeline = pipeline or Pipeline()

    def build(self) -> tfx_pipeline.Pipeline:
        source_channel = SourceBuilder(self._pipeline.config.source).build()
        stages: List[BaseComponent] = []
        context = Context('pipeline')
        context.put_self('source.channel', source_channel)

        for stage in self._pipeline.config.stages:
            stage_context = context.for_stage(stage.id)
            stages.append(
                StageBuilder(stage.config).build(stage_context))

        metadata_store_config = MetadataStoreBuilder(
            self._pipeline.config.metadata).build()

        return tfx_pipeline.Pipeline(
            pipeline_name=self._pipeline.name,
            pipeline_root=self._pipeline.config.root_dir,
            metadata_connection_config=metadata_store_config,
            enable_cache=self._pipeline.config.params.enable_cache,
            components=stages
        )
