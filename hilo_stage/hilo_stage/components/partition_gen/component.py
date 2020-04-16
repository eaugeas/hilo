from typing import Optional, Text

from tfx import types
from tfx.components.base import base_component, executor_spec

from hilo_stage.components.partition_gen.spec import PartitionSpec
from hilo_stage.components.partition_gen.executor import Executor
from hilo_stage.components.partition_gen.artifact import Partitions


class PartitionGen(base_component.BaseComponent):
    """The PartitionGen component.

    It breaks down data into independent partitions that can
    be manipulated independently.
    """
    SPEC_CLASS = PartitionSpec
    EXECUTOR_SPEC = executor_spec.ExecutorClassSpec(Executor)

    def __init__(self,
                 statistics: types.Channel,
                 schema: types.Channel,
                 examples: types.Channel,
                 partitions: Optional[types.Channel] = None,
                 instance_name: Optional[Text] = None):
        if not partitions:
            partitions_artifact = Partitions()
            partitions = types.Channel(type=Partitions,
                                       artifacts=[partitions_artifact])

        spec = PartitionSpec(statistics=statistics,
                             schema=schema,
                             examples=examples,
                             partitions=partitions)

        super().__init__(spec=spec, instance_name=instance_name)
