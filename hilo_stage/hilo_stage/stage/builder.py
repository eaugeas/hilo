from typing import Any, Dict, List, Optional, Text, Type

from google.protobuf.message import Message
from tfx.types import Channel, standard_artifacts, artifact_utils
from tfx.components.base.base_node import BaseNode

from hilo_stage.components.utils.splits import splits_or_example_defaults
from hilo_rpc.serialize.dict import serialize as serialize_dict
from hilo_rpc.proto.stage_pb2 import (
    Stage, PartitionGenConfig, ExampleValidatorConfig,
    JsonExampleGenConfig, SingleDimensionGenConfig,
    StatisticsGenConfig, SchemaGenConfig,
    CsvExampleGenConfig, TransformConfig,
    TrainerConfig, ResolverNodeConfig, EvaluatorConfig,
    PusherConfig)


class Context:
    def __init__(
            self,
            id: Text,
            stack: Optional[List[Text]] = None,
            parent: Optional['Context'] = None,
    ):
        self._context: Dict[str, Any] = {}
        if parent:
            self._context = parent._context
        self._id = id
        if stack:
            self._stack: List[Text] = [self._id] + stack
        else:
            self._stack = [self._id]

        if self._id in self._context:
            raise ValueError(
                'Created new context for stage with '
                'existing id {0}'.format(self._id))

    @property
    def root_id(self) -> Text:
        return self._stack[-1]

    @property
    def id(self) -> Text:
        return self._id

    def for_stage(self, id: Text) -> 'Context':
        return Context(id, parent=self, stack=self._stack)

    def get_or(self, map_key, default: Optional[Any] = None) -> Optional[Any]:
        return self._context.get(map_key, default)

    def get(self, key: Text, default: Any = None) -> Any:
        print('look for key: ', key, default)
        print('current context: ', self._context)
        if key in self._context:
            print('key found in context', key, self._context[key])
            return self._context[key]

        for id in self._stack:
            map_key = '{0}.{1}'.format(id, key)
            if map_key in self._context:
                print('key found in parent', key, map_key)
                return self._context[map_key]
            else:
                print('key not found in parent', key, map_key)

        if default is not None:
            print('return defulat')
            return default

        raise KeyError(
            'key {0} not found in context. Current keys: {1}'.format(
                key, list(self._context.keys())))

    def get_self(self, key: Text, default: Any = None) -> Any:
        map_key = '{0}.{1}'.format(self._id, key)
        if map_key in self._context:
            return self._context[map_key]
        elif default is not None:
            return default
        else:
            raise KeyError(
                'key {0} for stage {1} missing in context'.format(key, id))

    def put_outputs(self, message: Message, component: BaseNode):
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

    def build(self, context: Context) -> BaseNode:
        raise NotImplementedError()


class EvaluatorBuilder(ComponentBuilder):
    def __init__(self, config: Optional[EvaluatorConfig]):
        super().__init__(config)
        self._config = config or EvaluatorConfig

    def build(self, context: Context) -> BaseNode:
        from tfx.components import Evaluator
        import tensorflow_model_analysis as tfma

        threshold = {
            'binary_accuracy':
                tfma.config.MetricThreshold(
                    value_threshold=tfma.GenericValueThreshold(
                        lower_bound={'value': 0.6}),
                    change_threshold=tfma.GenericChangeThreshold(
                        direction=tfma.MetricDirection.HIGHER_IS_BETTER,
                        absolute={'value': -1e-10}))
                }
        eval_config = tfma.EvalConfig(
            model_specs=[tfma.ModelSpec(signature_name='eval')],
            slicing_specs=[
                tfma.SlicingSpec(),
            ],
            metrics_specs=[tfma.MetricsSpec(thresholds=threshold)])

        component = Evaluator(
            examples=context.get(self._config.inputs.examples),
            model=context.get(self._config.inputs.model),
            baseline_model=context.get(self._config.inputs.baseline_model),
            eval_config=eval_config,
            instance_name=context.id)
        context.put_outputs(self._config.outputs, component)
        return component


class PusherBuilder(ComponentBuilder):
    def __init__(self, config: Optional[PusherConfig] = None):
        super().__init__(config)
        self._config = config or PusherConfig()

    def build(self, context: Context) -> BaseNode:
        from tfx.components import Pusher
        from tfx.proto.pusher_pb2 import PushDestination

        d = self._config.params.destination.filesystem.base_directory
        push_destination = PushDestination(
            filesystem=PushDestination.Filesystem(base_directory=d))

        component = Pusher(
            model=context.get(self._config.inputs.model),
            model_blessing=context.get(self._config.inputs.model_blessing),
            push_destination=push_destination,
            instance_name=context.id
        )

        context.put_outputs(self._config.outputs, component)
        return component


class ExampleValidatorBuilder(ComponentBuilder):
    def __init__(self, config: Optional[ExampleValidatorConfig] = None):
        super().__init__(config)
        self._config = config or ExampleValidatorConfig()

    def build(self, context: Context) -> BaseNode:
        from hilo_stage.components import ExampleValidator

        statistics = context.get(self._config.inputs.statistics)
        schema = context.get(self._config.inputs.schema)
        component = ExampleValidator(
            statistics=statistics,
            schema=schema,
            instance_name=context.id
        )

        context.put_outputs(self._config.outputs, component)
        return component


