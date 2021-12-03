import json
import logging
from dataclasses import asdict, dataclass, is_dataclass
from datetime import date, datetime
from decimal import Decimal
from enum import Enum, unique
from functools import partial
from typing import Any, Dict, Optional

import dacite
from pygments import formatters, highlight
from pygments.lexers import JsonLexer

log = logging.getLogger(__name__)


def json_default_func(date_fmt="%Y-%m-%d", dt_fmt="%Y-%m-%d %H:%M:%S", decimal_fmt=str):
    """Serialize additional types."""

    def encoder(obj):
        if isinstance(obj, datetime):
            return obj.strftime(dt_fmt)
        elif isinstance(obj, date):
            return obj.strftime(date_fmt)
        elif isinstance(obj, Decimal):
            return decimal_fmt(obj)
        elif isinstance(obj, BaseDataclass):
            return obj.to_dict()
        elif is_dataclass(obj):
            return asdict(obj)
        raise TypeError("%r is not JSON serializable" % obj)

    return encoder


json_dumps = partial(json.dumps, default=json_default_func())


def make_colorful(obj: Any):
    """Make colorful output with pygments."""
    try:
        json_str = json_dumps(obj, indent=4)
        return highlight(json_str, lexer=JsonLexer(), formatter=formatters.TerminalFormatter())
    except Exception as e:
        log.error(f"Error while formatting json: {e}.")
        return str(obj)


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
