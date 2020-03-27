from typing import List, Optional, Text

from tfx.types import Channel, artifact, standard_artifacts, artifact_utils
from tfx.components import StatisticsGen as TfxStatisticsGen
import tensorflow_data_validation as tfdv


class StatisticsGen(TfxStatisticsGen):
    """StatisticsGen is just an abstraction on top of the official
    TFX StatisticsGen component for easy instantiation"""
    def __init__(
            self,
            examples: Optional[Channel] = None,
            schema: Optional[Channel] = None,
            stats_options: Optional[tfdv.StatsOptions] = None,
            instance_name: Optional[Text] = None,
            split_names: Optional[List[Text]] = None,
    ):
        splits: List[Text] = []
        if split_names:
            splits = split_names
        else:
            for el in artifact.DEFAULT_EXAMPLE_SPLITS:
                splits.append(el)

        statistics_artifact = standard_artifacts.ExampleStatistics()
        statistics_artifact.split_names = artifact_utils.encode_split_names(
            split_names)
        output = Channel(
            type=standard_artifacts.ExampleStatistics,
            artifacts=[statistics_artifact])

        super().__init__(
            examples=examples,
            schema=schema,
            stats_options=stats_options,
            output=output,
            instance_name=instance_name)
