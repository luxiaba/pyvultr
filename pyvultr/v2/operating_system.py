from dataclasses import dataclass
from functools import partial
from typing import Optional

from pyvultr.utils import BaseDataclass, VultrPagination

from .base import BaseVultrV2


@dataclass
class OSItem(BaseDataclass):
    id: int
    name: str
    arch: str
    family: str


class OperatingSystem(BaseVultrV2):
    """Vultr OS API.

    Reference: https://www.vultr.com/zh/api/#tag/os

    We have a wide range of operating systems available to deploy server instances.
    You can also upload an ISO or choose from our public ISO library.

    Attributes:
        api_key: Vultr API key, we get it from env variable `$ENV_TOKEN_NAME` if not provided.
    """

    def __init__(self, api_key: Optional[str] = None):
        super().__init__(api_key)

    def list(self, per_page: int = None, cursor: str = None, capacity: int = None) -> VultrPagination[OSItem]:
        """List the OS images available for installation at Vultr.

        Args:
            per_page: Number of items requested per page. Default is 100 and Max is 500.
            cursor: Cursor for paging.
            capacity: The capacity of the VultrPagination[OSItem], see `VultrPagination` for details.

        Returns:
            VultrPagination[OSItem]: A list-like object of `OSItem` object.
        """
        fetcher = partial(self._get, endpoint="/os")
        return VultrPagination[OSItem](
            fetcher=fetcher,
            cursor=cursor,
            page_size=per_page,
            return_type=OSItem,
            capacity=capacity,
        )
