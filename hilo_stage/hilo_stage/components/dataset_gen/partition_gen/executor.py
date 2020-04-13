import logging
import os
from typing import Any, Dict, List, Text

import apache_beam as beam
import tensorflow as tf
from tensorflow_metadata.proto.v0.statistics_pb2 import (
    DatasetFeatureStatisticsList)
import pyarrow as pa
from tensorflow_data_validation.coders import tf_example_decoder
from tfx.components.base.base_executor import BaseExecutor
from tfx.types import (Artifact, artifact_utils)
from tfx.utils import io_utils

from hilo_rpc.serialize.text import deserialize_from_file

# Keys for input_dict.
EXAMPLES_KEY = 'examples'
DATASETS_KEY = 'datasets'

# Keys for output_dict
PARTITIONS_KEY = 'partitions'


def _partition(
        table: pa.Table,
        datasets: DatasetFeatureStatisticsList
):
    for dataset in datasets.datasets:
        dataset_columns = []
        dataset_column_names = []
        has_all_columns = True
        for feature in dataset.features:
            name = feature.path.step[0]
            if name in table.column_names:
                dataset_columns.append(table.column(name))
                dataset_column_names.append(name)
            else:
                has_all_columns = False
                break
        if has_all_columns:
            dataset_table = pa.Table.from_arrays(
                dataset_columns, dataset_column_names)
            yield beam.pvalue.TaggedOutput(dataset.name, dataset_table)


def _feature_from_value(
        value: Any,
) -> tf.train.Feature:
    # TODO(): there must be a deterministic way to do this
    # instead of trying each type
    try:
        return tf.train.Feature(bytes_list=tf.train.BytesList(value=value))
    except TypeError:
        pass
    try:
        return tf.train.Feature(int64_list=tf.train.Int64List(value=value))
    except TypeError:
        pass
    try:
        return tf.train.Feature(float_list=tf.train.FloatList(value=value))
    except TypeError:
        pass

    raise TypeError('Unknown type for value {0}'.format(value))


def _cleanup_dataset(
        table: pa.Table,
):
    column_names = table.column_names
    for batch in table.to_batches():
        d = batch.to_pydict()
        columns = [d[column_name] for column_name in d]
        for el in zip(*columns):
            feature: Dict[str, Any] = {}
            if None in el:
                continue

            for i in range(0, len(column_names)):
                feature[column_names[i]] = _feature_from_value(el[i])

            features = tf.train.Features(feature=feature)
            example = tf.train.Example(features=features)
            yield example.SerializeToString()


class Executor(BaseExecutor):
    def Do(
            self,
            input_dict: Dict[Text, List[Artifact]],
            output_dict: Dict[Text, List[Artifact]],
            exec_properties: Dict[Text, Any]
    ):
        self._log_startup(input_dict, output_dict, exec_properties)
        logging.info('Partitions written!')

        split_uris = []
        for artifact in input_dict[EXAMPLES_KEY]:
            for split in artifact_utils.decode_split_names(
                    artifact.split_names):
                uri = os.path.join(artifact.uri, split)
                split_uris.append((split, uri))
        split_uris = list(filter(lambda uri: uri[0] == 'train', split_uris))
        datasets_uri = io_utils.get_only_uri_in_dir(
            artifact_utils.get_single_uri(input_dict[DATASETS_KEY]))
        datasets = deserialize_from_file(
            datasets_uri, DatasetFeatureStatisticsList)
        dataset_names = [dataset.name for dataset in datasets.datasets]

        with self._make_beam_pipeline() as p:
            for split, uri in split_uris:
                logging.info('Partition split {}'.format(split))

                output_uri = artifact_utils.get_split_uri(
                    output_dict[PARTITIONS_KEY], split)
                input_uri = io_utils.all_files_pattern(uri)

                partitioned = (
                        p
                        | 'ReadData.' + split >>
                        beam.io.ReadFromTFRecord(file_pattern=input_uri)
                        | 'DecodeData.' + split >>
                        tf_example_decoder.DecodeTFExample()
                        | 'PartitionData.' + split >>
                        beam.FlatMap(_partition, datasets).with_outputs(
                            *dataset_names))

                for i in range(0, len(datasets.datasets)):
                    dataset_name = datasets.datasets[i].name
                    output_path = os.path.join(
                        output_uri, dataset_name, split)
                    _ = (partitioned[dataset_name]
                         | 'CleanupDatasets.' + split + '.' + dataset_name >>
                         beam.FlatMap(_cleanup_dataset)
                         | 'WriteOutput.' + split + '.' + dataset_name >>
                         beam.io.WriteToTFRecord(
                             output_path,
                             file_name_suffix='.gz',
                         ))