class ResolverNodeBuilder(ComponentBuilder):
    def __init__(self, config: Optional[ResolverNodeConfig] = None):
        super().__init__(config)
        self._config = config or ResolverNodeConfig()

    def build(self, context: Context) -> BaseNode:
        from tfx.components import ResolverNode
        from tfx.dsl.experimental.latest_blessed_model_resolver import (
            LatestBlessedModelResolver)
        from tfx.types.standard_artifacts import Model, ModelBlessing

        component = ResolverNode(
            instance_name=context.id,
            resolver_class=LatestBlessedModelResolver,
            model=Channel(type=Model),
            model_blessing=Channel(type=ModelBlessing))

        context.put_outputs(self._config.outputs, component)
        return component


class TrainerBuilder(ComponentBuilder):
    def __init__(self, config: Optional[TrainerConfig] = None):
        super().__init__(config)
        self._config = config or TrainerConfig()

    def build(self, context: Context) -> BaseNode:
        from tfx.components import Trainer

        component = Trainer(
            examples=context.get(self._config.inputs.examples),
            schema=context.get(self._config.inputs.schema),
            transform_graph=context.get_or(
                self._config.inputs.transform_graph, None),
            train_args=serialize_dict(self._config.params.train_args),
            eval_args=serialize_dict(self._config.params.eval_args),
            module_file=self._config.params.module_file,
            instance_name=context.id
        )

        context.put_outputs(self._config.outputs, component)
        return component


class SchemaGenBuilder(ComponentBuilder):
    def __init__(self, config: Optional[SchemaGenConfig] = None):
        super().__init__(config)
        self._config = config or SchemaGenConfig()

    def build(self, context: Context) -> BaseNode:
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

    def build(self, context: Context) -> BaseNode:
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

    def build(self, context: Context) -> BaseNode:
        from hilo_stage.components import SingleDimensionGen
        split_names = splits_or_example_defaults(
            self._config.params.split_names)

        statistics = context.get(self._config.inputs.statistics)
        component = SingleDimensionGen(
            statistics=statistics,
            split_names=split_names,
            instance_name=context.id
        )

        context.put_outputs(self._config.outputs, component)
        return component


class PartitionGenBuilder(ComponentBuilder):
    def __init__(self, config: Optional[PartitionGenConfig]):
        super().__init__(config)
        self._config = config or PartitionGenConfig()

    def build(self, context: Context) -> BaseNode:
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

    def build(self, context: Context) -> BaseNode:
        from tfx.components import CsvExampleGen
        from tfx.proto.example_gen_pb2 import Input, Output, SplitConfig

        input_config: Optional[Output] = None
        if (self._config.params.input_config and
                len(self._config.params.input_config.splits) > 0):
            input_splits: List[Dict[str, str]] = [
                {
                    'name': split.name,
                    'pattern': split.pattern,
                } for split in self._config.params.input_config.splits
            ]
            input_config = Input(splits=input_splits)

        output_config: Optional[Output] = None
        if (self._config.params.output_config and
                len(self._config.params.output_config.splits) > 0):
            output_splits: List[Dict[str, str]] = [
                {
                    'name': split.name,
                    'hash_buckets': split.hash_buckets
                } for split in self._config.params.output_config.splits
            ]
            output_config = Output(
                split_config=SplitConfig(splits=output_splits))

        component = CsvExampleGen(
            instance_name=context.id,
            input=context.get(self._config.inputs.input),
            input_config=input_config,
            output_config=output_config)
        context.put_outputs(self._config.outputs, component)
        return component


class TransformBuilder(ComponentBuilder):
    def __init__(self, config: Optional[TransformConfig] = None):
        super().__init__(config)
        self._config = config or TransformConfig()

    def build(self, context: Context) -> BaseNode:
        from hilo_stage.components import Transform

        props = {}

        if not self._config.inputs.examples:
            raise KeyError(
                'transform pipeline requires `examples`'
                ' as one of its inputs')

        props['examples'] = context.get(self._config.inputs.examples)

        if self._config.inputs.schema:
            props['schema'] = context.get(self._config.inputs.schema)

        if not self._config.params.module_file:
            raise KeyError(
                'transform pipeline requires `module_file`'
                ' as one of its params')

        props['module_file'] = self._config.params.module_file
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

    def build(self, context: Context) -> BaseNode:
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
            'transform': TransformBuilder,
            'example_validator': ExampleValidatorBuilder,
            'trainer': TrainerBuilder,
            'resolver_node': ResolverNodeBuilder,
            'evaluator': EvaluatorBuilder,
            'pusher': PusherBuilder,
        }

    def _build(self, context: Context) -> BaseNode:
        config = self._stage.config
        stage_name = config.WhichOneof('config')
        if stage_name in self._stage_builders:
            builder_constructor = self._stage_builders[stage_name]
            args = getattr(config, stage_name)
            builder = builder_constructor(args)
            return builder.build(context)
        else:
            raise ValueError('Unknown stage name {0}'.format(stage_name))

    def build(self, context: Context) -> BaseNode:
        try:
            return self._build(context)
        except KeyError as e:
            raise KeyError(
                'missing property for config stage `{0}`; {1}'.format(
                    self._stage.config.WhichOneof('config'), str(e)))
