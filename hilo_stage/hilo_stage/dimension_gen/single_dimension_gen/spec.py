from typing import Any, Dict

from tfx.types import standard_artifacts
from tfx.types.component_spec import ChannelParameter
from tfx.types.component_spec import ComponentSpec

from hilo_stage.dimension_gen.entity.artifact import ExampleDimensions


class SingleDimensionGenSpec(ComponentSpec):
    """SingleDimensionGenSpec component spec."""

    PARAMETERS: Dict[Any, Any] = {}
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
        'dimensions': ChannelParameter(type=ExampleDimensions),
    }
