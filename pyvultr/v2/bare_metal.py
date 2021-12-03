import logging
from dataclasses import dataclass
from functools import partial
from typing import Dict, List, Optional
from urllib.parse import urljoin

from pyvultr.utils import BaseDataclass, VultrPagination, get_only_value

from .base import BaseVultrV2, command
from .enums import BareMetalUpgradeType
from .instance import BandwidthItem, IPv4Item, IPv6Item, UserData

log = logging.getLogger(__name__)


@dataclass
class ReqBareMetal(BaseDataclass):
    # [REQUIRED]
    region: str  # The Region id(see `RegionAPI.list`) to create the instance.
    plan: str  # The Bare Metal plan id(see `PlanAPI.list_bare_metal`) to use for this instance.

    # [CHOOSE_ONE] Please choose one source to create instance
    os_id: int = None  # Use OS to deployment
    snapshot_id: str = None  # Use Snapshot to deployment.
    app_id: int = None  # Use application to deployment.
    image_id: str = None  # Use image to deployment.

    # [OPTIONAl]
    script_id: str = None  # The Startup Script id(create in advance) to use for this instance.
    enable_ipv6: bool = None  # Enable IPv6.
    sshkey_id: List[str] = None  # The SSH Key id(create in advance) to install on this instance.
    user_data: str = None  # The user-supplied, base64 encoded user data for this Instance.
    label: str = None  # Set label for this instance.
    activation_email: bool = None  # Notify by email after deployment, default is false.
    hostname: str = None  # Set hostname for this instance.
    tag: str = None  # Set tag for this instance.
    reserved_ipv4: str = None  # Set a Reserved IP id for this instance.
    persistent_pxe: bool = None

    @property
    def valid_basic(self) -> bool:
        """Region and plan are required."""
        return all((self.region, self.plan))

    @property
    def valid_source(self) -> bool:
        """Check whether the data meets the conditions for bare metal instance creation."""
        return any((self.os_id, self.snapshot_id, self.app_id, self.image_id))


@dataclass
class BareMetal(BaseDataclass):
    id: str  # A unique ID for the BareMetal.
    os: str  # The Operating System name, check OperatingSystemAPI.list and `OSItem.name` for available OSes.
    ram: str  # Text description of the BareMetal instance's RAM.
    disk: str  # Text description of the BareMetal instances' disk configuration.
    main_ip: str  # The main IPv4 address.
    cpu_count: int  # Number of CPUs.
    # The Region id where the instance is located, check `RegionAPI.list` and `RegionItem.id` for available regions.
    region: str
    date_created: str  # The date this BareMetal instance was created.
    status: str  # The status of the BareMetal instance, check `enums.BareMetalStatus` for details.
    netmask_v4: str  # The IPv4 netmask in dot-decimal notation.
    gateway_v4: str  # The IPv4 gateway in dot-decimal notation.
    # The plan id of the instance, check `Plan.list_bare_metal` and `BareMetalPlanItem.id` for available plans.
    plan: str
    label: str  # The user-supplied label for this BareMetal instance.
    tag: str  # The user-supplied tag for this BareMetal instance.
    os_id: int  # The Operating System id, check OperatingSystemAPI.list and `OSItem.id` for available OSes.
    app_id: int  # The Application id, check `Application.list` and `ApplicationItem.id` for available options.
    # The Application image_id, check `Application.list` and `ApplicationItem.image_id` for available options.
    image_id: str
    v6_network: str  # The IPv6 network size in bits.
    v6_main_ip: str  # The main IPv6 network address.
    v6_network_size: int  # The IPv6 subnet.
    mac_address: int  # The MAC address for a Bare Metal server
    default_password: str = None  # The default password assigned at deployment.


@dataclass
class BareMetalAvailableUpgrade(BaseDataclass):
    applications: List  # Available application upgrades, list of any.
    os: List  # Available os upgrades, list of any.


@dataclass
class BareMetalVNC(BaseDataclass):
    url: str  # VNC URL.


