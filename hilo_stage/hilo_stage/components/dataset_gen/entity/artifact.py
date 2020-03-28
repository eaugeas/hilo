from tfx.types.artifact import Artifact
from tfx.types import standard_artifacts


class ExampleDimensions(Artifact):
    TYPE_NAME = 'ExampleDimensions'

    PROPERTIES = {
        'split_names': standard_artifacts.SPLIT_NAMES_PROPERTY,
    }
