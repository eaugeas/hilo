from typing import Optional

from tfx.components.base import executor_spec
from tfx.components.base.base_component import BaseComponent
from tfx.types import Channel
from tfx.types import artifact
from tfx.types import artifact_utils

from hilo_stage.dimension_gen.entity.artifact import ExampleDimensions
from hilo_stage.dimension_gen.single_dimension_gen.executor import Executor
from hilo_stage.dimension_gen.single_dimension_gen.spec import (
    SingleDimensionGenSpec)


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
    ):
        """Construct a SingleDimensionGen component."""
        dimension_artifacts = ExampleDimensions()
        dimension_artifacts.split_names = artifact_utils.encode_split_names(
            artifact.DEFAULT_EXAMPLE_SPLITS)
        dimensions = Channel(
            type=ExampleDimensions,
            artifacts=[dimension_artifacts])

        spec = SingleDimensionGenSpec(
            examples=examples,
            schema=schema,
            statistics=statistics,
            dimensions=dimensions)
        super().__init__(spec=spec)
