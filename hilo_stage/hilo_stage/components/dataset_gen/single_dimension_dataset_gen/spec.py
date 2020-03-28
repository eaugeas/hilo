from typing import Any, Dict, List, Text

from tfx.types.artifact import Artifact
from tfx.types import standard_artifacts
from tfx.types.component_spec import ExecutionParameter
from tfx.types.component_spec import ChannelParameter
from tfx.types.component_spec import ComponentSpec


class Datasets(Artifact):
    TYPE_NAME = 'Datasets'


class SingleDimensionGenSpec(ComponentSpec):
    """SingleDimensionGenSpec component spec."""

    PARAMETERS: Dict[Any, Any] = {
        'split_names': ExecutionParameter(type=List[Text]),
    }
    INPUTS = {
        'examples': ChannelParameter(
            type=standard_artifacts.Examples),
        'schema': ChannelParameter(
            type=standard_artifacts.Schema,
            optional=True),
        'statistics': ChannelParameter(
            type=standard_artifacts.ExampleStatistics,
            optional=True),
    }
    OUTPUTS = {
        'datasets': ChannelParameter(type=Datasets)
    }
