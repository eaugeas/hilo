from typing import Any, Dict, Text

from tfx.components.trainer.executor import TrainerFnArgs
import tensorflow as tf
import tensorflow_model_analysis as tfma
import tensorflow_transform as tft
from tensorflow_transform.tf_metadata import schema_utils

NUMERIC_FEATURE_KEYS = [
    'timestamp',
    't_degc',
    'tpot_k',
    'tdew_degc',
    'rh_perc',
    'vpmax_mbar',
    'vpact_mbar',
    'vpdef_mbar',
    'sh_g_kg',
    'h2oc_mmol_mol',
    'rho_g_m__3',
    'wv_m_s',
    'max__wv_m_s',
    'wd_deg'
]

LABEL_KEYS = ['p_mbar']


def _get_raw_feature_spec(schema):
    return schema_utils.schema_as_feature_spec(schema).feature_spec


def _transformed_name(key: Text) -> Text:
    if key in NUMERIC_FEATURE_KEYS:
        return 'input_{0}'.format(NUMERIC_FEATURE_KEYS.index(key) + 1)
    elif key in LABEL_KEYS:
        return 'label_{0}'.format(LABEL_KEYS.index(key) + 1)
    else:
        raise KeyError(
            'key {0} not in keys {1}'.format(key, NUMERIC_FEATURE_KEYS))


def _transformed_names(keys):
    return [_transformed_name(key) for key in keys]


def _estimator(
        base_model,
        serving_model_dir: Text,
        warm_start_from=None
):
    run_config = tf.estimator.RunConfig(
        save_checkpoints_steps=999, keep_checkpoint_max=5)
    run_config.replace(
        model_dir=serving_model_dir)

    columns = []
    for column in NUMERIC_FEATURE_KEYS:
        name = _transformed_name(column)
        columns.append(
            tf.compat.v1.feature_column.numeric_column(name))

    return tf.compat.v1.estimator.DNNClassifier(
        hidden_units=[1, 14, 1],
        feature_columns=columns,
        model_dir=base_model,
        warm_start_from=warm_start_from
    )


def _input_dataset(
        file_pattern: Text,
        transform_output: tft.TFTransformOutput,
        batch_size: int = 200
) -> tf.data.Dataset:
    features = transform_output.transformed_feature_spec().copy()
    return tf.data.experimental.make_batched_features_dataset(
        file_pattern=file_pattern,
        batch_size=batch_size,
        features=features,
        reader=lambda files: tf.data.TFRecordDataset(
            files,
            compression_type='GZIP'),
        label_key=_transformed_name(LABEL_KEYS[0]))


def _train_spec(
        file_pattern: Text,
        transform_output: tft.TFTransformOutput,
        max_steps: int
) -> tf.estimator.TrainSpec:
    return tf.estimator.TrainSpec(
        lambda: _input_dataset(file_pattern, transform_output),
        max_steps=max_steps)


def _serving_input_receiver_fn(
        transform_output: tft.TFTransformOutput,
        schema
) -> tf.estimator.export.ServingInputReceiver:
    raw_feature_spec = _get_raw_feature_spec(schema)
    for key in LABEL_KEYS:
        raw_feature_spec.pop(key)

    raw_input_fn = tf.estimator.export.build_parsing_serving_input_receiver_fn(
        raw_feature_spec, default_batch_size=None)
    serving_input_receiver = raw_input_fn()

    transformed_features = transform_output.transform_raw_features(
        serving_input_receiver.features)

    return tf.estimator.export.ServingInputReceiver(
        transformed_features, serving_input_receiver.receiver_tensors)


def _eval_spec(
        file_pattern: Text,
        transform_output: tft.TFTransformOutput,
        schema,
        steps: int
) -> tf.estimator.EvalSpec:
    exporter = tf.estimator.FinalExporter(
        'weather', lambda: _serving_input_receiver_fn(
            transform_output, schema))
    return tf.estimator.EvalSpec(
        lambda: _input_dataset(file_pattern, transform_output),
        steps=steps,
        exporters=[exporter],
        name='weather-eval')


def _eval_input_receiver_fn(transform_output, schema):
    raw_feature_spec = _get_raw_feature_spec(schema)
    serialized_tf_example = tf.compat.v1.placeholder(
        dtype=tf.string, shape=[None], name='input_example_tensor')
    features = tf.io.parse_example(
        serialized=serialized_tf_example, features=raw_feature_spec)
    transformed_features = transform_output.transform_raw_features(features)
    receiver_tensors = {'examples': serialized_tf_example}
    features.update(transformed_features)

    return tfma.export.EvalInputReceiver(
        features=features,
        receiver_tensors=receiver_tensors,
        labels=transformed_features[_transformed_name(LABEL_KEYS[0])])


def trainer_fn(
        trainer_fn_args: TrainerFnArgs,
        schema
) -> Dict[str, Any]:
    transform_output = tft.TFTransformOutput(
        trainer_fn_args.transform_output)

    return {
        'estimator': _estimator(
            trainer_fn_args.base_model,
            trainer_fn_args.serving_model_dir),
        'train_spec': _train_spec(
            trainer_fn_args.train_files,
            transform_output,
            trainer_fn_args.train_steps),
        'eval_spec': _eval_spec(
            trainer_fn_args.eval_files,
            transform_output,
            schema,
            trainer_fn_args.eval_steps),
        'eval_input_receiver_fn': lambda: _eval_input_receiver_fn(
            transform_output, schema)
    }
