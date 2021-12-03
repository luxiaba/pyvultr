import logging
from dataclasses import dataclass
from functools import partial
from typing import Dict, List, Optional
from urllib.parse import urljoin

from pyvultr.utils import BaseDataclass, VultrPagination, get_only_value

from .base import BaseVultrV2, command
from .enums import BackupScheduleType, InstanceUpgradeType

log = logging.getLogger(__name__)


@dataclass
class ReqInstance(BaseDataclass):
    # [REQUIRED]
    # The Region id where the instance is located, check `RegionAPI.list` and `RegionItem.id` for available regions.
    region: str
    plan: str

    # [CHOOSE_ONE] Please choose one source to create instance
    os_id: int = None  # The Operating System id, check OperatingSystemAPI.list and `OSItem.id` for available OSes.
    iso_id: str = None  # The ISO id to use when deploying this instance.
    snapshot_id: str = None  # The Snapshot id to use when deploying the instance.
    app_id: int = None  # The Application id, check `Application.list` and `ApplicationItem.id` for available options.
    # The Application image_id, check `Application.list` and `ApplicationItem.image_id` for available options.
    image_id: str = None

    # [OPTIONAl]
    ipxe_chain_url: str = None  # The URL location of the iPXE chain loader.
    script_id: str = None  # The Startup Script id to use when deploying this instance.
    enable_ipv6: bool = None  # Enable IPv6.

    # An array of Private Network ids to attach to this Instance.
    # This parameter takes precedence over `enable_private_network`. Please choose one parameter.
    attach_private_network: List[str] = None
    # If `true`, private networking support will be added to the new server.
    # This parameter attaches a single network. When no network exists in the region, it will be automatically created.
    enable_private_network: bool = None

    label: str = None  # The user-supplied label for this instance.
    sshkey_id: List[str] = None  # The SSH Key id(create in advance) to install on this instance.
    backups: str = None  # 'enabled'/'disabled' Enable automatic backups for the instance.
    user_data: str = None  # The user-supplied, base64 encoded user data to attach to this instance.
    ddos_protection: bool = None  # Enable DDoS protection (there is an additional charge for this).
    activation_email: bool = None  # Notify by email after deployment, default is false.
    hostname: str = None  # Set hostname for this instance.
    tag: str = None  # Set tag for this instance.
    firewall_group_id: str = None  # The Firewall Group id to attach to this Instance.
    reserved_ipv4: str = None  # ID of the floating IP to use as the main IP of this server.

    @property
    def valid_basic(self) -> bool:
        """Region and plan are required."""
        return all((self.region, self.plan))

    @property
    def valid_source(self) -> bool:
        """Check whether the data meets the conditions for instance creation."""
        return any((self.os_id, self.iso_id, self.snapshot_id, self.app_id, self.image_id))


@dataclass
class Instance(BaseDataclass):
    id: str  # A unique ID for the VPS Instance.
    os: str  # The Operating System name, check OperatingSystemAPI.list and `OSItem.name` for available OSes.
    ram: int  # Text description of the instances' RAM.
    disk: int  # Text description of the instances' disk configuration.
    main_ip: str  # The main IPv4 address.
    vcpu_count: int  # Number of vCPUs.
    # The Region id where the instance is located, check `RegionAPI.list` and `RegionItem.id` for available regions.
    region: str
    date_created: str  # The date this instance was created.
    status: str  # The status of the instance, see `enums.InstanceStatus` for possible values.
    power_status: str  # The power-on status, see `enums.InstancePowerStatus` for possible values.
    server_status: str  # The server health status, see `enums.InstanceServerStatus` for possible values.
    allowed_bandwidth: int  # Monthly bandwidth quota in GB.
    netmask_v4: str  # The IPv4 netmask in dot-decimal notation.
    gateway_v4: str  # The gateway IP address.
    v6_network: str  # The IPv6 network size in bits.
    v6_network_size: int  # The IPv6 subnet.
    v6_main_ip: str  # The main IPv6 network address.
    hostname: str  # The hostname of the instance.
    label: str  # The user-supplied label for this instance.
    tag: str  # The user-supplied tag for this instance.
    internal_ip: str  # The user data that can be supplied for tools such as cloudinit.
    kvm: str  # HTTPS link to the Vultr noVNC Web Console.
    os_id: int  # The Operating System id, check OperatingSystemAPI.list and `OSItem.id` for available OSes.
    app_id: int  # The Application id, check `Application.list` and `ApplicationItem.id` for available options.
    firewall_group_id: str  # The Firewall Group id linked to this Instance.
    features: List[str]  # A list of features enabled on the instance, see `enums.InstanceFeatures` for possible values.
    plan: str  # A unique ID for the Plan.
    default_password: str = None  # The default password assigned at deployment.


