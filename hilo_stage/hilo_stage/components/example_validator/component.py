# Lint as: python2, python3
# Copyright 2019 Google LLC. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""TFX ExampleValidator component definition."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging
from typing import Optional, Text

from tfx import types
from tfx.components.base import base_component
from tfx.components.base import executor_spec
from tfx.types import standard_artifacts
from tfx.types.standard_component_specs import ExampleValidatorSpec

from hilo_stage.components.example_validator.executor import Executor


class ExampleValidator(base_component.BaseComponent):
    SPEC_CLASS = ExampleValidatorSpec
    EXECUTOR_SPEC = executor_spec.ExecutorClassSpec(Executor)

    def __init__(self,
                 statistics: types.Channel = None,
                 schema: types.Channel = None,
                 output: Optional[types.Channel] = None,
                 stats: Optional[types.Channel] = None,
                 instance_name: Optional[Text] = None):
        """An ExampleValidator component for examples.

     TFX has its ExampleValidator component, and this one uses the same
     executor. The reason for this one to exist, is that the TFX
     component does not allow to specify the splits to use, it just
     assumes `train` and `eval`. This component will be unnecessary
     once TFX Transform allows to set the input and output splits
     as other components do"""

        if stats:
            logging.warning(
                'The "stats" argument to the StatisticsGen component has '
                'been renamed to "statistics" and is deprecated. Please update'
                ' your usage as support for this argument will be removed'
                ' soon.')
            statistics = stats
        anomalies = output or types.Channel(
            type=standard_artifacts.ExampleAnomalies,
            artifacts=[standard_artifacts.ExampleAnomalies()])
        spec = ExampleValidatorSpec(statistics=statistics,
                                    schema=schema,
                                    anomalies=anomalies)
        super(ExampleValidator, self).__init__(spec=spec,
                                               instance_name=instance_name)
