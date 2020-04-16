from typing import List, Optional, Text, Union

from tfx.components.base import base_component, executor_spec
from tfx.orchestration import data_types
from tfx.types import Channel, standard_artifacts, artifact_utils
from tfx.types.standard_component_specs import TransformSpec

from hilo_stage.components.transform.executor import Executor
from hilo_stage.components.utils.splits import splits_or_example_defaults

ProcessingFn = Union[Text, data_types.RuntimeParameter]


class Transform(base_component.BaseComponent):
    """A Transform component for input examples.

     TFX has its Transform component, and this one uses the same
     executor. The reason for this one to exist, is that the TFX
     component does not allow to specify the splits to use, it just
     assumes `train` and `eval`. This component will be unnecessary
     once TFX Transform allows to set the input and output splits
     as other components do"""
    SPEC_CLASS = TransformSpec
    EXECUTOR_SPEC = executor_spec.ExecutorClassSpec(Executor)

    def __init__(self,
                 examples: Channel = None,
                 schema: Channel = None,
                 module_file: Optional[ProcessingFn] = None,
                 preprocessing_fn: Optional[ProcessingFn] = None,
                 transform_graph: Optional[Channel] = None,
                 split_names: Optional[List[Text]] = None,
                 input_data: Optional[Channel] = None,
                 instance_name: Optional[Text] = None):
        if bool(module_file) == bool(preprocessing_fn):
            raise ValueError(
                'Exactly one of `module_file` or `preprocessing_fn`'
                ' must be supplied.')

        split_names = splits_or_example_defaults(split_names)
        transform_artifact = standard_artifacts.Examples()
        transform_artifact.split_names = artifact_utils.encode_split_names(
            split_names)

        transform_graph = transform_graph or Channel(
            type=standard_artifacts.TransformGraph,
            artifacts=[standard_artifacts.TransformGraph()])

        transformed_examples = Channel(type=standard_artifacts.Examples,
                                       artifacts=[transform_artifact])

        spec = TransformSpec(examples=examples,
                             schema=schema,
                             module_file=module_file,
                             preprocessing_fn=preprocessing_fn,
                             transform_graph=transform_graph,
                             transformed_examples=transformed_examples)
        super(Transform, self).__init__(spec=spec, instance_name=instance_name)
