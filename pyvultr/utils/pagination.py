import sys
from dataclasses import dataclass, is_dataclass
from typing import Any, Callable, Dict, Generic, List, Optional, TypeVar

import dacite

from pyvultr.exception import NoMorePageDataException, OutOfRangePageDataException, UnexpectedPageDataException

from .box import BaseDataclass, Enums, get_only_value, remove_none


class PaginationFetchState(Enums):
    NeverFetch = "NeverFetch"
    FetchAble = "FetchAble"
    NoMoreData = "NoMoreData"


@dataclass
class PageMetaLink(BaseDataclass):
    next: str = ""
    prev: str = ""


@dataclass
class PageMeta(BaseDataclass):
    links: PageMetaLink
    total: int


T = TypeVar("T")


class VultrPagination(Generic[T], list):
    """Vultr Pagination API Handler.

    Interface for handling paging type, hiding paging details and providing list like objects to the outside.
    which can be used as a list type, such as slice/index/iterate.
    - Fetch only when you need more data.
    - Automatically strip dict data that only has one key.
    """

    def __init__(
        self,
        fetcher: Callable[..., Dict],
        cursor: str = None,
        page_size: int = None,
        return_type: T = None,
        capacity: int = None,
        **params: Dict[str, Any],
    ):
        super().__init__()
        self.fetcher: Callable[..., Dict] = fetcher
        self.cursor: str = cursor
        self.page_size: int = page_size
        self.return_type = return_type
        self.extra_params = params
        self.data: List[T] = []
        self.__idx = 0
        self.__total = None
        self.state: PaginationFetchState = PaginationFetchState.NeverFetch
        self.capacity: int = capacity
        self.check_prefetch(self.capacity)

    def __repr__(self):
        """Return the string representation of the object."""
        return f"<{self.__class__.__name__} {len(self)} items, state: {self.state.value}>"

    def __len__(self):
        """Return the length of the object."""
        return len(self.data)

    def __iter__(self) -> "VultrPagination":
        """Return the iterator of the object."""
        return self

    def __next__(self) -> T:
        """Return the next value of the object."""
        try:
            value = self[self.__idx]
            self.__idx += 1
            return value
        except IndexError:
            self.__idx = 0
            raise StopIteration()

    def __getitem__(self, key) -> T:
        """Get data by index."""
        if self.capacity is not None:
            return self.data[key]

        if isinstance(key, int):
            try:
                return self.get_by_idx(key)
            except OutOfRangePageDataException:
                raise IndexError
        elif isinstance(key, slice):
            try:
                self.get_by_slice(key)
            except OutOfRangePageDataException:
                ...
            return self.data[key]
        else:
            raise TypeError(f"{key} is not int or slice")

    def first(self) -> T:
        """Get the first value of the object."""
        try:
            return self.get_by_idx(0)
        except OutOfRangePageDataException:
            return None

    def check_prefetch(self, cnt: int = None) -> T:
        """Check if we need to prefetch data."""
        if cnt and cnt > 0:
            return self.get_by_idx(cnt - 1)

    @staticmethod
    def calc_max_idx_we_need(seg: slice) -> Optional[int]:
        """Calc the max index we need from the slice.

        Args:
            seg: Python slice.

        Returns:
            Optional[int]: The max index we need. if the slice is invalid, return None.
        """
        sys_max_ids = sys.maxsize

        # default slice value
        _start, _stop, _step = seg.start, seg.stop, seg.step
        _start = 0 if _start is None else _start
        _stop = sys_max_ids if _stop is None else _stop
        _step = 1 if _step is None else _step

        # invalid slice, don't fetch any data to slice
        #   1. departure same with destination.
        #   2. destination and step direction are different.
        if (_stop - _start) * _step <= 0:
            return None

        # counting from tail, we need to fetch all data
        if _start < 0 or _stop < 0:
            return sys_max_ids
        return max(_start, _stop - 1)

    def get_by_slice(self, seg) -> T:
        """Get data by slice.

        Args:
            seg: Python slice.

        Returns:
            T: The value in the self.data.
        """
        max_idx_we_need = self.calc_max_idx_we_need(seg)
        if max_idx_we_need is None:
            return
        return self.get_by_idx(max_idx_we_need)

    def get_by_idx(self, idx: int) -> T:
        """Get data by index."""
        if self.data:
            if idx < len(self.data):
                return self.data[idx]
            if self.capacity is not None:
                raise OutOfRangePageDataException()

        try:
            self.fetch()
        except NoMorePageDataException:
            self.state = PaginationFetchState.NoMoreData
            raise OutOfRangePageDataException()

        return self.get_by_idx(idx)

    @property
    def params(self) -> Dict:
        """Get params for fetching data."""
        return remove_none(
            {
                **self.extra_params,
                "per_page": self.page_size,
                "cursor": self.cursor,
            }
        )

    def fetch(self) -> List[T]:
        """Fetch Data.

        Use fetcher to fetch data from Vultr pagination API.

        Returns:
            List[T]: A list of data with except type.

        Raises:
            NoMorePageDataException: No more data to fetch.
            UnexpectedPageDataException: The interface did not return the expected data structure.
        """
        # no cursor back during previous fetch, means no more data
        if self.cursor == "":
            raise NoMorePageDataException()

        raw_data: Dict = self.fetcher(params=self.params)
        self.state = PaginationFetchState.FetchAble
        page_meta = raw_data.pop("meta", None)
        if not page_meta:
            raise UnexpectedPageDataException()
        _data = get_only_value(raw_data)
        if _data is None:
            raise UnexpectedPageDataException()
        if len(_data) <= 0:
            raise NoMorePageDataException()

        if is_dataclass(self.return_type):
            _data = [dacite.from_dict(data_class=self.return_type, data=i) for i in _data]

        meta: PageMeta = PageMeta.from_dict(page_meta)
        self.cursor = meta.links.next or ""  # in case return null
        self.__total = meta.total
        should_end_at = None if self.capacity is None else max(self.capacity - len(self.data), 0)
        self.data.extend(_data[:should_end_at])
        return _data
