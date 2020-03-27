from tfx.components import SchemaGen
from tfx.components.base.base_component import BaseComponent

from hilo_stage.components import (
    JsonExampleGen, SingleDimensionGen, StatisticsGen)
from hilo_rpc.proto.stage_pb2 import Stage as StageDescriptor


class Stage:
    def __init__(self, descriptor: StageDescriptor):
        self._descriptor = descriptor

    @property
    def descriptor(self) -> StageDescriptor:
        return self._descriptor

    @staticmethod
    def _build_stage_by_class_name(name, **kwargs) -> BaseComponent:
        # TODO(eaugeas): we may want to filter out the parameters
        # provide in kwargs based on the expected inputs defined
        # in the descriptor
        if name == 'JsonExampleGen':
            return JsonExampleGen(**kwargs)
        elif name == 'StatisticsGen':
            return StatisticsGen(**kwargs)
        elif name == 'SchemaGen':
            return SchemaGen(**kwargs)
        elif name == 'SingleDimensionGen':
            return SingleDimensionGen(**kwargs)
        else:
            raise ValueError('Unknown stage class_name {0}'.format(name))

    def build(self, **kwargs) -> BaseComponent:
        if self._descriptor.config.url.WhichOneof('url') == 'class_name':
            return Stage._build_stage_by_class_name(
                self._descriptor.config.url.class_name, **kwargs)
        elif self._descriptor.config.url.WhichOneof('url') == 'full_path':
            raise ValueError('Unsupported specification of stage by full_path')
        else:
            raise ValueError('Unknown url value {0}'.format(
                self._descriptor.config.url.WhichOneof('url')))