@dataclass
class BandwidthItem(BaseDataclass):
    incoming_bytes: int  # Total bytes received by this instance on the date (UTC) denoted by the object key.
    outgoing_bytes: int  # Total bytes sent by this instance on the date (UTC) denoted by the object key.


@dataclass
class InstancePrivateNetworkItem(BaseDataclass):
    ip_address: str  # The assigned IP address.
    mac_address: str  # The assigned MAC address.
    network_id: str  # The private network id.


@dataclass
class ISOStatus(BaseDataclass):
    iso_id: str  # The ISO id, check `ISO.list` and `ISOItem.id` for available options.
    state: str  # The status of this ISO, check `enums.ISOStatusState` for possible values.


@dataclass
class BackupSchedule(BaseDataclass):
    enabled: bool  # Indicates if backup is enabled.
    type: str  # Type of backup schedule, check `enums.BackupScheduleType` for possible values.
    next_scheduled_time_utc: str  # Time of next backup run in UTC.
    hour: int  # Scheduled hour of day in UTC.
    dow: int  # Day of week to run, possible value: 1-7 (1 is Sunday).
    dom: int  # Day of month to run. Use values between 1 and 28.


@dataclass
class RestoreStatus(BaseDataclass):
    restore_type: str
    restore_id: str
    status: str


@dataclass
class IPv4Item(BaseDataclass):
    ip: str  # The IPv4 address.
    netmask: str  # The IPv4 netmask in dot-decimal notation.
    gateway: str  # The gateway IP address.
    type: str  # The type of IP address, check `enums.IPV4Type` for details.
    reverse: str  # The reverse DNS information for this IP address.
    # The MAC address associated with this IP address.
    # It's in the document, but not in the code.
    mac_address: str = None


@dataclass
class IPv6Item(BaseDataclass):
    ip: str  # A unique ID for the IPv6 address.
    network: str  # The IPv6 subnet.
    network_size: int  # The IPv6 network size in bits.
    type: str  # The type of IP address, check `enums.IPV6Type` for details.


@dataclass
class IPv6ReverseItem(BaseDataclass):
    reverse: str  # The IPv6 reverse entry.
    ip: str  # The IPv6 address.


@dataclass
class UserData(BaseDataclass):
    data: str  # The user-supplied, base64 encoded user data attached to this instance.


@dataclass
class AvailableUpgrade(BaseDataclass):
    applications: List  # Available application upgrades, list of any.
    os: List  # Available os upgrades, list of any.
    plans: List  # Available plan upgrades, list of any.


