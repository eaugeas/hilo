from tfx.types import artifact, standard_artifacts


PARTITIONS_PROPERTY = artifact.Property(type=artifact.PropertyType.STRING)


class Datasets(artifact.Artifact):
    TYPE_NAME = 'Datasets'


class PartitionedExamples(artifact.Artifact):
    TYPE_NAME = 'Partitions'

    PROPERTIES = {
        'span': standard_artifacts.SPAN_PROPERTY,
        'split_names': standard_artifacts.SPLIT_NAMES_PROPERTY,
        'partitions': PARTITIONS_PROPERTY
    }
