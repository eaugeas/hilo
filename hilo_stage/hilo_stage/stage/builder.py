from typing import Any, Dict, Optional, Text, Type

from google.protobuf.message import Message
from tfx.types import Channel, standard_artifacts, artifact_utils
from tfx.components.base.base_component import BaseComponent

from hilo_stage.components.utils.splits import splits_or_example_defaults
from hilo_rpc.proto.stage_pb2 import (
    Stage, PartitionGenConfig,
    JsonExampleGenConfig, SingleDimensionGenConfig,
    StatisticsGenConfig, SchemaGenConfig,
    CsvExampleGenConfig, TransformConfig)


class Context:
    def __init__(
            self,
            id: Text,
            parent: Optional['Context'] = None,
    ):
        self._context: Dict[str, Any] = {}
        if parent:
            self._context = parent._context
        self._id = id

        if self._id in self._context:
            raise ValueError(
                'Created new context for stage with '
                'existing id {0}'.format(self._id))

    @property
    def id(self) -> Text:
        return self._id

    def for_stage(self, id: Text) -> 'Context':
        return Context(id, parent=self)

    def get(self, map_key) -> Any:
        return self._context[map_key]

    def put_outputs(self, message: Message, component: BaseComponent):
        descriptor = message.DESCRIPTOR
        for field in descriptor.fields:
            self.put_self(
                'outputs.{0}'.format(getattr(message, field.name)),
                component.outputs[field.name])

    def put_self(self, key: Text, value: Any):
        map_key = '{0}.{1}'.format(self._id, key)
        self._context[map_key] = value


class ComponentBuilder(object):
    def __init__(self, config: Optional[Any] = None):
        pass

    def build(self, context: Context) -> BaseComponent:
        raise NotImplementedError()


class SchemaGenBuilder(ComponentBuilder):
    def __init__(self, config: Optional[SchemaGenConfig] = None):
        super().__init__(config)
        self._config = config or SchemaGenConfig()

    def build(self, context: Context) -> BaseComponent:
        from tfx.components import SchemaGen

        statistics = context.get(self._config.inputs.statistics)
        component = SchemaGen(
            statistics=statistics,
            infer_feature_shape=self._config.params.infer_feature_shape,
            instance_name=context.id
        )

        context.put_outputs(self._config.outputs, component)
        return component


class StatisticsGenBuilder(ComponentBuilder):
    def __init__(self, config: Optional[StatisticsGenConfig] = None):
        super().__init__(config)
        self._config = config or StatisticsGenConfig()

    def build(self, context: Context) -> BaseComponent:
        from tfx.components import StatisticsGen

        statistics_artifact = standard_artifacts.ExampleStatistics()
        statistics_artifact.split_names = artifact_utils.encode_split_names(
            splits_or_example_defaults(self._config.params.split_names))

        output = Channel(
            type=standard_artifacts.ExampleStatistics,
            artifacts=[statistics_artifact])

        examples = context.get(self._config.inputs.examples)
        component = StatisticsGen(
            examples=examples,
            stats_options=None,
            output=output,
            instance_name=context.id
        )

        context.put_outputs(self._config.outputs, component)
        return component


class SingleDimensionGenBuilder(ComponentBuilder):
    def __init__(self, config: Optional[SingleDimensionGenConfig] = None):
        super().__init__(config)
        self._config = config or SingleDimensionGenConfig()

    def build(self, context: Context) -> BaseComponent:
        from hilo_stage.components import SingleDimensionGen
        split_names = splits_or_example_defaults(
            self._config.params.split_names)

        statistics = context.get(self._config.inputs.statistics)
        examples = context.get(self._config.inputs.examples)
        component = SingleDimensionGen(
            statistics=statistics,
            examples=examples,
            split_names=split_names,
            instance_name=context.id
        )

        context.put_outputs(self._config.outputs, component)
        return component


class PartitionGenBuilder(ComponentBuilder):
    def __init__(self, config: Optional[PartitionGenConfig]):
        super().__init__(config)
        self._config = config or PartitionGenConfig()

    def build(self, context: Context) -> BaseComponent:
        from hilo_stage.components import PartitionGen

        split_names = splits_or_example_defaults(
            self._config.params.split_names)

        partition_artifact = standard_artifacts.Examples()
        partition_artifact.split_names = artifact_utils.encode_split_names(
            splits_or_example_defaults(self._config.params.split_names))

        partitions = Channel(
            type=standard_artifacts.Examples,
            artifacts=[partition_artifact])

        component = PartitionGen(
            examples=context.get(self._config.inputs.examples),
            datasets=context.get(self._config.inputs.datasets),
            partitions=partitions,
            split_names=split_names,
            instance_name=context.id)
        context.put_outputs(self._config.outputs, component)
        return component


