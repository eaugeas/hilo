from typing import Iterable, List, Optional, Text

from tfx.types import artifact


def splits_or_example_defaults(
        split_names: Optional[Iterable[Text]]) -> List[Text]:
    """splits_or_example_defaults returns split_names if the value
    is set, or the default value for example splits"""

    source: Iterable[Text] = split_names or artifact.DEFAULT_EXAMPLE_SPLITS
    return [split_name for split_name in source]
