import os
import logging
from typing import Any, Dict, List, Text

from tfx.components.transform import executor, labels
from tfx.types import Artifact, artifact_utils
from tfx.utils import io_utils


class Executor(executor.Executor):
    def Do(self, input_dict: Dict[Text, List[Artifact]],
           output_dict: Dict[Text, List[Artifact]],
           exec_properties: Dict[Text, Any]) -> None:
        """
        Executor is just a copy of tfx.components.transform.executor.Executor.
        The reason for this new Executor is because the original does not
        allow the client to specify the input and output splits. Once this
        is allowed, this Executor will not be needed
        """
        split_uris: List[Text] = []
        for artifact in input_dict[executor.EXAMPLES_KEY]:
            for split in artifact_utils.decode_split_names(
                    artifact.split_names):
                split_uris.append(split)

        self._log_startup(input_dict, output_dict, exec_properties)
        data_uris = []
        for split in split_uris:
            data_uris.append(
                artifact_utils.get_split_uri(
                    input_dict[executor.EXAMPLES_KEY], split))

        schema_file = io_utils.get_only_uri_in_dir(
            artifact_utils.get_single_uri(input_dict[executor.SCHEMA_KEY]))
        transform_output = artifact_utils.get_single_uri(
            output_dict[executor.TRANSFORM_GRAPH_KEY])
        transformed_data_uris = []
        for split in split_uris:
            transformed_data_uris.append(
                artifact_utils.get_split_uri(
                    output_dict[executor.TRANSFORMED_EXAMPLES_KEY], split))
        temp_path = os.path.join(
            transform_output, executor._TEMP_DIR_IN_TRANSFORM_OUTPUT)
        logging.debug('Using temp path %s for tft.beam', temp_path)

        def _GetCachePath(label, params_dict):
            if label not in params_dict:
                return None
            else:
                return artifact_utils.get_single_uri(params_dict[label])

        label_inputs = {
            labels.COMPUTE_STATISTICS_LABEL:
                False,
            labels.SCHEMA_PATH_LABEL:
                schema_file,
            labels.EXAMPLES_DATA_FORMAT_LABEL:
                labels.FORMAT_TF_EXAMPLE,
            labels.ANALYZE_DATA_PATHS_LABEL:
                io_utils.all_files_pattern(data_uris[0]),
            labels.ANALYZE_PATHS_FILE_FORMATS_LABEL:
                labels.FORMAT_TFRECORD,
            labels.TRANSFORM_DATA_PATHS_LABEL: [
                io_utils.all_files_pattern(uri)
                for uri in data_uris],
            labels.TRANSFORM_PATHS_FILE_FORMATS_LABEL: [
                labels.FORMAT_TFRECORD for uri in data_uris],
            labels.TFT_STATISTICS_USE_TFDV_LABEL:
                True,
            labels.MODULE_FILE:
                exec_properties.get('module_file', None),
            labels.PREPROCESSING_FN:
                exec_properties.get('preprocessing_fn', None),
            # TODO(b/149754658): switch to True once the TFXIO integration is
            # complete.
            labels.USE_TFXIO_LABEL: False,
        }
        cache_input = _GetCachePath('cache_input_path', input_dict)
        if cache_input is not None:
            label_inputs[labels.CACHE_INPUT_PATH_LABEL] = cache_input

        label_outputs = {
            labels.TRANSFORM_METADATA_OUTPUT_PATH_LABEL: transform_output,
            labels.TRANSFORM_MATERIALIZE_OUTPUT_PATHS_LABEL: [
                os.path.join(
                    uri, executor._DEFAULT_TRANSFORMED_EXAMPLES_PREFIX)
                for uri in transformed_data_uris
            ],
            labels.TEMP_OUTPUT_LABEL: str(temp_path),
        }
        cache_output = _GetCachePath('cache_output_path', output_dict)
        if cache_output is not None:
            label_outputs[labels.CACHE_OUTPUT_PATH_LABEL] = cache_output
        status_file = 'status_file'  # Unused
        self.Transform(label_inputs, label_outputs, status_file)
        logging.debug(
            'Cleaning up temp path %s on executor success', temp_path)
        io_utils.delete_dir(temp_path)
