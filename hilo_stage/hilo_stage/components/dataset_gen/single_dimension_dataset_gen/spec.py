from typing import Any, Dict, List, Text

from tfx.types import standard_artifacts
from tfx.types.component_spec import (
    ChannelParameter, ComponentSpec, ExecutionParameter)

from hilo_stage.components.dataset_gen.entity.artifact import Datasets


class SingleDimensionGenSpec(ComponentSpec):
    """SingleDimensionGenSpec component spec."""

    PARAMETERS: Dict[Any, Any] = {
        'split_names': ExecutionParameter(type=List[Text]),
    }
    INPUTS = {
        'examples': ChannelParameter(type=standard_artifacts.Examples),
        'statistics': ChannelParameter(
            type=standard_artifacts.ExampleStatistics,
            optional=True),
    }
    OUTPUTS = {
        'datasets': ChannelParameter(type=Datasets)
    }