class BareMetalAPI(BaseVultrV2):
    """Vultr BareMetal API.

    Reference: https://www.vultr.com/api/#tag/baremetal

    Bare Metal servers give you access to the underlying physical
    hardware in a single-tenant environment without a virtualization layer.

    Attributes:
        api_key: Vultr API key, we get it from env variable `$VULTR_API_KEY` if not provided.
    """

    def __init__(self, api_key: Optional[str] = None):
        super().__init__(api_key)

    @property
    def base_url(self):
        """Get base url for all API in this section."""
        return urljoin(super().base_url, "bare-metals")

    @command
    def list(self, per_page: int = None, cursor: str = None, capacity: int = None) -> VultrPagination[BareMetal]:
        """List all Bare Metal instances in your account.

        Args:
            per_page: Number of items requested per page. Default is 100 and Max is 500.
            cursor: Cursor for paging.
            capacity: The capacity of the VultrPagination[BareMetalItem], see `VultrPagination` for details.

        Returns:
            VultrPagination[BareMetal]: A list-like object of `BareMetalItem` object.
        """
        return VultrPagination[BareMetal](
            fetcher=self._get,
            cursor=cursor,
            page_size=per_page,
            return_type=BareMetal,
            capacity=capacity,
        )

    @command
    def create(self, bare_metal: ReqBareMetal) -> Optional[BareMetal]:
        """Create a new Bare Metal instance in a region with the desired plan.

        Choose one of the following to deploy the instance:
            - os_id
            - snapshot_id
            - app_id
            - image_id
        Supply other attributes as desired.

        Args:
            bare_metal: A ReqBareMetal object to create a Bare Metal instance.

        Returns:
            BareMetal: A `BareMetalItem` object.
        """
        # instance kwargs: see [Vultr Create Instance](https://www.vultr.com/api/#operation/create-instance)
        if not bare_metal.valid_basic:
            log.error(f"Invalid bare_metal: {bare_metal}, `Region` and `Plan` is required.")
            return
        if not bare_metal.valid_source:
            log.error(
                f"Invalid bare_metal: {bare_metal}, "
                f"Please provide at least one: `os_id`, `image_id`, `snapshot_id`, `app_id`."
            )
            return

        resp = self._post(json=bare_metal.to_dict())
        return BareMetal.from_dict(get_only_value(resp))

    @command
    def get(self, bare_metal_id: str) -> BareMetal:
        """Get information for a Bare Metal instance.

        Args:
            bare_metal_id: The Bare Metal instance id.

        Returns:
            BareMetal: A `BareMetalItem` object.
        """
        resp = self._get(f"/{bare_metal_id}")
        return BareMetal.from_dict(get_only_value(resp))

    @command
    def update(
        self,
        bare_metal_id: str,
        user_data: str = None,
        label: str = None,
        tag: str = None,
        os_id: int = None,
        app_id: int = None,
        image_id: str = None,
        enable_ipv6: bool = None,
    ) -> BareMetal:
        """Update a Bare Metal instance.

        All attributes are optional. If not set, the attributes will retain their original values.
        Note: Changing `os_id`, `app_id` or `image_id` may take a few extra seconds to complete.

        Args:
            bare_metal_id: The Bare Metal instance id.
            user_data: The user-supplied, base64 encoded user data to attach to this instance.
            label: The user-supplied label.
            tag: The user-supplied tag.
            os_id: If supplied, reinstall the instance using this Operating System id.
            app_id: If supplied, reinstall the instance using this Application id.
            image_id: If supplied, reinstall the instance using this Application image_id.
            enable_ipv6: Enable IPv6.

        Returns:
            BareMetal: A `BareMetalItem` object.
        """
        update_args = {
            "user_data": user_data,
            "label": label,
            "tag": tag,
            "os_id": os_id,
            "app_id": app_id,
            "image_id": image_id,
            "enable_ipv6": enable_ipv6,
        }
        resp = self._patch(f"/{bare_metal_id}", json=update_args)
        return BareMetal.from_dict(get_only_value(resp))

    @command
    def delete(self, bare_metal_id: str):
        """Delete a Bare Metal instance.

        Args:
            bare_metal_id: The Bare Metal instance id.

        Returns:
            STATUS CODE: 204
            /NO CONTENT/
        """
        return self._delete(f"/{bare_metal_id}")

    @command
    def list_ipv4s(
        self,
        bare_metal_id: str,
        per_page: int = None,
        cursor: str = None,
        capacity: int = None,
    ) -> VultrPagination[IPv4Item]:
        """Get the IPv4 information for the Bare Metal instance.

        Args:
            bare_metal_id: The Bare Metal instance id.
            per_page: Number of items requested per page. Default is 100 and Max is 500.
            cursor: Cursor for paging.
            capacity: The capacity of the VultrPagination[IPV4Item], see `VultrPagination` for details.

        Returns:
            VultrPagination[IPv4Item]: A list-like object of `IPV4Item` object.
        """
        fetcher = partial(self._get, endpoint=f"/{bare_metal_id}/ipv4")
        return VultrPagination[IPv4Item](
            fetcher=fetcher,
            cursor=cursor,
            page_size=per_page,
            return_type=IPv4Item,
            capacity=capacity,
        )

    @command
    def list_ipv6s(
        self,
        bare_metal_id: str,
        per_page: int = None,
        cursor: str = None,
        capacity: int = None,
    ) -> VultrPagination[IPv6Item]:
        """Get the IPv6 information for the Bare Metal instance.

        Args:
            bare_metal_id: The Bare Metal instance id.
            per_page: Number of items requested per page. Default is 100 and Max is 500.
            cursor: Cursor for paging.
            capacity: The capacity of the VultrPagination[IPv6Item], see `VultrPagination` for details.

        Returns:
            VultrPagination[IPv6Item]: A list-like object of `IPv6Item` object.
        """
        fetcher = partial(self._get, endpoint=f"/{bare_metal_id}/ipv6")
        return VultrPagination[IPv6Item](
            fetcher=fetcher,
            cursor=cursor,
            page_size=per_page,
            return_type=IPv6Item,
            capacity=capacity,
        )

    @command
    def get_bandwidth(self, bare_metal_id: str) -> Dict[str, BandwidthItem]:
        """Get bandwidth information for the Bare Metal instance.

        The `bandwidth` object in a successful response contains objects representing a day in the month.
        The date is denoted by the nested object keys. Days begin and end in the UTC timezone.
        Bandwidth utilization data contained within the date object is refreshed periodically.
        We do not recommend using this endpoint to gather real-time metrics.

        Args:
            bare_metal_id: The Bare Metal instance id.

        Returns:
            Dict[str, BandwidthItem]: This object will contain objects that represent days in the month (UTC).
            The date is denoted by the nested objects keys.
        """
        _resp: Dict = self._get(f"/{bare_metal_id}/bandwidth")
        resp = get_only_value(_resp)
        return {_date: BandwidthItem.from_dict(item) for _date, item in resp.items()}

    @command
    def start(self, bare_metal_id: str):
        """Start the Bare Metal instance.

        Args:
            bare_metal_id: The Bare Metal instance id.

        Returns:
            STATUS CODE: 204
            /NO CONTENT/
        """
        return self._post(f"/{bare_metal_id}/start")

    @command
    def reboot(self, bare_metal_id: str):
        """Reboot the Bare Metal instance.

        Args:
            bare_metal_id: The Bare Metal instance id.

        Returns:
            STATUS CODE: 204
            /NO CONTENT/
        """
        return self._post(f"/{bare_metal_id}/reboot")

    @command
    def halt(self, bare_metal_id: str):
        """Halt the Bare Metal instance.

        Args:
            bare_metal_id: The Bare Metal instance id.

        Returns:
            STATUS CODE: 204
            /NO CONTENT/
        """
        return self._post(f"/{bare_metal_id}/halt")

    @command
    def reinstall(self, bare_metal_id: str) -> BareMetal:
        """Reinstall the Bare Metal instance.

        Note: This action may take a few extra seconds to complete.

        Args:
            bare_metal_id: The Bare Metal instance id.

        Returns:
            STATUS CODE: 204
            /NO CONTENT/
        """
        resp = self._post(f"/{bare_metal_id}/reinstall")
        return BareMetal.from_dict(get_only_value(resp))

    @command
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

    @command
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

    @command
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

    @command
    def get_user_data(self, bare_metal_id: str) -> UserData:
        """Get the user-supplied, base64 encoded user data for a Bare Metal.

        Args:
            bare_metal_id: The Bare Metal instance id.

        Returns:
            UserData: A `UserData` object.
        """
        resp = self._get(f"/{bare_metal_id}/user-data")
        return UserData.from_dict(get_only_value(resp))

    @command
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
        return BareMetalAvailableUpgrade.from_dict(get_only_value(resp))

    @command
    def get_vnc(self, bare_metal_id: str) -> BareMetalVNC:
        """Get the VNC URL for a Bare Metal.

        Args:
            bare_metal_id: The Bare Metal instance id.

        Returns:
            BareMetalVNC: A `BareMetalVNC` object.
        """
        resp = self._get(f"/{bare_metal_id}/vnc")
        return BareMetalVNC.from_dict(get_only_value(resp))
