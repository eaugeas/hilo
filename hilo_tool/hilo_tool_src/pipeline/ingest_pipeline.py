from hilo_tool_src.pipeline.pipeline_builder import PipelineBuilder


class IngestPipelineBuilder(PipelineBuilder):
    """
    IngestPipelineBuilder creates a new Pipeline that ingests different
    data formats and outputs them in a format and to a store supported
    by the other pipelines.
    """
    def __init__(self):
        super().__init__()

    def build(self):
        pass
