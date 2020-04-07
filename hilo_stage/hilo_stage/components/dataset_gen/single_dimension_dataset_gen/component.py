from typing import List, Optional, Text

from tfx.components.base import executor_spec
from tfx.components.base.base_component import BaseComponent
from tfx.types import Channel

from hilo_stage.components.utils.splits import (
    splits_or_example_defaults)
from hilo_stage.components.dataset_gen.single_dimension_dataset_gen.executor import (  # noqa: E501
    Executor)
from hilo_stage.components.dataset_gen.single_dimension_dataset_gen.spec import (  # noqa: E501
    SingleDimensionGenSpec, Datasets)


class SingleDimensionGen(BaseComponent):
    """The SingleDimensionGen component.

    It generates multiple single dimension partitions
    from the provided data. It ignores all dimensions
    that do not have a relevant amount of records based
    on the proportion of events in which the dimension
    is present
    """
    SPEC_CLASS = SingleDimensionGenSpec
    EXECUTOR_SPEC = executor_spec.ExecutorClassSpec(Executor)

    def __init__(
            self,
            statistics: Optional[Channel] = None,
            split_names: Optional[List[Text]] = None,
            instance_name: Optional[Text] = None
    ):
        """Construct a SingleDimensionGen component."""
        spec = SingleDimensionGenSpec(
            statistics=statistics,
            datasets=Channel(type=Datasets, artifacts=[Datasets()]),
            split_names=splits_or_example_defaults(split_names))
        super().__init__(spec=spec, instance_name=instance_name)
