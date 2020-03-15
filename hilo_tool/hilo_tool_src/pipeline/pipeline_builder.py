from tfx.orchestration import pipeline


class PipelineBuilder(object):
    def __init__(self):
        pass

    def build(self) -> pipeline.Pipeline:
        raise NotImplementedError()
