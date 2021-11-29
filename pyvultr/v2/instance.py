from dataclasses import dataclass
from functools import partial
from typing import Dict, List, Optional
from urllib.parse import urljoin

import dacite

from pyvultr.utils import BaseDataclass, VultrPagination, get_only_value, merge_args
from pyvultr.v2.base import BaseVultrV2
from pyvultr.v2.enum import BackupScheduleType, InstanceUpgradeType


@dataclass
class V6NetworkItem(BaseDataclass):
    network: str
    main_ip: str
    network_size: int


@dataclass
class InstanceItem(BaseDataclass):
    id: str
    os: str
    ram: int
    disk: int
    main_ip: str
    vcpu_count: int
    region: str
    plan: str
    date_created: str
    status: str
    allowed_bandwidth: int
    netmask_v4: str
    gateway_v4: str
    power_status: str
    server_status: str
    v6_networks: List[V6NetworkItem]
    v6_main_ip: str
    v6_network_size: str
    label: str
    internal_ip: str
    kvm: str
    hostname: str
    tag: str
    os_id: str
    app_id: int
    image_id: str
    firewall_group_id: str
    features: List[str]
    default_password: str


@dataclass
class BandwidthItem(BaseDataclass):
    incoming_bytes: int
    outgoing_bytes: int


@dataclass
class PrivateNetworkItem(BaseDataclass):
    id: str
    mac_address: str
    ip_address: str


@dataclass
class ISOStatus(BaseDataclass):
    iso_id: str
    state: str


@dataclass
class BackupSchedule(BaseDataclass):
    enabled: bool
    type: str
    next_scheduled_time_utc: str
    hour: int
    dow: int
    dom: int


@dataclass
class RestoreStatus(BaseDataclass):
    restore_type: str
    restore_id: str
    status: str


@dataclass
class IPv4Item(BaseDataclass):
    ip: str
    netmask: str
    gateway: str
    type: str
    reverse: str
    mac_address: str = None


@dataclass
class IPv6Item(BaseDataclass):
    ip: str
    network: str
    network_size: int
    type: str


@dataclass
class IPv6ReverseItem(BaseDataclass):
    reverse: str
    ip: str


@dataclass
class UserData(BaseDataclass):
    data: str


@dataclass
class AvailableUpgrade(BaseDataclass):
    applications: List
    plans: List
    os: List


