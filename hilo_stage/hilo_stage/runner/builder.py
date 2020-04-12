from typing import Any, Dict, List, Optional, Type

from tfx.orchestration import tfx_runner

from hilo_rpc.proto.runner_pb2 import BeamDagRunnerConfig, RunnerConfig
from hilo_stage.runner.runner import Runner


class RunnerBuilder(object):
    def __init__(self, config: Optional[Any] = None):
        pass

    def build(self) -> tfx_runner.TfxRunner:
        raise NotImplementedError()


class BeamDagRunnerBuilder(RunnerBuilder):
    def __init__(self, config: Optional[BeamDagRunnerConfig] = None):
        super().__init__(config)
        self._config = config or BeamDagRunnerConfig()

    def build(self) -> tfx_runner.TfxRunner:
        from tfx.orchestration.beam.beam_dag_runner import BeamDagRunner

        orchestrator_args: Optional[List] = None
        if len(self._config.orchestrator_args) > 0:
            orchestrator_args = [arg for arg in self._config.orchestrator_args]

        return BeamDagRunner(
            beam_orchestrator_args=orchestrator_args)


class Builder(object):
    def __init__(self, config: Optional[RunnerConfig] = None):
        self._config = config or RunnerConfig(beam=BeamDagRunnerConfig())

        self._runner_builders: Dict[str, Type[RunnerBuilder]] = {
            'beam': BeamDagRunnerBuilder,
        }

    def build(self) -> Runner:
        runner_name = self._config.WhichOneof('config')
        if runner_name in self._runner_builders:
            runner_constructor = self._runner_builders[runner_name]
            builder = runner_constructor(getattr(self._config, runner_name))
            return Runner(builder.build())
        else:
            raise ValueError('Unknown runner name {0}'.format(runner_name))
