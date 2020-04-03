from abc import ABC
import logging
import os
from typing import Any, Dict, Iterable, List, Optional, Text, Callable

import apache_beam as beam
import tensorflow as tf
from tfx.components.example_gen.base_example_gen_executor import (
    BaseExampleGenExecutor)
from tfx.components.example_gen.base_example_gen_executor import INPUT_KEY
from tfx_bsl.coders import csv_decoder
from tfx.types import Artifact, artifact_utils

from hilo_stage.components.example_gen.json_example_gen.json_decoder import (
    JsonValue, JsonCellSerialized, ParseJsonLine,
    ValueTypeInferrer, ValueInfo, deserialize_json_cell)

TypeHandler = Callable[[JsonValue], tf.train.Feature]


@beam.typehints.with_input_types(List[JsonCellSerialized],
                                 List[ValueInfo])
@beam.typehints.with_output_types(tf.train.Example)
class _ParsedJsonToTfExample(beam.DoFn, ABC):
    """A beam.DoFn to convert a parsed CSV line to a tf.Example."""

    def __init__(self, *unused_args, **unused_kwargs):
        super().__init__(*unused_args, **unused_kwargs)
        self._prop_handlers: Optional[Dict[Text, TypeHandler]] = None

    def _initialize_prop_infos(
            self,
            prop_infos: List[ValueInfo],
    ) -> Dict[Text, TypeHandler]:
        prop_handlers = {}
        for prop_info in prop_infos:
            if prop_info.type == csv_decoder.ColumnType.INT:
                prop_handlers[prop_info.name] = (
                    lambda json_value: tf.train.Feature(
                        int64_list=tf.train.Int64List(
                            value=[int(json_value)])))
            elif prop_info.type == csv_decoder.ColumnType.FLOAT:
                prop_handlers[prop_info.name] = (
                    lambda json_value: tf.train.Feature(
                        float_list=tf.train.FloatList(
                            value=[float(json_value)])))
            elif prop_info.type == csv_decoder.ColumnType.STRING:
                prop_handlers[prop_info.name] = (
                    lambda json_value: tf.train.Feature(
                        bytes_list=tf.train.BytesList(
                            value=[tf.compat.as_bytes(json_value)])))
        self._prop_handlers = prop_handlers
        return self._prop_handlers

    def process(
            self,
            json_cells_serialized: List[JsonCellSerialized],
            prop_infos: List[ValueInfo],
            **kwargs,
    ) -> Iterable[tf.train.Example]:
        prop_handlers: Dict[Text, TypeHandler] = (
                self._prop_handlers or
                self._initialize_prop_infos(prop_infos))

        # skip blank lines.
        if not json_cells_serialized:
            return {}

        feature = {}
        for json_cell_serialized in json_cells_serialized:
            json_cell = deserialize_json_cell(json_cell_serialized)
            prop_name = json_cell[0]
            prop_value = json_cell[1]
            if not json_cell:
                feature[prop_name] = tf.train.Feature()
                continue

            handler_fn = prop_handlers.get(prop_name, None)
            if not handler_fn:
                raise ValueError(
                    'Internal error: failed to infer type'
                    ' of column {} while it'
                    'had at least some values {}'.format(
                        prop_name, prop_value))
            feature[prop_name] = handler_fn(prop_value)
        yield tf.train.Example(features=tf.train.Features(feature=feature))


@beam.ptransform_fn
@beam.typehints.with_input_types(beam.Pipeline)
@beam.typehints.with_output_types(tf.train.Example)
def _JsonToExample(
        pipeline: beam.Pipeline,
        input_dict: Dict[Text, List[Artifact]],
        exec_properties: Dict[Text, Any],  # pylint: disable=unused-argument
        split_pattern: Text,
) -> beam.pvalue.PCollection:
    input_base_uri = artifact_utils.get_single_uri(input_dict[INPUT_KEY])
    json_pattern = os.path.join(input_base_uri, split_pattern)

    logging.info(
        'Processing input json data {} to TFExample.'.format(json_pattern))
    json_files = tf.io.gfile.glob(json_pattern)
    if not json_files:
        raise RuntimeError(
            'Split pattern {} does not match any files.'.format(json_pattern))

    parsed_json_lines = (
            pipeline
            | 'ReadFromText' >> beam.io.ReadFromText(file_pattern=json_pattern)
            | 'ParseJSONLine' >> beam.ParDo(ParseJsonLine()))

    value_infos = beam.pvalue.AsSingleton(
        parsed_json_lines
        | 'InferColumnTypes' >> beam.CombineGlobally(ValueTypeInferrer()))

    return (parsed_json_lines
            | 'ToTFExample' >> beam.ParDo(
                _ParsedJsonToTfExample(), value_infos))


class Executor(BaseExampleGenExecutor):
    def GetInputSourceToExamplePTransform(self) -> beam.PTransform:
        """Returns PTransform for CSV to TF examples."""
        return _JsonToExample
