from tfx.orchestration import tfx_runner

from hilo_stage.pipeline.pipeline import Pipeline


class Runner(object):
    def __init__(self, runner: tfx_runner.TfxRunner):
        self._runner = runner

    def run(self, pipeline: Pipeline):
        for p in pipeline.pipelines:
            self._runner.run(p)
