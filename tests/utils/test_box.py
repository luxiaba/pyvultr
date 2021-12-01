import copy

import pytest

from pyvultr.utils import get_only_value, merge_args, remove_none
from tests.conftest import test_pair

to_merge_args_data = [
    test_pair(input=[{"a": "b"}, {"m": "n"}, {"a": "d"}], expected={"a": "d", "m": "n"}),
    test_pair(input=[{"a": "b"}, {"m": "n"}], expected={"a": "b", "m": "n"}),
    test_pair(input=[{"a": "b"}, None, {"m": "n"}, {}], expected={"a": "b", "m": "n"}),
    test_pair(input=[{}], expected={}),
    test_pair(input=[], expected={}),
    test_pair(input=[None, None, None], expected={}),
]


@pytest.mark.parametrize("test", to_merge_args_data)
def test_merge_args(test: test_pair):
    """Test function `merge_args`."""
    original = copy.deepcopy(test.input)
    merged = merge_args(*test.input)
    assert original == test.input
    assert merged == test.expected


to_remove_none_data = [
    test_pair(input={"b": "", "c": "c"}, expected={"b": "", "c": "c"}),
    test_pair(input={"a": None, "b": "", "c": "c"}, expected={"b": "", "c": "c"}),
    test_pair(input={}, expected={}),
    test_pair(input=None, expected={}),
    test_pair(input={None: "a"}, expected={None: "a"}),
    test_pair(input={None: None}, expected={}),
]


@pytest.mark.parametrize("test", to_remove_none_data)
def test_remove_none(test: test_pair):
    """Test function `remove_none`."""
    original = copy.deepcopy(test.input)
    returned = remove_none(test.input)
    assert original == test.input
    assert returned == test.expected


to_get_only_value_data = [
    test_pair(input={"a": "b"}, expected="b"),
    test_pair(input={"a": "b", "b": "c"}, expected=None),
    test_pair(input={}, expected=None),
    test_pair(input={None: "a"}, expected="a"),
    test_pair(input={None: None}, expected=None),
]


@pytest.mark.parametrize("test", to_get_only_value_data)
def test_get_only_value(test: test_pair):
    """Test function `get_only_value`."""
    original = copy.deepcopy(test.input)
    result = get_only_value(test.input)
    assert original == test.input
    assert result == test.expected
