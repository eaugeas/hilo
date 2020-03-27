import json
from typing import Dict, List, Text, Tuple, Union

from abc import ABC
import apache_beam as beam
import numpy as np
import six
from tfx_bsl.coders.csv_decoder import (
    ColumnInfo as ValueInfo,
    ColumnName as ValueName,
    ColumnType as ValueType)

JsonValue = Union[Text, int, float]
JsonCell = Tuple[Text, JsonValue]
JsonCellSerialized = Text
JsonLine = Text


def serialize_json_cell(cell: JsonCell) -> Text:
    return json.dumps(cell)


def deserialize_json_cell(s: Text) -> JsonCell:
    return json.loads(s)  # type: ignore


@beam.typehints.with_input_types(JsonLine)
@beam.typehints.with_output_types(beam.typehints.List[JsonCellSerialized])
class ParseJsonLine(beam.DoFn, ABC):
    """A beam.DoFn to parse JSONLines into List[JsonCell]"""

    def __init__(self):
        super(ParseJsonLine, self).__init__()

    def setup(self):
        pass

    def process(self, line: JsonLine):
        record = json.loads(line)
        normalized_record = ParseJsonLine.normalize(record)
        yield [
            serialize_json_cell((field, normalized_record[field]))
            for field in normalized_record]

    @staticmethod
    def prop_name(namespace, prop):
        if len(namespace) == 0:
            return prop
        else:
            return '{0}.{1}'.format(namespace, prop)

    @staticmethod
    def normalize_record(namespace, record, result):
        for prop in record:
            normalized_name = ParseJsonLine.prop_name(namespace, prop)
            if (isinstance(record[prop], int)
                    or isinstance(record[prop], float)
                    or isinstance(record[prop], str)
                    or record[prop] is None):
                result[normalized_name] = record[prop]
            elif isinstance(record[prop], list):
                result[normalized_name] = json.dumps(record[prop])
            elif isinstance(record[prop], dict):
                ParseJsonLine.normalize_record(
                    normalized_name, record[prop], result)
            else:
                raise ValueError(
                    'unexpected instance type in'
                    ' record {0} for property {1}'.format(record, prop))

    @staticmethod
    def normalize(record):
        normalized = {}
        ParseJsonLine.normalize_record('', record, normalized)
        return normalized


@beam.typehints.with_input_types(beam.typehints.List[JsonCellSerialized])
@beam.typehints.with_output_types(beam.typehints.List[ValueInfo])
class ValueTypeInferrer(beam.CombineFn, ABC):
    """A beam.CombineFn to infer Json key types."""

    def __init__(self):
        super(ValueTypeInferrer, self).__init__()

    def create_accumulator(self) -> Dict[ValueName, ValueType]:
        """Creates an empty accumulator to keep track of the feature types."""
        return {}

    def add_input(
            self,
            accumulator: Dict[ValueName, ValueType],
            serialized_cells: List[JsonCellSerialized]
    ) -> Dict[ValueName, ValueType]:
        """Updates the feature types in the accumulator using
        the values provided in the cells.
        """
        if not serialized_cells:
            return accumulator

        for serialized_cell in serialized_cells:
            cell = deserialize_json_cell(serialized_cell)
            prop_name = cell[0]
            prop_value = cell[1]

            previous_type = accumulator.get(prop_name, None)
            current_type = _infer_value_type(prop_value)

            if previous_type is None or current_type < previous_type:
                accumulator[prop_name] = current_type
        return accumulator

    def merge_accumulators(self, accumulators) -> Dict[ValueName, ValueType]:
        result: Dict[ValueName, ValueType] = {}
        for shard_types in accumulators:
            # Merge the types inferred in each partition using
            # the type hierarchy. Specifically, whenever we observe
            # a type higher in the type hierarchy we update the type.
            for feature_name, feature_type in six.iteritems(shard_types):
                if (feature_name not in result
                        or feature_type > result[feature_name]):  # noqa: E129
                    result[feature_name] = feature_type
        return result

    def extract_output(
            self,
            accumulator: Dict[ValueName, ValueType],
    ) -> List[ValueInfo]:
        """Return a list of tuples containing the column info."""
        return [
            ValueInfo(prop_name, accumulator.get(
                prop_name, ValueType.UNKNOWN))
            for prop_name in accumulator
        ]


_INT64_MIN = np.iinfo(np.int64).min
_INT64_MAX = np.iinfo(np.int64).max


def _infer_value_type(value: JsonValue) -> ValueType:
    """Infer column type from the input value."""
    if not value:
        return ValueType.UNKNOWN

    # Check if the value is of type INT.
    try:
        if _INT64_MIN <= int(value) <= _INT64_MAX:
            return ValueType.INT
        # We infer STRING type when we have long integer values.
        return ValueType.STRING
    except ValueError:
        # If the type is not INT, we next check for FLOAT type (according
        # to our type hierarchy). If we can convert the string to a
        # float value, we fix the type to be FLOAT. Else we resort to
        # STRING type.
        try:
            float(value)
        except ValueError:
            return ValueType.STRING
        return ValueType.FLOAT
