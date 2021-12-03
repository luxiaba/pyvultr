from dataclasses import dataclass
from functools import partial
from typing import Optional

from pyvultr.utils import BaseDataclass, VultrPagination

from .base import BaseVultrV2, command


@dataclass
class OS(BaseDataclass):
    id: int  # The Operating System id.
    name: str  # The Operating System description.
    arch: str  # The Operating System architecture.
    family: str  # The Operating System family.


class OperatingSystemAPI(BaseVultrV2):
    """Vultr OS API.

    Reference: https://www.vultr.com/api/#tag/os

    We have a wide range of operating systems available to deploy server instances.
    You can also upload an ISO or choose from our public ISO library.
    """

    def __init__(self, api_key: Optional[str] = None):
        super().__init__(api_key)

    @command
    def list(self, per_page: int = None, cursor: str = None, capacity: int = None) -> VultrPagination[OS]:
        """List the OS images available for installation at Vultr.

        Args:
            per_page: Number of items requested per page. Default is 100 and Max is 500.
            cursor: Cursor for paging.
            capacity: The capacity of the VultrPagination[OSItem], see `VultrPagination` for details.

        Returns:
            VultrPagination[OS]: A list-like object of `OSItem` object.
        """
        fetcher = partial(self._get, endpoint="/os")
        return VultrPagination[OS](
            fetcher=fetcher,
            cursor=cursor,
            page_size=per_page,
            return_type=OS,
            capacity=capacity,
        )
