import os
import logging
from typing import Any, Dict, List, Text

import tensorflow_data_validation as tfdv
from tensorflow_metadata.proto.v0.statistics_pb2 import (
    DatasetFeatureStatisticsList, DatasetFeatureStatistics)
from tfx.types import (Artifact, artifact_utils)
from tfx.components.base.base_executor import BaseExecutor
from tfx.utils import io_utils

# Keys for input_dict
STATISTICS_KEY = 'statistics'

# Keys for output_dict
DATASETS_KEY = 'datasets'

# Default file name for dimensions generated.
_DEFAULT_FILE_NAME = 'datasets.pbtxt'


def infer_dimensions(
        stats: DatasetFeatureStatisticsList,
) -> DatasetFeatureStatisticsList:
    result = []
    for dataset in stats.datasets:
        for feature in dataset.features:
            common_stats = getattr(
                feature, feature.WhichOneof('stats')).common_stats
            if dataset.num_examples * .05 < common_stats.num_non_missing:
                if feature.WhichOneof('field_id') == 'name':
                    name = feature.name
                elif feature.WhichOneof('field_id') == 'path':
                    name = '.'.join(feature.path.step)
                else:
                    raise ValueError(
                        'unknown field_id oneof {0}'.format(
                            feature.WhichOneof('field_id')))

                dataset = DatasetFeatureStatistics(
                    name=name,
                    num_examples=common_stats.num_non_missing,
                    weighted_num_examples=0,
                    features=[feature],
                    cross_features=[])
                result.append(dataset)
    return DatasetFeatureStatisticsList(datasets=result)


class Executor(BaseExecutor):
    """Computes the single-dimension partitions that have enough
    data for consideration."""

    def Do(
            self,
            input_dict: Dict[Text, List[Artifact]],
            output_dict: Dict[Text, List[Artifact]],
            exec_properties: Dict[Text, Any]
    ) -> None:
        self._log_startup(input_dict, output_dict, exec_properties)

        logging.info('Generating dimensions for split {}'.format('train'))
        stats_uri = io_utils.get_only_uri_in_dir(
            artifact_utils.get_split_uri(input_dict[STATISTICS_KEY], 'train'))
        output_uri = os.path.join(
            artifact_utils.get_single_uri(output_dict[DATASETS_KEY]),
            _DEFAULT_FILE_NAME)

        stats = tfdv.load_statistics(stats_uri)
        dimension_sets = infer_dimensions(stats)
        io_utils.write_pbtxt_file(output_uri, dimension_sets)
        logging.info('Dimension sets written to %s.' % output_uri)
