from dataclasses import dataclass
from functools import partial
from typing import List, Optional

from pyvultr.utils import BaseDataclass, VultrPagination

from .base import BaseVultrV2, command
from .enums import RegionType


@dataclass
class Plan(BaseDataclass):
    id: str  # A unique ID for the Plan.
    vcpu_count: int  # The number of vCPUs in this Plan.
    ram: int  # The amount of RAM in MB.
    disk: int  # The disk size in GB.
    bandwidth: int  # The monthly bandwidth quota in GB.
    monthly_cost: float  # The monthly cost in US Dollars.
    type: str  # The plan type, see `enums.PlayType` for possible values.
    locations: List[str]  # An array of Regions where this plan is valid for use.
    disk_count: int  # The number of disks that this plan offers.


@dataclass
class BareMetalPlanItem(BaseDataclass):
    id: str  # A unique ID for the Bare Metal Plan.
    cpu_count: int  # The number of CPUs in this Plan.
    cpu_model: str  # The CPU model type for this instance.
    cpu_threads: int  # The numner of supported threads for this instance.
    ram: int  # The amount of RAM in MB.
    disk: int  # The disk size in GB.
    bandwidth: int  # The monthly bandwidth quota in GB.
    locations: List[str]  # An array of Regions where this plan is valid for use.
    type: str  # The plan type., see `enums.BareMetalPlayType` for possible values.
    monthly_cost: float  # The monthly cost in US Dollars.
    disk_count: int  # The number of disks that this plan offers.


class PlanAPI(BaseVultrV2):
    """Vultr Plan API.

    Reference: https://www.vultr.com/api/#tag/plans

    A Plan is a particular configuration of vCPU, RAM, SSD, and bandwidth to deploy an Instance.
    Not all Plans are available in all Regions.
    You can browse plans in the Customer Portal or get a list of Plans from the API.

    Attributes
        :api_key: Vultr API key, we get it from env variable `$VULTR_API_KEY` if not provided.
    """

    def __init__(self, api_key: Optional[str] = None):
        # set api key
        super().__init__(api_key)

    @command
    def list(
        self,
        per_page: int = None,
        cursor: str = None,
        plan_type: RegionType = None,
        os: str = None,
        capacity: int = None,
    ) -> VultrPagination[Plan]:
        """Get a list of all VPS plans at Vultr. The list can be filtered by `plan_type`.

        Args:
            per_page: Number of items requested per page. Default is 100 and Max is 500.
            cursor: Cursor for paging.
            plan_type: Filter the results by plan_type.
            os: Filter the results by operating system.
            capacity: The capacity of the VultrPagination[PlanItem], see `VultrPagination` for details.

        Returns:
            VultrPagination[Plan]: A list-like object of `PlanItem` object.
        """
        _extra_params = {
            "type": plan_type and plan_type.value,
            "os": os,
        }
        fetcher = partial(self._get, endpoint="/plans")
        return VultrPagination[Plan](
            fetcher=fetcher,
            cursor=cursor,
            page_size=per_page,
            return_type=Plan,
            capacity=capacity,
            **_extra_params,
        )

    @command
    def list_bare_metal(
        self,
        per_page: int = None,
        cursor: str = None,
        capacity: int = None,
    ) -> VultrPagination[BareMetalPlanItem]:
        """Get a list of all Bare Metal plans at Vultr.

        Args:
            per_page: number of items requested per page. Default is 100 and Max is 500.
            cursor: cursor for paging.
            capacity: The capacity of the `VultrPagination[BareMetalPlanItem]`, see `VultrPagination` for details.

        Returns:
            VultrPagination[BareMetalPlanItem]: A list-like object of `BareMetalPlanItem` object.
        """
        fetcher = partial(self._get, endpoint="/plans-metal")
        return VultrPagination[BareMetalPlanItem](
            fetcher=fetcher,
            cursor=cursor,
            page_size=per_page,
            return_type=BareMetalPlanItem,
            capacity=capacity,
        )
