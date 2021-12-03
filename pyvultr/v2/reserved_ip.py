from dataclasses import dataclass
from typing import Optional
from urllib.parse import urljoin

from pyvultr.utils import BaseDataclass, VultrPagination, get_only_value

from .base import BaseVultrV2, command
from .enums import IPType


@dataclass
class ReservedIP(BaseDataclass):
    id: str
    region: str
    ip_type: str
    subnet: str
    subnet_size: int
    label: str
    instance_id: str


class ReservedIPAPI(BaseVultrV2):
    """Vultr ReservedIP API.

    Reference: https://www.vultr.com/api/#tag/reserved-ip

    IP addresses can be reserved and moved between instances.
    Reserved IPs can also be used as floating addresses for high-availability.

    Attributes:
        api_key: Vultr API key, we get it from env variable `$VULTR_API_KEY` if not provided.
    """

    def __init__(self, api_key: Optional[str] = None):
        super().__init__(api_key)

    @property
    def base_url(self):
        """Get base url for all API in this section."""
        return urljoin(super().base_url, "reserved-ips")

    @command
    def list(self, per_page: int = None, cursor: str = None, capacity: int = None) -> VultrPagination[ReservedIP]:
        """List all Reserved IPs in your account.

        Args:
            per_page: number of items requested per page. Default is 100 and Max is 500.
            cursor: cursor for paging.
            capacity: The capacity of the VultrPagination[ReservedIPItem], see `VultrPagination` for details.

        Returns:
            VultrPagination[ReservedIP]: A list-like object of `ReservedIPItem` object.
        """
        return VultrPagination[ReservedIP](
            fetcher=self._get,
            cursor=cursor,
            page_size=per_page,
            return_type=ReservedIP,
            capacity=capacity,
        )

    @command
    def create(self, region: str, ip_type: IPType, label: str = None) -> ReservedIP:
        """Create a new Reserved IP.

        The `region` and `ip_type` attributes are required.

        Args:
            region: The Region id where the Reserved IP will be created.
            ip_type: The type of IP address.
            label: The user-supplied label.

        Returns:
            ReservedIP: The Reserved IP object.
        """
        _json = {
            "region": region,
            "ip_type": ip_type and ip_type.value,
            "label": label,
        }
        resp = self._post(json=_json)
        return ReservedIP.from_dict(data=get_only_value(resp))

    @command
    def get(self, reserved_ip: str) -> ReservedIP:
        """Get information about a Reserved IP.

        Args:
            reserved_ip: The Reserved IP id.

        Returns:
            ReservedIP: The Reserved IP object.
        """
        resp = self._get(f"/{reserved_ip}")
        return ReservedIP.from_dict(data=get_only_value(resp))

    @command
    def attach(self, reserved_ip: str, instance_id: str):
        """Attach a Reserved IP to an compute instance or a baremetal instance - `instance_id`.

        Args:
            reserved_ip: The Reserved IP id.
            instance_id: Attach the Reserved IP to a Compute Instance id or a Bare Metal Instance id.

        Returns:
            STATUS CODE: 204
            /NO CONTENT/
        """
        _json = {
            "instance_id": instance_id,
        }
        return self._post(f"/{reserved_ip}/attach", json=_json)

    @command
    def detach(self, reserved_ip: str):
        """Detach a Reserved IP.

        Args:
            reserved_ip: The Reserved IP id.

        Returns:
            STATUS CODE: 204
            /NO CONTENT/
        """
        return self._post(f"/{reserved_ip}/detach")

    @command
    def to_reserved(self, ip_address: str, label: str = None) -> ReservedIP:
        """Convert the `ip_address` of an existing instance into a Reserved IP.

        Args:
            ip_address: The IP address to convert.
            label: A user-supplied label for this IP address.

        Returns:
            ReservedIP: The Reserved IP object.
        """
        _json = {
            "ip_address": ip_address,
            "label": label,
        }
        resp = self._post("/convert", json=_json)
        return ReservedIP.from_dict(get_only_value(resp))

    @command
    def delete(self, reserved_ip: str):
        """Delete a Reserved IP.

        Args:
            reserved_ip: The Reserved IP id.

        Returns:
            STATUS CODE: 204
            /NO CONTENT/
        """
        return self._delete(f"/{reserved_ip}")
