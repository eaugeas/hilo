from typing import List, Optional, Text

from tfx.components.base import executor_spec
from tfx.components.base.base_component import BaseComponent
from tfx.types import Channel
from tfx.types import artifact

from hilo_stage.components.dimension_gen.single_dimension_gen.executor import (
    Executor)
from hilo_stage.components.dimension_gen.single_dimension_gen.spec import (
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
            examples: Channel,
            schema: Optional[Channel] = None,
            statistics: Optional[Channel] = None,
            split_names: Optional[List[Text]] = None,
    ):
        """Construct a SingleDimensionGen component."""
        splits: List[Text] = []
        if split_names:
            splits = split_names
        else:
            for el in artifact.DEFAULT_EXAMPLE_SPLITS:
                splits.append(el)

        datasets = Channel(
            type=Datasets,
            artifacts=[Datasets()])

        spec = SingleDimensionGenSpec(
            examples=examples,
            schema=schema,
            statistics=statistics,
            datasets=datasets,
            split_names=splits)
        super().__init__(spec=spec)