class InstanceAPI(BaseVultrV2):
    """Vultr Instance API.

    Reference: https://www.vultr.com/api/#tag/instances

    Vultr Cloud instances can be deployed with your preferred operating system or pre-installed application in seconds.
    High Frequency Compute instances are powered by high clock speed CPU's and NVMe local storage to power
    your most demanding applications. Dedicated Cloud instances have dedicated CPU, SSD drives, and RAM.

    Attributes:
        api_key: Vultr API key, we get it from env variable `$VULTR_API_KEY` if not provided.
    """

    def __init__(self, api_key: Optional[str] = None):
        super().__init__(api_key)

    @property
    def base_url(self):
        """Get base url for all API in this section."""
        return urljoin(super().base_url, "instances")

    @command
    def list(
        self,
        per_page: int = None,
        cursor: str = None,
        tag: str = None,
        label: str = None,
        main_ip: str = None,
        capacity: int = None,
    ) -> VultrPagination[Instance]:
        """List all Bare Metal instances in your account.

        Args:
            per_page: Number of items requested per page. Default is 100 and Max is 500.
            cursor: Cursor for paging.
            tag: Filter by specific tag.
            label: Filter by label.
            main_ip: Filter by main ip address.
            capacity: The capacity of the VultrPagination[InstanceItem], see `VultrPagination` for details.

        Returns:
            VultrPagination[Instance]: A list-like object of `InstanceItem` object.
        """
        _extra_params = {
            "tag": tag,
            "label": label,
            "main_ip": main_ip,
        }
        return VultrPagination[Instance](
            fetcher=self._get,
            cursor=cursor,
            page_size=per_page,
            return_type=Instance,
            capacity=capacity,
            **_extra_params,
        )

    @command
    def create(self, instance: ReqInstance) -> Optional[Instance]:
        """Create a new VPS Instance in a region with the desired plan.

        Choose one of the following to deploy the instance:
            - os_id
            - iso_id
            - snapshot_id
            - app_id
            - image_id
        Supply other attributes as desired.

        Args:
            instance: A ReqInstance object to create instance.

        Returns:
            Instance: A `InstanceItem` object.
        """
        if not instance.valid_basic:
            log.error(f"Invalid instance: {instance}, `Region` and `Plan` is required.")
            return
        if not instance.valid_source:
            log.error(
                f"Invalid instance: {instance}, "
                f"Please provide at least one: `os_id`, `iso_id`, `image_id`, `snapshot_id`, `app_id`."
            )
            return

        resp = self._post(json=instance.to_dict())
        return Instance.from_dict(get_only_value(resp))

    @command
    def get(self, instance_id: str) -> Instance:
        """Get information about an Instance.

        Args:
            instance_id: The Instance id.

        Returns:
            Instance: A `InstanceItem` object.
        """
        resp = self._get(f"/{instance_id}")
        return Instance.from_dict(get_only_value(resp))

    @command
    def update(self, instance_id: str, **kwargs) -> Instance:
        """Update information for an Instance.

        All attributes are optional. If not set, the attributes will retain their original values.
        Note: Changing `os_id`, `app_id` or `image_id` may take a few extra seconds to complete.

        Args:
            instance_id: The Instance id.
            **kwargs: Other attributes to update.

        Returns:
            Instance: A `InstanceItem` object.
        """
        resp = self._patch(f"/{instance_id}", json=kwargs)
        return Instance.from_dict(get_only_value(resp))

    @command
    def delete(self, instance_id: str):
        """Delete an Instance.

        Args:
            instance_id: The Instance id.

        Returns:
            STATUS CODE: 204
            /NO CONTENT/
        """
        return self._delete(f"/{instance_id}")

    @command
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

    @command
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

    @command
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

    @command
    def start(self, instance_id: str):
        """Start an Instance.

        Args:
            instance_id: The Instance id.

        Returns:
            STATUS CODE: 204
            /NO CONTENT/
        """
        return self._post(f"/{instance_id}/start")

    @command
    def reboot(self, instance_id: str):
        """Reboot an Instance.

        Args:
            instance_id: The Instance id.

        Returns:
            STATUS CODE: 204
            /NO CONTENT/
        """
        return self._post(f"/{instance_id}/reboot")

    @command
    def reinstall(self, instance_id: str, hostname: str = None) -> Instance:
        """Reinstall an Instance using an optional `hostname`.

        Note: This action may take a few extra seconds to complete.

        Args:
            instance_id: The Instance id.
            hostname: The hostname to use when reinstalling this instance.

        Returns:
            Instance: A `InstanceItem` object.
        """
        _json = {
            "hostname": hostname,
        }
        resp = self._post(f"/{instance_id}/reinstall", json=_json)
        return Instance.from_dict(get_only_value(resp))

    @command
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
        return {_date: BandwidthItem.from_dict(item) for _date, item in resp.items()}

    @command
    def list_neighbors(self, instance_id: str) -> List[str]:
        """Get a list of other instances in the same location as this Instance.

        Args:
            instance_id: The Instance id.

        Returns:
            List[str]: An array of Instance ids in the same location as this Instance.
        """
        resp = self._get(f"/{instance_id}/neighbors")
        return get_only_value(resp)

    @command
    def list_private_networks(
        self,
        instance_id: str,
        per_page: int = None,
        cursor: str = None,
        capacity: int = None,
    ) -> VultrPagination[InstancePrivateNetworkItem]:
        """List the private networks for an Instance.

        Args:
            instance_id: The Instance id.
            per_page: Number of items requested per page. Default is 100 and Max is 500.
            cursor: Cursor for paging.
            capacity: The capacity of the VultrPagination[PrivateNetworkItem], see `VultrPagination` for details.

        Returns:
            VultrPagination[InstancePrivateNetworkItem]: A list-like object of `PrivateNetworkItem` object.
        """
        fetcher = partial(self._get, endpoint=f"/{instance_id}/private-networks")
        return VultrPagination[InstancePrivateNetworkItem](
            fetcher=fetcher,
            cursor=cursor,
            page_size=per_page,
            return_type=InstancePrivateNetworkItem,
            capacity=capacity,
        )

    @command
    def get_iso_status(self, instance_id: str) -> ISOStatus:
        """Get the ISO status for an Instance.

        Args:
            instance_id: The Instance id.

        Returns:
            ISOStatus: A `ISOStatus` object.
        """
        resp = self._get(f"/{instance_id}/iso")
        return ISOStatus.from_dict(get_only_value(resp))

    @command
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

    @command
    def detach_iso(self, instance_id: str):
        """Detach the ISO from an Instance.

        Args:
            instance_id: The Instance id.

        Returns:
            STATUS CODE: 202
            /NO CONTENT/
        """
        return self._post(f"/{instance_id}/iso/detach")

    @command
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

    @command
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

    @command
    def set_backup_schedule(
        self,
        instance_id: str,
        backup_type: BackupScheduleType,
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
        return BackupSchedule.from_dict(get_only_value(resp))

    @command
    def get_backup_schedule(self, instance_id: str) -> BackupSchedule:
        """Get the backup schedule for an Instance.

        Args:
            instance_id: The Instance id.

        Returns:
            BackupSchedule: A `BackupSchedule` object.
        """
        resp = self._get(f"/{instance_id}/backup-schedule")
        return BackupSchedule.from_dict(get_only_value(resp))

    @command
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
        return RestoreStatus.from_dict(get_only_value(resp))

    @command
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
            capacity: The capacity of the VultrPagination[IPv4Item], see `VultrPagination` for details.

        Returns:
            VultrPagination[IPv4Item]: A list-like object of `IPv4Item` object.
        """
        _public_network = None
        if public_network is not None:
            _public_network = "yes" if public_network else "no"
        _extra_params = {
            "public_network": _public_network,
        }
        fetcher = partial(self._get, endpoint=f"/{instance_id}/ipv4")
        return VultrPagination[IPv4Item](
            fetcher=fetcher,
            cursor=cursor,
            page_size=per_page,
            return_type=IPv4Item,
            capacity=capacity,
            **_extra_params,
        )

    @command
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
        return IPv4Item.from_dict(get_only_value(resp))

    @command
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
            capacity: The capacity of the VultrPagination[IPv6Item], see `VultrPagination` for details.

        Returns:
            VultrPagination[IPv6Item]: A list-like object of `IPv6Item` object.
        """
        fetcher = partial(self._get, endpoint=f"/{instance_id}/ipv6")
        return VultrPagination[IPv6Item](
            fetcher=fetcher,
            cursor=cursor,
            page_size=per_page,
            return_type=IPv6Item,
            capacity=capacity,
        )

    @command
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

    @command
    def list_ipv6_reverses(self, instance_id: str) -> List[IPv6ReverseItem]:
        """List the reverse IPv6 information for an Instance.

        Args:
            instance_id: The Instance id.

        Returns:
            List[IPv6ReverseItem]: A list of `IPv6ReverseItem`.
        """
        _resp = self._get(f"/{instance_id}/ipv6/reverse")
        reps = get_only_value(_resp)
        return [IPv6ReverseItem.from_dict(r) for r in reps]

    @command
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

    @command
    def get_user_date(self, instance_id: str) -> UserData:
        """Get the user-supplied, base64 encoded user data for an Instance.

        Args:
            instance_id: The Instance id.

        Returns:
            UserData: A `UserData` object.
        """
        resp = self._get(f"/{instance_id}/user-data")
        return UserData.from_dict(get_only_value(resp))

    @command
    def halt(self, instance_id: str):
        """Halt an Instance.

        Args:
            instance_id: The Instance id.

        Returns:
            STATUS CODE: 204
            /NO CONTENT/
        """
        return self._post(f"/{instance_id}/halt")

    @command
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

    @command
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

    @command
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

    @command
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
        resp = self._get(f"/{instance_id}/upgrades", params=_params)
        return AvailableUpgrade.from_dict(get_only_value(resp))