class Instance(BaseVultrV2):
    """Vultr Instance API.

    Vultr Cloud instances can be deployed with your preferred operating system or pre-installed application in seconds.
    High Frequency Compute instances are powered by high clock speed CPU's and NVMe local storage to power
    your most demanding applications. Dedicated Cloud instances have dedicated CPU, SSD drives, and RAM.

    Attributes:
        api_key: Vultr API key, we get it from env variable `VULTR_API_TOKEN` if not provided.
    """

    def __init__(self, api_key: Optional[str] = None):
        super().__init__(api_key)

    @property
    def base_url(self):
        """Get base url for all API in this section."""
        return urljoin(super().base_url, "instances")

    def list(
        self,
        per_page: int = None,
        cursor: str = None,
        tag: str = None,
        label: str = None,
        main_ip: str = None,
        capacity: int = None,
    ) -> VultrPagination[InstanceItem]:
        """List all Bare Metal instances in your account.

        Args:
            per_page: Number of items requested per page. Default is 100 and Max is 500.
            cursor: Cursor for paging.
            tag: Filter by specific tag.
            label: Filter by label.
            main_ip: Filter by main ip address.
            capacity: the capacity of the VultrPagination[InstanceItem],
            see `pyvultr.utils.VultrPagination` for detail.

        Returns:
            VultrPagination[InstanceItem]: a paginated list of `InstanceItem`.
        """
        _extra_params = {
            "tag": tag,
            "label": label,
            "main_ip": main_ip,
        }
        return VultrPagination[InstanceItem](
            fetcher=self._get,
            cursor=cursor,
            page_size=per_page,
            return_type=InstanceItem,
            capacity=capacity,
            **_extra_params,
        )

    def create(self, region: str, plan: str, **kwargs) -> InstanceItem:
        """Create a new VPS Instance in a region with the desired plan.

        Choose one of the following to deploy the instance:
            - os_id
            - iso_id
            - snapshot_id
            - app_id
            - image_id
        Supply other attributes as desired.

        Args:
            region: The Region id where the Instance is located.
            plan: The Plan id to use when deploying this instance.
            **kwargs: Other attributes to supply when deploying the instance.

        Returns:
            InstanceItem: A `InstanceItem` object.
        """
        _fixed_args = {
            "region": region,
            "plan": plan,
        }
        resp = self._post(json=merge_args(kwargs, _fixed_args))
        return dacite.from_dict(data_class=InstanceItem, data=get_only_value(resp))

    def get(self, instance_id: str) -> InstanceItem:
        """Get information about an Instance.

        Args:
            instance_id: The Instance id.

        Returns:
            InstanceItem: A `InstanceItem` object.
        """
        resp = self._get(f"/{instance_id}")
        return dacite.from_dict(data_class=InstanceItem, data=get_only_value(resp))

    def update(self, instance_id: str, **kwargs) -> InstanceItem:
        """Update information for an Instance.

        All attributes are optional. If not set, the attributes will retain their original values.
        Note: Changing `os_id`, `app_id` or `image_id` may take a few extra seconds to complete.

        Args:
            instance_id: The Instance id.
            **kwargs: Other attributes to update.

        Returns:
            InstanceItem: A `InstanceItem` object.
        """
        resp = self._patch(f"/{instance_id}", json=kwargs)
        return dacite.from_dict(data_class=InstanceItem, data=get_only_value(resp))

    def delete(self, instance_id: str):
        """Delete an Instance.

        Args:
            instance_id: The Instance id.

        Returns:
            STATUS CODE: 204
            /NO CONTENT/
        """
        return self._delete(f"/{instance_id}")

    def batch_halt(self, instance_ids: List[str]):
        """Halt Instances.

        Args:
            instance_ids: The Instance IDs to halt.

        Returns:
            STATUS CODE: 204
            /NO CONTENT/
        """
        _json = {
            "instance_ids": instance_ids,
        }
        return self._post("/halt", json=_json)

    def batch_reboot(self, instance_ids: List[str]):
        """Reboot Instances.

        Args:
            instance_ids: The Instance IDs to reboot.

        Returns:
            STATUS CODE: 204
            /NO CONTENT/
        """
        _json = {
            "instance_ids": instance_ids,
        }
        return self._post("/reboot", json=_json)

    def batch_start(self, instance_ids: List[str]):
        """Start Instances.

        Args:
            instance_ids: The Instance IDs to start.

        Returns:
            STATUS CODE: 204
            /NO CONTENT/
        """
        _json = {
            "instance_ids": instance_ids,
        }
        return self._post("/start", json=_json)

    def start(self, instance_id: str):
        """Start an Instance.

        Args:
            instance_id: The Instance id.

        Returns:
            STATUS CODE: 204
            /NO CONTENT/
        """
        return self._post(f"/{instance_id}/start")

    def reboot(self, instance_id: str):
        """Reboot an Instance.

        Args:
            instance_id: The Instance id.

        Returns:
            STATUS CODE: 204
            /NO CONTENT/
        """
        return self._post(f"/{instance_id}/reboot")

    def reinstall(self, instance_id: str, hostname: str = None) -> InstanceItem:
        """Reinstall an Instance using an optional `hostname`.

        Note: This action may take a few extra seconds to complete.

        Args:
            instance_id: The Instance id.
            hostname: The hostname to use when reinstalling this instance.

        Returns:
            InstanceItem: A `InstanceItem` object.
        """
        _json = {
            "hostname": hostname,
        }
        resp = self._post(f"/{instance_id}/reinstall", json=_json)
        return dacite.from_dict(data_class=InstanceItem, data=get_only_value(resp))

    def get_bandwidth(self, instance_id: str) -> Dict[str, BandwidthItem]:
        """Get bandwidth information about an Instance.

        The bandwidth object in a successful response contains objects representing a day in the month.
        The date is denoted by the nested object keys. Days begin and end in the UTC timezone.
        The bandwidth utilization data contained within the date object is refreshed periodically.
        We do not recommend using this endpoint to gather real-time metrics.

        Args:
            instance_id: The Instance id.

        Returns:
            Dict[str, BandwidthItem]: This object will contain objects that represent days in the month (UTC).
            The date is denoted by the nested objects keys.
        """
        _resp: Dict = self._get(f"/{instance_id}/bandwidth")
        resp = get_only_value(_resp)
        return {_date: dacite.from_dict(data_class=BandwidthItem, data=item) for _date, item in resp.items()}

    def list_neighbors(self, instance_id: str) -> List[str]:
        """Get a list of other instances in the same location as this Instance.

        Args:
            instance_id: The Instance id.

        Returns:
            List[str]: An array of Instance ids in the same location as this Instance.

        """
        resp = self._get(f"/{instance_id}/neighbors")
        return get_only_value(resp)

    def list_private_networks(
        self,
        instance_id: str,
        per_page: int = None,
        cursor: str = None,
        capacity: int = None,
    ) -> VultrPagination[PrivateNetworkItem]:
        """List the private networks for an Instance.

        Args:
            instance_id: The Instance id.
            per_page: Number of items requested per page. Default is 100 and Max is 500.
            cursor: Cursor for paging.
            capacity: the capacity of the VultrPagination[PrivateNetworkItem],
            see `pyvultr.utils.VultrPagination` for detail.

        Returns:
            VultrPagination[PrivateNetworkItem]: a paginated list of `PrivateNetworkItem`.
        """
        fetcher = partial(self._get, endpoint=f"/{instance_id}/private-networks")
        return VultrPagination[PrivateNetworkItem](
            fetcher=fetcher,
            cursor=cursor,
            page_size=per_page,
            return_type=PrivateNetworkItem,
            capacity=capacity,
        )

    def get_iso_status(self, instance_id: str) -> ISOStatus:
        """Get the ISO status for an Instance.

        Args:
            instance_id: The Instance id.

        Returns:
            ISOStatus: A `ISOStatus` object.
        """
        resp = self._get(f"/{instance_id}/iso")
        return dacite.from_dict(data_class=ISOStatus, data=get_only_value(resp))

    def attach_iso(self, instance_id: str, iso_id: str = None):
        """Attach an ISO to an Instance.

        Args:
            instance_id: The Instance id.
            iso_id: The ISO id.

        Returns:
            STATUS CODE: 202
            /NO CONTENT/
        """
        _json = {
            "iso_id": iso_id,
        }
        return self._post(f"/{instance_id}/iso/attach", json=_json)

    def detach_iso(self, instance_id: str):
        """Detach the ISO from an Instance.

        Args:
            instance_id: The Instance id.

        Returns:
            STATUS CODE: 202
            /NO CONTENT/
        """
        return self._post(f"/{instance_id}/iso/detach")

    def attach_private_network(self, instance_id: str, network_id: str = None):
        """Attach Private Network to an Instance.

        Args:
            instance_id: The Instance id.
            network_id: The Private Network id.

        Returns:
            STATUS CODE: 204
            /NO CONTENT/
        """
        _json = {
            "network_id": network_id,
        }
        return self._post(f"/{instance_id}/private-networks/attach", json=_json)

    def detach_private_network(self, instance_id: str, network_id: str = None):
        """Detach Private Network from an Instance.

        Args:
            instance_id: The Instance id.
            network_id: The Private Network id.

        Returns:
            STATUS CODE: 204
            /NO CONTENT/
        """
        _json = {
            "network_id": network_id,
        }
        return self._post(f"/{instance_id}/private-networks/detach", json=_json)

    def set_backup_schedule(
        self,
        instance_id: str,
        backup_type: BackupScheduleType = None,
        hour: int = None,
        dow: int = None,
        dom: int = None,
    ) -> BackupSchedule:
        """Set the backup schedule for an Instance in UTC. The `backup_type` is required.

        Args:
            instance_id: The Instance id.
            backup_type: Type of backup schedule.
            hour: Hour of day to run in UTC.
            dow: Day of week to run.
            dom: Day of month to run. Use values between 1 and 28.

        Returns:
            BackupSchedule: A `BackupSchedule` object.
        """
        _json = {
            "type": backup_type.value,
            "hour": hour,
            "dow": dow,
            "dom": dom,
        }
        resp = self._post(f"/{instance_id}/backup-schedule", json=_json)
        return dacite.from_dict(data_class=BackupSchedule, data=get_only_value(resp))

    def get_backup_schedule(self, instance_id: str) -> BackupSchedule:
        """Get the backup schedule for an Instance.

        Args:
            instance_id: The Instance id.

        Returns:
            BackupSchedule: A `BackupSchedule` object.
        """
        resp = self._get(f"/{instance_id}/backup-schedule")
        return dacite.from_dict(data_class=BackupSchedule, data=get_only_value(resp))

    def restore(self, instance_id: str, backup_id: str = None, snapshot_id: str = None) -> RestoreStatus:
        """Restore an Instance from either `backup_id` or `snapshot_id`.

        Args:
            instance_id: The Instance id.
            backup_id: The Backup id.
            snapshot_id: The Snapshot id.

        Returns:
            RestoreStatus: A `RestoreStatus` object.
        """
        _json = {
            "backup_id": backup_id,
            "snapshot_id": snapshot_id,
        }
        resp = self._post(f"/{instance_id}/restore", json=_json)
        return dacite.from_dict(data_class=RestoreStatus, data=get_only_value(resp))

    def list_ipv4s(
        self,
        instance_id: str,
        public_network: bool = None,
        per_page: int = None,
        cursor: str = None,
        capacity: int = None,
    ) -> VultrPagination[IPv4Item]:
        """List the IPv4 information for an Instance.

        Args:
            instance_id: The Instance id.
            public_network: List only Public networks.
            per_page: Number of items requested per page. Default is 100 and Max is 500.
            cursor: Cursor for paging.
            capacity: the capacity of the VultrPagination[IPv4Item],
            see `pyvultr.utils.VultrPagination` for detail.

        Returns:
            VultrPagination[IPv4Item]: a paginated list of `IPv4Item`.
        """
        _public_network = None
        if public_network is not None:
            _public_network = "yes" if public_network else "no"
        _extra_params = {
            "public_network": _public_network,
        }
        fetcher = partial(self._get, endpoint=f"/{instance_id}/ipv4s")
        return VultrPagination[IPv4Item](
            fetcher=fetcher,
            cursor=cursor,
            page_size=per_page,
            return_type=IPv4Item,
            capacity=capacity,
            **_extra_params,
        )

    def create_ipv4(self, instance_id: str, reboot: bool = None) -> IPv4Item:
        """Create an IPv4 address for an Instance.

        Args:
            instance_id: The Instance id.
            reboot: Set if the server is rebooted immediately after the IPv4 address is created.

        Returns:
            IPv4Item: A `IPv4Item` object.
        """
        _json = {
            "reboot": reboot,
        }
        resp = self._post(f"/{instance_id}/ipv4", json=_json)
        return dacite.from_dict(data_class=IPv4Item, data=get_only_value(resp))

    def list_ipv6s(
        self,
        instance_id: str,
        per_page: int = None,
        cursor: str = None,
        capacity: int = None,
    ) -> VultrPagination[IPv6Item]:
        """List the reverse IPv6 information for an Instance.

        Args:
            instance_id: The Instance id.
            per_page: Number of items requested per page. Default is 100 and Max is 500.
            cursor: Cursor for paging.
            capacity: the capacity of the VultrPagination[IPv6Item],
            see `pyvultr.utils.VultrPagination` for detail.

        Returns:
            VultrPagination[IPv6Item]: a paginated list of `IPv6Item`.
        """
        fetcher = partial(self._get, endpoint=f"/{instance_id}/ipv6")
        return VultrPagination[IPv4Item](
            fetcher=fetcher,
            cursor=cursor,
            page_size=per_page,
            return_type=IPv4Item,
            capacity=capacity,
        )

    def create_ipv6_reverse(self, instance_id: str, ip: str, reverse: str):
        """Create a reverse IPv6 entry for an Instance.

        The `ip` and `reverse` attributes are required. IP address must be in full, expanded format.

        Args:
            instance_id: The Instance id.
            ip: The IPv6 address in full, expanded format.
            reverse: The IPv6 reverse entry.

        Returns:
            STATUS CODE: 204
            /NO CONTENT/
        """
        _json = {
            "ip": ip,
            "reverse": reverse,
        }
        return self._post(f"/{instance_id}/ipv6/reverse", json=_json)

    def list_ipv6_reverses(self, instance_id: str) -> List[IPv6ReverseItem]:
        """List the reverse IPv6 information for an Instance.

        Args:
            instance_id: The Instance id.

        Returns:
            List[IPv6ReverseItem]: A list of `IPv6ReverseItem`.
        """
        _resp = self._get(f"/{instance_id}/ipv6/reverse")
        reps = get_only_value(_resp)
        return [dacite.from_dict(data_class=IPv6ReverseItem, data=r) for r in reps]

    def create_ipv4_reverse(self, instance_id: str, ip: str, reverse: str):
        """Create a reverse IPv4 entry for an Instance.

        The `ip` and `reverse` attributes are required.

        Args:
            instance_id: The Instance id.
            ip: The IPv4 address.
            reverse: The IPv4 reverse entry.

        Returns:
            STATUS CODE: 204
            /NO CONTENT/
        """
        _json = {
            "ip": ip,
            "reverse": reverse,
        }
        return self._post(f"/{instance_id}/ipv4/reverse", json=_json)

    def get_user_date(self, instance_id: str) -> UserData:
        """Get the user-supplied, base64 encoded user data for an Instance.

        Args:
            instance_id: The Instance id.

        Returns:
            UserData: A `UserData` object.
        """
        resp = self._get(f"/{instance_id}/user-date")
        return dacite.from_dict(data_class=UserData, data=get_only_value(resp))

    def halt(self, instance_id: str):
        """Halt an Instance.

        Args:
            instance_id: The Instance id.

        Returns:
            STATUS CODE: 204
            /NO CONTENT/
        """
        return self._post(f"/{instance_id}/halt")

    def set_default_reverse_dns_entry(self, instance_id: str, ip: str):
        """Set a reverse DNS entry for an IPv4 address.

        Args:
            instance_id: The Instance id.
            ip: The IP address.

        Returns:
            STATUS CODE: 204
            /NO CONTENT/
        """
        _json = {
            "ip": ip,
        }
        return self._post(f"/{instance_id}/reverse/default", json=_json)

    def delete_ipv4(self, instance_id: str, ipv4: str):
        """Delete an IPv4 address from an Instance.

        Args:
            instance_id: The Instance id.
            ipv4: The IPv4 address.

        Returns:
            STATUS CODE: 204
            /NO CONTENT/
        """
        return self._delete(f"/{instance_id}/ipv4/{ipv4}")

    def delete_reverse_ipv6(self, instance_id: str, ipv6: str):
        """Delete the reverse IPv6 for an Instance.

        Args:
            instance_id: The Instance id.
            ipv6: The IPv6 address.

        Returns:
            STATUS CODE: 204
            /NO CONTENT/
        """
        return self._delete(f"/{instance_id}/ipv6/reverse/{ipv6}")

    def list_upgrades(self, instance_id: str, upgrade_type: InstanceUpgradeType = None) -> AvailableUpgrade:
        """Get available upgrades for an Instance.

        Args:
            instance_id: The Instance id.
            upgrade_type: Filter upgrade by type.

        Returns:
            AvailableUpgrade: A `AvailableUpgrade` object.
        """
        _params = {
            "type": upgrade_type and upgrade_type.value,
        }
        _resp = self._get(f"/{instance_id}/upgrades", params=_params)
        return dacite.from_dict(data_class=AvailableUpgrade, data=get_only_value(_resp))
