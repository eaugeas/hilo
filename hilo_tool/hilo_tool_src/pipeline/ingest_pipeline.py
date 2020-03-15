from typing import Text
from tfx.orchestration import metadata, pipeline
from tfx.utils.dsl_utils import external_input

from hilo_tool_src.pipeline.pipeline_builder import PipelineBuilder
from hilo_stage.parser_gen.json_parser_gen.component import JsonParserGen


class IngestPipelineBuilder(PipelineBuilder):
    """
    IngestPipelineBuilder creates a new Pipeline that ingests different
    data formats and outputs them in a format and to a store supported
    by the other pipelines.
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
        samples_gen = JsonParserGen(input=samples)

        mcc = metadata.sqlite_metadata_connection_config(
            self._metadata_path)

        return pipeline.Pipeline(
            pipeline_name=self._pipeline_name,
            pipeline_root=self._pipeline_root,
            enable_cache=self._enable_cache,
            metadata_connection_config=mcc,
            components=[samples_gen]
        )
