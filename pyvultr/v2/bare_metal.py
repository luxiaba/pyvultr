from dataclasses import dataclass
from functools import partial
from typing import Dict, List, Optional
from urllib.parse import urljoin

import dacite

from pyvultr.utils import BaseDataclass, VultrPagination, get_only_value, merge_args
from pyvultr.v2.base import BaseVultrV2
from pyvultr.v2.enum import BareMetalUpgradeType


@dataclass
class BareMetalItem(BaseDataclass):
    id: str
    os: str
    ram: str
    disk: str
    main_ip: str
    cpu_count: int
    region: str
    default_password: str
    date_created: str
    status: str
    netmask_v4: str
    gateway_v4: str
    plan: str
    label: str
    tag: str
    os_id: int
    app_id: int
    image_id: str
    v6_network: str
    v6_main_ip: str
    v6_network_size: int
    mac_address: int


@dataclass
class BareMetalIPV4Item(BaseDataclass):
    ip: str
    netmask: str
    gateway: str
    type: str
    reverse: str
    mac_address: str


@dataclass
class BareMetalIPV6Item(BaseDataclass):
    ip: str
    netmask: str
    network_size: int
    type: str


@dataclass
class BareMetalBandwidthItem(BaseDataclass):
    incoming_bytes: int
    outgoing_bytes: int


@dataclass
class BareMetalUserData(BaseDataclass):
    data: str


@dataclass
class BareMetalAvailableUpgrade(BaseDataclass):
    applications: List
    os: List


@dataclass
class BareMetalVNC(BaseDataclass):
    url: str


