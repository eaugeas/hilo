from typing import Any, Dict, Optional, Text, Union
from tfx.components.base import executor_spec
from tfx.components.example_gen import component
from tfx.proto.example_gen_pb2 import Input, Output
from tfx.types import Channel

from hilo_stage.components.example_gen.json_example_gen.executor import (
    Executor)


class JsonExampleGen(component.FileBasedExampleGen):
    EXECUTOR_SPEC = executor_spec.ExecutorClassSpec(Executor)

    def __init__(
            self,
            input: Channel,
            input_config: Optional[Union[Input, Dict[Text, Any]]] = None,
            output_config: Optional[Union[Output, Dict[Text, Any]]] = None,
            example_artifacts: Optional[Channel] = None,
            instance_name: Optional[Text] = None,
    ):
        super(JsonExampleGen, self).__init__(
            input=input,
            input_config=input_config,
            output_config=output_config,
            example_artifacts=example_artifacts,
            instance_name=instance_name)