class CsvExampleGenBuilder(ComponentBuilder):
    def __init__(self, config: Optional[CsvExampleGenConfig] = None):
        super().__init__(config)
        self._config = config or CsvExampleGenConfig()

    def build(self, context: Context) -> BaseComponent:
        from tfx.components import CsvExampleGen
        from tfx.proto.example_gen_pb2 import Input, Output, SplitConfig

        input_splits = []
        for split in self._config.params.input_config.splits:
            input_splits.append({
                'name': split.name,
                'pattern': split.pattern,
            })

        output_splits = []
        for split in self._config.params.output_config.splits:
            output_splits.append(
                SplitConfig.Split(
                    name=split.name,
                    hash_buckets=split.hash_buckets))

        component = CsvExampleGen(
            instance_name=context.id,
            input=context.get(self._config.inputs.input),
            input_config=Input(splits=input_splits),
            output_config=Output(
                split_config=SplitConfig(splits=output_splits)))
        context.put_outputs(self._config.outputs, component)
        return component


class TransformBuilder(ComponentBuilder):
    def __init__(self, config: Optional[TransformConfig] = None):
        super().__init__(config)
        self._config = config or TransformConfig()

    def build(self, context: Context) -> BaseComponent:
        from hilo_stage.components import Transform

        props = {}

        if not self._config.inputs.examples:
            raise KeyError(
                'transform pipeline requires `examples`'
                ' as one of its inputs')

        props['examples'] = context.get(self._config.inputs.examples)

        if self._config.inputs.schema:
            props['schema'] = context.get(self._config.inputs.schema)

        if not self._config.params.module_file_path:
            raise KeyError(
                'transform pipeline requires `module_file_path`'
                ' as one of its params')

        props['module_file'] = self._config.params.module_file_path
        props['instance_name'] = context.id
        props['split_names'] = splits_or_example_defaults(
            self._config.params.split_names)
        component = Transform(**props)
        context.put_outputs(self._config.outputs, component)
        return component


class JsonExampleGenBuilder(ComponentBuilder):
    def __init__(self, config: Optional[JsonExampleGenConfig] = None):
        super().__init__(config)
        self._config = config or JsonExampleGenConfig()

    def build(self, context: Context) -> BaseComponent:
        from hilo_stage.components import JsonExampleGen
        from tfx.proto.example_gen_pb2 import Input, Output, SplitConfig

        input_splits = []
        for split in self._config.params.input_config.splits:
            input_splits.append({
                'name': split.name,
                'pattern': split.pattern,
            })

        output_splits = []
        for split in self._config.params.output_config.splits:
            output_splits.append(
                SplitConfig.Split(
                    name=split.name,
                    hash_buckets=split.hash_buckets))

        component = JsonExampleGen(
            instance_name=context.id,
            input=context.get(self._config.inputs.input),
            input_config=Input(splits=input_splits),
            output_config=Output(
                split_config=SplitConfig(splits=output_splits)))
        context.put_outputs(self._config.outputs, component)
        return component


class Builder:
    def __init__(self, stage: Optional[Stage] = None):
        self._stage = stage or Stage()

        self._stage_builders: Dict[str, Type[ComponentBuilder]] = {
            'json_example_gen': JsonExampleGenBuilder,
            'statistics_gen': StatisticsGenBuilder,
            'schema_gen': SchemaGenBuilder,
            'single_dimension_gen': SingleDimensionGenBuilder,
            'partition_gen': PartitionGenBuilder,
            'csv_example_gen': CsvExampleGenBuilder,
            'transform': TransformBuilder
        }

    def _build(self, context: Context) -> BaseComponent:
        config = self._stage.config
        stage_name = config.WhichOneof('config')
        if stage_name in self._stage_builders:
            builder_constructor = self._stage_builders[stage_name]
            args = getattr(config, stage_name)
            builder = builder_constructor(args)
            return builder.build(context)
        else:
            raise ValueError('Unknown stage name {0}'.format(stage_name))

    def build(self, context: Context) -> BaseComponent:
        try:
            return self._build(context)
        except KeyError as e:
            raise KeyError(
                'missing property for config stage `{0}`; {1}'.format(
                    self._stage.config.WhichOneof('config'), str(e)))
