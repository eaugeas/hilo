from datetime import datetime
from typing import Any, Dict, Text

import tensorflow as tf


def datetime_to_timestamp(t: tf.Tensor) -> tf.Tensor:
    s = t.numpy().decode('utf-8')

    timestamp = datetime.timestamp(datetime.strptime(s, '%d.%m.%Y %H:%M:%S'))
    return tf.convert_to_tensor(
        int(timestamp),
        dtype=tf.int64
    )


def preprocessing_fn(inputs: Dict[Text, Any]) -> Dict[Text, Any]:
    """preprocessing_fn is the function executed by the Transform
    stage"""
    results: Dict[Text, Any] = {}

    for key in inputs:
        new_key = key.lstrip('"').rstrip('"')
        results[new_key] = inputs[key]

    results['timestamp'] = tf.SparseTensor(
        inputs['"Date Time"'].indices,
        tf.map_fn(
            lambda t: tf.py_function(
                datetime_to_timestamp, [t], [tf.int64])[0],
            inputs['"Date Time"'].values,
            dtype=tf.int64),
        inputs['"Date Time"'].dense_shape)

    return results
