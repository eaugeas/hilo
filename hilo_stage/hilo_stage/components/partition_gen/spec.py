from typing import Any, Dict, Text

from tfx.types import standard_artifacts
from tfx.types.component_spec import ChannelParameter, ComponentSpec

from hilo_stage.components.partition_gen.artifact import Partitions


class PartitionSpec(ComponentSpec):
    """PartitionSpec component spec."""
    PARAMETERS: Dict[Text, Any] = {}

    INPUTS: Dict[Text, ChannelParameter] = {
        'statistics':
        ChannelParameter(type=standard_artifacts.ExampleStatistics,
                         optional=False),
        'schema':
        ChannelParameter(type=standard_artifacts.Schema, optional=False),
        'examples':
        ChannelParameter(type=standard_artifacts.Examples, optional=False)
    }
    OUTPUTS: Dict[Text, ChannelParameter] = {
        'partitions': ChannelParameter(type=Partitions)
    }
