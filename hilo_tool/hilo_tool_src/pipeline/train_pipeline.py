from typing import Text
from tfx.components import SchemaGen, StatisticsGen
from tfx.orchestration import metadata, pipeline
from tfx.utils.dsl_utils import external_input

from hilo_tool_src.pipeline.pipeline_builder import PipelineBuilder
from hilo_stage.example_gen.json_example_gen.component import JsonExampleGen
from hilo_stage.dimension_gen.single_dimension_gen.component import (
    SingleDimensionGen)


class TrainPipelineBuilder(PipelineBuilder):
    """
    TrainPipelineBuilder creates a new Pipeline that trains models
    based on the input data.
    """
    def __init__(
            self,
            data_root: Text,
            metadata_path: Text,
            pipeline_name: Text,
            pipeline_root: Text,
            enable_cache: bool = False,
    ):
        super().__init__()
        self._pipeline_name = pipeline_name
        self._pipeline_root = pipeline_root
        self._data_root: Text = data_root
        self._metadata_path: Text = metadata_path
        self._enable_cache = enable_cache

    def build(self) -> pipeline.Pipeline:
        samples = external_input(self._data_root)
        samples_gen = JsonExampleGen(input=samples)
        statistics_gen = StatisticsGen(
            examples=samples_gen.outputs['examples'])
        schema_gen = SchemaGen(
            statistics=statistics_gen.outputs['statistics'],
            infer_feature_shape=False)
        dimension_gen = SingleDimensionGen(
            examples=samples_gen.outputs['examples'],
            statistics=statistics_gen.outputs['statistics'],
            schema=schema_gen.outputs['schema'])

        mcc = metadata.sqlite_metadata_connection_config(
            self._metadata_path)

        components = [
            samples_gen,
            statistics_gen,
            schema_gen,
            dimension_gen]

        return pipeline.Pipeline(
            pipeline_name=self._pipeline_name,
            pipeline_root=self._pipeline_root,
            enable_cache=self._enable_cache,
            metadata_connection_config=mcc,
            components=components
        )
