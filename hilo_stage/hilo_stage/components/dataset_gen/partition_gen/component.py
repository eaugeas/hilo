from typing import List, Optional, Text

from tfx.components.base import executor_spec
from tfx.components.base.base_component import BaseComponent
from tfx.types import Channel

from hilo_stage.components.utils.splits import (
    splits_or_example_defaults)
from hilo_stage.components.dataset_gen.partition_gen.spec import (
    PartitionGenSpec)
from hilo_stage.components.dataset_gen.partition_gen.executor import (
    Executor)


class PartitionGen(BaseComponent):
    """The PartitionGen component.

    It partitions the input dataset into multiple, independent datasets
    """

    SPEC_CLASS = PartitionGenSpec
    EXECUTOR_SPEC = executor_spec.ExecutorClassSpec(Executor)

    def __init__(
            self,
            examples: Channel,
            datasets: Optional[Channel] = None,
            partitions: Optional[Channel] = None,
            split_names: Optional[List[Text]] = None,
    ):
        super().__init__(spec=PartitionGenSpec(
            examples=examples,
            datasets=datasets,
            partitions=partitions,
            split_names=splits_or_example_defaults(split_names=split_names)
        ))
