from dataclasses import dataclass
from typing import List, Optional
from urllib.parse import urljoin

from pyvultr.utils import BaseDataclass, VultrPagination, get_only_value

from .base import BaseVultrV2, command
from .enums import RegionType


@dataclass
class Region(BaseDataclass):
    id: str  # A unique ID for the Region.
    country: str  # The two-letter country code for this Region.
    options: List[str]  # An array of product features available in this Region, eg: ["ddos_protection"]
    continent: str  # The name of the continent for this Region.
    city: str  # The name of the city for this Region.


class RegionAPI(BaseVultrV2):
    """Vultr Region API.

    Reference: https://www.vultr.com/api/#tag/region

    Instances can be deployed in many Regions on multiple continents.
    Choose any of our worldwide locations to deploy servers near your office or customers for low-latency.

    Attributes:
        api_key: Vultr API key, we get it from env variable `$VULTR_API_KEY` if not provided.
    """

    def __init__(self, api_key: Optional[str] = None):
        super().__init__(api_key)

    @property
    def base_url(self):
        """Get base url for all API in this section."""
        return urljoin(super().base_url, "regions")

    @command
    def list(self, per_page: int = None, cursor: str = None, capacity: int = None) -> VultrPagination[Region]:
        """List all Regions at Vultr.

        Args:
            per_page: Number of items requested per page. Default is 100 and Max is 500.
            cursor: Cursor for paging.
            capacity: The capacity of the VultrPagination[RegionItem], see `VultrPagination` for details.

        Returns:
            VultrPagination[Region]: A list-like object of `RegionItem` object.
        """
        return VultrPagination[Region](
            fetcher=self._get,
            cursor=cursor,
            page_size=per_page,
            return_type=Region,
            capacity=capacity,
        )

    @command
    def list_in_region(self, region: str, region_type: RegionType = None) -> List[str]:
        """Get a list of the available plans in Region `region-id`.

        Not all plans are available in all regions. The list can be filtered by `region_type`.

        Args:
            region: The Region id.
            region_type: Filter the results by type.

        Returns:
            List[str]: a list of plan ids.
        """
        _params = {
            "type": region_type and region_type.value,
        }
        resp = self._get(f"/{region}/availability", params=_params)
        return [i for i in get_only_value(resp)]
