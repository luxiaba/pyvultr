import logging
from dataclasses import asdict, dataclass
from enum import Enum, unique
from typing import Any, Dict, Optional

import dacite

log = logging.getLogger(__name__)


def merge_args(*args: Optional[Dict]) -> Dict:
    """Merge multi ple dicts into one dict.

    Args:
        *args: Dicts to merge.

    Returns:
        dict: Merged dict.
    """
    return {k: v for d in args if d for k, v in d.items()}


def remove_none(d: Optional[Dict] = None) -> Dict:
    """Remove None value from dict.

    Args:
        d: Dict to remove None value.

    Returns:
        dict: Dict without None value.
    """
    if not d:
        return {}
    return {k: v for k, v in d.items() if v is not None}


def get_only_value(d: Dict) -> Any:
    """Get the value from dict that only has one key.

    Args:
        d: Dict that only has one key.

    Returns:
        Any: Value of the only key.
    """
    values = list(d.values())
    if not values or len(values) != 1:
        return None
    return values[0]


@unique
class Enums(Enum):
    ...


@dataclass
class BaseDataclass:
    def to_dict(self):
        """Convert dataclass to dict.

        Returns:
            Dict: Python dict representation of the object.
        """
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict) -> "BaseDataclass":
        """Convert dict to dataclass.

        Args:
            data: a dict that convert to dataclass

        Returns:
            BaseDataclass:
        """
        return dacite.from_dict(data_class=cls, data=data)
