from dataclasses import dataclass
from functools import partial
from typing import List, Optional

from pyvultr.utils import BaseDataclass, VultrPagination

from .base import BaseVultrV2
from .enum import RegionType


@dataclass
class PlanItem(BaseDataclass):
    id: str
    vcpu_count: int
    ram: int
    disk: int
    disk_count: int
    bandwidth: int
    monthly_cost: float
    type: str
    locations: List[str]


@dataclass
class BareMetalPlanItem(BaseDataclass):
    id: str
    cpu_count: int
    cpu_model: str
    cpu_threads: int
    ram: int
    disk: int
    bandwidth: int
    locations: List[str]
    type: str
    monthly_cost: float
    disk_count: int


class Plan(BaseVultrV2):
    """Vultr Plan API.

    Reference: https://www.vultr.com/zh/api/#tag/plans

    A Plan is a particular configuration of vCPU, RAM, SSD, and bandwidth to deploy an Instance.
    Not all Plans are available in all Regions.
    You can browse plans in the Customer Portal or get a list of Plans from the API.

    Attributes
        :api_key: Vultr API key, we get it from env variable `$ENV_TOKEN_NAME` if not provided.
    """

    def __init__(self, api_key: Optional[str] = None):
        # set api key
        super().__init__(api_key)

    def list(
        self,
        per_page: int = None,
        cursor: str = None,
        plan_type: RegionType = None,
        os: str = None,
        capacity: int = None,
    ) -> VultrPagination[PlanItem]:
        """Get a list of all VPS plans at Vultr. The list can be filtered by `plan_type`.

        Args:
            per_page: Number of items requested per page. Default is 100 and Max is 500.
            cursor: Cursor for paging.
            plan_type: Filter the results by plan_type.
            os: Filter the results by operating system.
            capacity: The capacity of the VultrPagination[PlanItem], see `VultrPagination` for details.

        Returns:
            VultrPagination[PlanItem]: A list-like object of `PlanItem` object.
        """
        _extra_params = {
            "type": plan_type and plan_type.value,
            "os": os,
        }
        fetcher = partial(self._get, endpoint="/plans")
        return VultrPagination[PlanItem](
            fetcher=fetcher,
            cursor=cursor,
            page_size=per_page,
            return_type=PlanItem,
            capacity=capacity,
            **_extra_params,
        )

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
