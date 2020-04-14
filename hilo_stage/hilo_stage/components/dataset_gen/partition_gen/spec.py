from typing import Dict, List, Text

from tfx.types import standard_artifacts
from tfx.types.component_spec import (
    ChannelParameter, ComponentSpec, ExecutionParameter)

from hilo_stage.components.types.artifact import Datasets


class PartitionGenSpec(ComponentSpec):
    """PartitionGenSpec component spec."""

    PARAMETERS: Dict[Text, ExecutionParameter] = {
        'split_names': ExecutionParameter(type=List[Text]),
    }
    INPUTS: Dict[Text, ChannelParameter] = {
        'examples': ChannelParameter(type=standard_artifacts.Examples),
        'datasets': ChannelParameter(type=Datasets),
    }
    OUTPUTS: Dict[Text, ChannelParameter] = {
        'partitions': ChannelParameter(type=standard_artifacts.Examples)
    }
