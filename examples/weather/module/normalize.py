from typing import Any, Dict, Text

import tensorflow as tf
import tensorflow_transform as tft

NUMERIC_FEATURE_KEYS = [
    'timestamp',
    'p_mbar',
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

LABEL_KEY = 'p_mbar'

RAW_DATA_FEATURE_SPEC = dict(
    [(name, tf.io.FixedLenFeature([], tf.float32))
     for name in NUMERIC_FEATURE_KEYS]
)

RAW_DATA_METADATA = tft.tf_metadata.dataset_metadata.DatasetMetadata(
    tft.tf_metadata.dataset_schema.schema_utils.schema_from_feature_spec(
        RAW_DATA_FEATURE_SPEC))


def _fill_in_missing(x):
    """Replace missing values in a SparseTensor.
    Fills in missing values of `x` with '' or 0, and converts to a dense tensor.
    Args:
    x: A `SparseTensor` of rank 2.  Its dense shape should have size at most 1
      in the second dimension.
    Returns:
    A rank 1 tensor where missing values of `x` have been filled in.
    """
    default_value = '' if x.dtype == tf.string else 0
    return tf.squeeze(
        tf.sparse.to_dense(
            tf.SparseTensor(x.indices, x.values, [x.dense_shape[0], 1]),
            default_value), axis=1)


def _transformed_name(key: Text) -> Text:
    if key not in NUMERIC_FEATURE_KEYS:
        raise KeyError(
            'Key {0} does not belong to NUMERIC_FEATURE_KEYS'.format(key))
    return '{0}_tx'.format(key)


def preprocessing_fn(inputs: Dict[Text, Any]) -> Dict[Text, Any]:
    """preprocessing_fn is the function executed by the Transform
        stage"""
    outputs = {}
    for key in NUMERIC_FEATURE_KEYS:
        outputs[_transformed_name(key)] = tft.scale_to_0_1(
            _fill_in_missing(inputs[key]))
    return outputs
