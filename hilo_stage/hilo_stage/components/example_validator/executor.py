import logging
from typing import Any, Dict, List, Text

from tfx.components.example_validator import executor, labels
from tfx import types
from tfx.types import artifact_utils
from tfx.utils import io_utils
import tensorflow_data_validation as tfdv


class Executor(executor.Executor):
    """
    Executor is just a copy of
    tfx.components.example_validator.executor.Executor. The reason for this
    new Executor is because the original does not allow the client to
    specify the input and output splits. Once this is allowed, this Executor
    will not be needed
    """
    def Do(self, input_dict: Dict[Text, List[types.Artifact]],
           output_dict: Dict[Text, List[types.Artifact]],
           exec_properties: Dict[Text, Any]) -> None:
        self._log_startup(input_dict, output_dict, exec_properties)
        logging.info('Validating schema against the computed statistics.')

        split_uris: List[Text] = []
        for artifact in input_dict[executor.STATISTICS_KEY]:
            for split in artifact_utils.decode_split_names(
                    artifact.split_names):
                split_uris.append(split)

        label_inputs = {
            labels.STATS:
            tfdv.load_statistics(
                io_utils.get_only_uri_in_dir(
                    artifact_utils.get_split_uri(
                        input_dict[executor.STATISTICS_KEY], split_uris[0]))),
            labels.SCHEMA:
            io_utils.SchemaReader().read(
                io_utils.get_only_uri_in_dir(
                    artifact_utils.get_single_uri(
                        input_dict[executor.SCHEMA_KEY])))
        }
        output_uri = artifact_utils.get_single_uri(
            output_dict[executor.ANOMALIES_KEY])
        label_outputs = {labels.SCHEMA_DIFF_PATH: output_uri}
        self._Validate(label_inputs, label_outputs)
        logging.info(
            'Validation complete. Anomalies written to {}.'.format(output_uri))
