from typing import List

from tfx.orchestration.pipeline import Pipeline as TfxPipeline


class Pipeline(object):
    def __init__(self, pipelines: List[TfxPipeline]):
        self._pipelines = pipelines

    @property
    def pipelines(self) -> List[TfxPipeline]:
        return self._pipelines
