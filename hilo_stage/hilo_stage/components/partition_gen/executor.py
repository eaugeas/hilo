import os
from typing import Any, Dict, List, Text, Tuple

import tensorflow_data_validation as tfdv
from tensorflow_metadata.proto.v0.schema_pb2 import Schema
from tensorflow_metadata.proto.v0.statistics_pb2 import (
    DatasetFeatureStatistics, DatasetFeatureStatisticsList,
    FeatureNameStatistics)
from tfx import types
from tfx.types import artifact_utils
from tfx.components.base import base_executor
from tfx.utils import io_utils

from hilo_rpc.proto.partition_pb2 import Partition, ExampleSplit

# Keys for input_dict
STATISTICS_KEY = 'statistics'
SCHEMA_KEY = 'schema'
EXAMPLES_KEY = 'examples'

# Keys for output_dict
PARTITIONS_KEY = 'partitions'


def feature_name(feature: FeatureNameStatistics) -> Text:
    print('feature: ', feature)
    if feature.WhichOneof('field_id') == 'name':
        return feature.name  # type: ignore
    elif feature.WhichOneof('field_id') == 'path':
        return '.'.join(feature.path.step)
    elif feature.WhichOneof('field_id') is None:
        raise ValueError('feature has no field_id')
    else:
        raise ValueError(
            'unknown feature field_id type. Received `{0}`'.format(
                feature.WhichOneof('field_id')))


def partition_fn(datasets: DatasetFeatureStatisticsList, schema: Schema,
                 examples: types.Artifact) -> List[List[Text]]:
    result: List[List[Text]] = []

    for dataset in datasets.datasets:
        timestamp_fs = list(
            filter(lambda f: feature_name(f) == 'timestamp', dataset.features))

        if len(timestamp_fs) != 1:
            raise ValueError('dataset should have one `timestmap` feature')

        for feature in dataset.features:
            if feature.path.step == 'timestamp':
                continue

            common_stats = getattr(feature,
                                   feature.WhichOneof('stats')).common_stats

            if dataset.num_examples * .05 < common_stats.num_non_missing:
                name = feature_name(feature)
                if len(name) > 0:
                    result.append(['timestamp', name])
                else:
                    raise ValueError(
                        'feature does not have a name {0}'.format(feature))
    return result


def lists_to_partitions(
        datasets: DatasetFeatureStatisticsList,
        schema: Schema,
        examples: types.Artifact,
        partitions: List[List[Text]],
) -> List[Partition]:
    result: List[Partition] = []
    for p in partitions:
        name = '__'.join(p)
        partition = Partition(
            name=name,
            statistics=DatasetFeatureStatisticsList(datasets=[
                DatasetFeatureStatistics(
                    name=name,
                    num_examples=min([
                        getattr(feature, feature.WhichOneof(
                            'stats')).common_stats.num_non_missing
                        for feature in filter(lambda f: feature_name(f) in p,
                                              dataset.features)
                    ]),
                    weighted_num_examples=0,
                    features=list(
                        filter(lambda f: feature_name(f) in p,
                               dataset.features)),
                ) for dataset in datasets.datasets
            ]),
            example_splits=[
                ExampleSplit(split=split,
                             uri=os.path.join(examples.uri, split)) for split
                in artifact_utils.decode_split_names(examples.split_names)
            ],
            schema=Schema(feature=filter(lambda f: f.name in p,
                                         schema.feature),
                          sparse_feature=filter(lambda f: f.name in p,
                                                schema.sparse_feature),
                          weighted_feature=filter(lambda f: f.name in p,
                                                  schema.weighted_feature),
                          string_domain=filter(lambda f: f.name in p,
                                               schema.string_domain),
                          float_domain=filter(lambda f: f.name in p,
                                              schema.float_domain),
                          int_domain=filter(lambda f: f.name in p,
                                            schema.int_domain),
                          default_environment=schema.default_environment))
        result.append(partition)
    return result


def group_stats_and_examples(
    input_dict: Dict[Text, List[types.Artifact]]
) -> List[Tuple[types.Artifact, Dict[Text, DatasetFeatureStatistics]]]:
    result = []
    examples_list = input_dict[EXAMPLES_KEY]
    if len(examples_list) > 1:
        raise ValueError('only one examples artifact expected')

    examples = examples_list[0]
    group = {}
    for split in artifact_utils.decode_split_names(examples.split_names):
        statistics = tfdv.load_statistics(
            io_utils.get_only_uri_in_dir(
                types.artifact_utils.get_split_uri(input_dict[STATISTICS_KEY],
                                                   split)))
        if len(statistics.datasets) != 1:
            raise ValueError('one statistics set expected')
        group[split] = statistics.datasets[0]
    result.append((examples, group))
    return result


class Executor(base_executor.BaseExecutor):
    def Do(self, input_dict: Dict[Text, List[types.Artifact]],
           output_dict: Dict[Text, List[types.Artifact]],
           exec_properties: Dict[Text, Any]):
        self._log_startup(input_dict, output_dict, exec_properties)

        schema = io_utils.SchemaReader().read(
            io_utils.get_only_uri_in_dir(
                artifact_utils.get_single_uri(input_dict[SCHEMA_KEY])))

        groups = group_stats_and_examples(input_dict)
        for examples, datasets in groups:
            datasets = DatasetFeatureStatisticsList(
                datasets=list(datasets.values()))
            partitions = lists_to_partitions(
                datasets, schema, examples,
                partition_fn(datasets, schema, examples))

            for partition in partitions:
                output_uri = os.path.join(
                    artifact_utils.get_single_uri(output_dict[PARTITIONS_KEY]),
                    partition.name)
                io_utils.write_pbtxt_file(
                    os.path.join(output_uri, 'schema.pbtxt'), partition.schema)

                for i in range(0, len(partition.statistics.datasets)):
                    dataset = partition.statistics.datasets[i]
                    example_splits = partition.example_splits[i]

                    io_utils.write_tfrecord_file(
                        os.path.join(output_uri, example_splits.split,
                                     'stats_tfrecord'), dataset)