class BareMetal(BaseVultrV2):
    """Vultr BareMetal API.

    Bare Metal servers give you access to the underlying physical
    hardware in a single-tenant environment without a virtualization layer.

    Attributes:
        api_key: Vultr API key, we get it from env variable `VULTR_API_TOKEN` if not provided.
    """

    def __init__(self, api_key: Optional[str] = None):
        super().__init__(api_key)

    @property
    def base_url(self):
        """Get base url for all API in this section."""
        return urljoin(super().base_url, "bare-metals")

    def list(self, per_page: int = None, cursor: str = None, capacity: int = None) -> VultrPagination[BareMetalItem]:
        """List all Bare Metal instances in your account.

        Args:
            per_page: Number of items requested per page. Default is 100 and Max is 500.
            cursor: Cursor for paging.
            capacity: the capacity of the VultrPagination[BareMetalItem],
            see `pyvultr.utils.VultrPagination` for detail.

        Returns:
            VultrPagination[BareMetalItem]: a paginated list of `BareMetalItem`.
        """
        return VultrPagination[BareMetalItem](
            fetcher=self._get,
            cursor=cursor,
            page_size=per_page,
            return_type=BareMetalItem,
            capacity=capacity,
        )

    def create(self, region: str, plan: str, **kwargs) -> BareMetalItem:
        """Create a new Bare Metal instance in a region with the desired plan.

        Choose one of the following to deploy the instance:
            - os_id
            - snapshot_id
            - app_id
            - image_id
        Supply other attributes as desired.

        Args:
            region: The Region id to create the instance.
            plan: The Bare Metal plan id to use for this instance.
            **kwargs: Other attributes to create the BareMetal.

        Returns:
            BareMetalItem: A `BareMetalItem` object.
        """
        # instance kwargs: see [Vultr Create Instance](https://www.vultr.com/api/#operation/create-instance)
        fixed_args = {
            "region": region,
            "plan": plan,
        }
        resp = self._post(json=merge_args(kwargs, fixed_args))
        return dacite.from_dict(data_class=BareMetalItem, data=get_only_value(resp))

    def get(self, bare_metal_id: str) -> BareMetalItem:
        """Get information for a Bare Metal instance.

        Args:
            bare_metal_id: The Bare Metal instance id.

        Returns:
            BareMetalItem: A `BareMetalItem` object.
        """
        resp = self._get(f"/{bare_metal_id}")
        return dacite.from_dict(data_class=BareMetalItem, data=get_only_value(resp))

    def update(self, bare_metal_id: str, **kwargs) -> BareMetalItem:
        """Update a Bare Metal instance.

        All attributes are optional. If not set, the attributes will retain their original values.
        Note: Changing `os_id`, `app_id` or `image_id` may take a few extra seconds to complete.

        Args:
            bare_metal_id: The Bare Metal instance id.
            **kwargs: Other attributes to update the BareMetal.

        Returns:
            BareMetalItem: A `BareMetalItem` object.
        """
        resp = self._patch(f"/{bare_metal_id}", json=kwargs)
        return dacite.from_dict(data_class=BareMetalItem, data=get_only_value(resp))

    def delete(self, bare_metal_id: str):
        """Delete a Bare Metal instance.

        Args:
            bare_metal_id: The Bare Metal instance id.

        Returns:
            STATUS CODE: 204
            /NO CONTENT/
        """
        return self._delete(f"/{bare_metal_id}")

    def list_ipv4s(
        self,
        bare_metal_id: str,
        per_page: int = None,
        cursor: str = None,
        capacity: int = None,
    ) -> VultrPagination[BareMetalIPV4Item]:
        """Get the IPv4 information for the Bare Metal instance.

        Args:
            bare_metal_id: The Bare Metal instance id.
            per_page: Number of items requested per page. Default is 100 and Max is 500.
            cursor: Cursor for paging.
            capacity: the capacity of the VultrPagination[BareMetalIPV4Item],
            see `pyvultr.utils.VultrPagination` for detail.

        Returns:
            VultrPagination[BareMetalIPV4Item]: a paginated list of `BareMetalIPV4Item`.
        """
        fetcher = partial(self._get, endpoint=f"/{bare_metal_id}/ipv4")
        return VultrPagination[BareMetalIPV4Item](
            fetcher=fetcher,
            cursor=cursor,
            page_size=per_page,
            return_type=BareMetalIPV4Item,
            capacity=capacity,
        )

    def list_ipv6s(
        self,
        bare_metal_id: str,
        per_page: int = None,
        cursor: str = None,
        capacity: int = None,
    ) -> VultrPagination[BareMetalIPV6Item]:
        """Get the IPv6 information for the Bare Metal instance.

        Args:
            bare_metal_id: The Bare Metal instance id.
            per_page: Number of items requested per page. Default is 100 and Max is 500.
            cursor: Cursor for paging.
            capacity: the capacity of the VultrPagination[BareMetalIPV6Item],
            see `pyvultr.utils.VultrPagination` for detail.

        Returns:
            VultrPagination[BareMetalIPV6Item]: a paginated list of `BareMetalIPV6Item`.
        """
        fetcher = partial(self._get, endpoint=f"/{bare_metal_id}/ipv6")
        return VultrPagination[BareMetalIPV6Item](
            fetcher=fetcher,
            cursor=cursor,
            page_size=per_page,
            return_type=BareMetalIPV6Item,
            capacity=capacity,
        )

    def get_bandwidth(self, bare_metal_id: str) -> Dict[str, BareMetalBandwidthItem]:
        """Get bandwidth information for the Bare Metal instance.

        The `bandwidth` object in a successful response contains objects representing a day in the month.
        The date is denoted by the nested object keys. Days begin and end in the UTC timezone.
        Bandwidth utilization data contained within the date object is refreshed periodically.
        We do not recommend using this endpoint to gather real-time metrics.

        Args:
            bare_metal_id: The Bare Metal instance id.

        Returns:
            Dict[str, BareMetalBandwidthItem]: This object will contain objects that represent days in the month (UTC).
            The date is denoted by the nested objects keys.
        """
        _resp: Dict = self._get(f"/{bare_metal_id}/bandwidth")
        resp = get_only_value(_resp)
        return {_date: dacite.from_dict(data_class=BareMetalBandwidthItem, data=item) for _date, item in resp.items()}

    def start(self, bare_metal_id: str):
        """Start the Bare Metal instance.

        Args:
            bare_metal_id: The Bare Metal instance id.

        Returns:
            STATUS CODE: 204
            /NO CONTENT/
        """
        return self._post(f"/{bare_metal_id}/start")

    def reboot(self, bare_metal_id: str):
        """Reboot the Bare Metal instance.

        Args:
            bare_metal_id: The Bare Metal instance id.

        Returns:
            STATUS CODE: 204
            /NO CONTENT/
        """
        return self._post(f"/{bare_metal_id}/reboot")

    def halt(self, bare_metal_id: str):
        """Halt the Bare Metal instance.

        Args:
            bare_metal_id: The Bare Metal instance id.

        Returns:
            STATUS CODE: 204
            /NO CONTENT/
        """
        return self._post(f"/{bare_metal_id}/halt")

    def reinstall(self, bare_metal_id: str):
        """Reinstall the Bare Metal instance.

        Note: This action may take a few extra seconds to complete.

        Args:
            bare_metal_id: The Bare Metal instance id.

        Returns:
            STATUS CODE: 204
            /NO CONTENT/
        """
        return self._post(f"/{bare_metal_id}/reinstall")

    def batch_start(self, bare_metal_ids: List[str]):
        """Start Bare Metals.

        Args:
            bare_metal_ids: A list of Bare Metal instance ids.

        Returns:
            STATUS CODE: 204
            /NO CONTENT/
        """
        _json = {
            "baremetal_ids": bare_metal_ids,
        }
        return self._post("/start", json=_json)

    def batch_reboot(self, bare_metal_ids: List[str]):
        """Reboot Bare Metals.

        Args:
            bare_metal_ids: A list of Bare Metal instance ids.

        Returns:
            STATUS CODE: 204
            /NO CONTENT/
        """
        _json = {
            "baremetal_ids": bare_metal_ids,
        }
        return self._post("/reboot", json=_json)

    def batch_halt(self, bare_metal_ids: List[str]):
        """Halt Bare Metals.

        Args:
            bare_metal_ids: A list of Bare Metal instance ids.

        Returns:
            STATUS CODE: 204
            /NO CONTENT/
        """
        _json = {
            "baremetal_ids": bare_metal_ids,
        }
        return self._post("/halt", json=_json)

    def get_user_data(self, bare_metal_id: str) -> BareMetalUserData:
        """Get the user-supplied, base64 encoded user data for a Bare Metal.

        Args:
            bare_metal_id: The Bare Metal instance id.

        Returns:
            BareMetalUserData: A `BareMetalUserData` object.
        """
        resp = self._get(f"/{bare_metal_id}/user-data")
        return dacite.from_dict(data_class=BareMetalUserData, data=get_only_value(resp))

    def list_upgrades(self, bare_metal_id: str, upgrade_type: BareMetalUpgradeType = None) -> BareMetalAvailableUpgrade:
        """Get available upgrades for a Bare Metal.

        Args:
            bare_metal_id: The Bare Metal instance id.
            upgrade_type: Filter upgrade by type.

        Returns:
            BareMetalAvailableUpgrade: A `BareMetalAvailableUpgrade` object.
        """
        _params = {
            "type": upgrade_type and upgrade_type.value,
        }
        resp = self._get(f"/{bare_metal_id}/upgrades", params=_params)
        return dacite.from_dict(data_class=BareMetalAvailableUpgrade, data=get_only_value(resp))

    def get_vnc(self, bare_metal_id: str) -> BareMetalVNC:
        """Get the VNC URL for a Bare Metal.

        Args:
            bare_metal_id: The Bare Metal instance id.

        Returns:
            BareMetalVNC: A `BareMetalVNC` object.
        """
        resp = self._get(f"/{bare_metal_id}/vnc")
        return dacite.from_dict(data_class=BareMetalVNC, data=get_only_value(resp))
