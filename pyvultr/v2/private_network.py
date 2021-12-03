from dataclasses import dataclass
from typing import Optional
from urllib.parse import urljoin

from pyvultr.utils import BaseDataclass, VultrPagination, get_only_value

from .base import BaseVultrV2, command


@dataclass
class PrivateNetwork(BaseDataclass):
    id: str  # A unique ID for the Private Network.
    # The Region id where the instance is located, check `RegionAPI.list` and `RegionItem.id` for available regions.
    region: str
    date_created: str  # Date the network was created.
    description: str  # A description of the private network.
    v4_subnet: str  # The IPv4 network address. For example: 10.99.0.0.
    v4_subnet_mask: int  # The number of bits for the netmask in CIDR notation. Example: 24.


class PrivateNetworkAPI(BaseVultrV2):
    """Vultr PrivateNetwork API.

    Reference: https://www.vultr.com/api/#tag/private-Networks

    Private Networks are fully isolated networks accessible only by instances on your account.
    Each private network is only available in one Region and cannot span across regions.
    An instance can connect to multiple private networks and you may have up to 5 private networks per region.

    Attributes:
        api_key: Vultr API key, we get it from env variable `$VULTR_API_KEY` if not provided.
    """

    def __init__(self, api_key: Optional[str] = None):
        super().__init__(api_key)

    @property
    def base_url(self):
        """Get base url for all API in this section."""
        return urljoin(super().base_url, "private-networks")

    @command
    def list(
        self,
        per_page: int = None,
        cursor: str = None,
        capacity: int = None,
    ) -> VultrPagination[PrivateNetwork]:
        """Get a list of all Private Networks in your account.

        Args:
            per_page: Number of items requested per page. Default is 100 and Max is 500.
            cursor: Cursor for paging.
            capacity: The capacity of the VultrPagination[PrivateNetworkItem], see `VultrPagination` for details.

        Returns:
            VultrPagination[PrivateNetwork]: A list-like object of `PrivateNetworkItem` object.
        """
        return VultrPagination[PrivateNetwork](
            fetcher=self._get,
            cursor=cursor,
            page_size=per_page,
            return_type=PrivateNetwork,
            capacity=capacity,
        )

    @command
    def create(
        self,
        region: str,
        description: str = None,
        v4_subnet: str = None,
        v4_subnet_mask: int = None,
    ) -> PrivateNetwork:
        """Create a new Private Network in a region.

        Private networks should use RFC1918 private address space:
            - 10.0.0.0    - 10.255.255.255  (10/8 prefix)
            - 172.16.0.0  - 172.31.255.255  (172.16/12 prefix)
            - 192.168.0.0 - 192.168.255.255 (192.168/16 prefix)

        Args:
            region: Create the Private Network in this Region id.
            description: A description of the private network.
            v4_subnet: The IPv4 network address. For example: 10.99.0.0.
            v4_subnet_mask: The number of bits for the netmask in CIDR notation. Example: 24.

        Returns:
            PrivateNetwork: PrivateNetworkItem object.
        """
        _json = {
            "region": region,
            "description": description,
            "v4_subnet": v4_subnet,
            "v4_subnet_mask": v4_subnet_mask,
        }
        resp = self._post(json=_json)
        return PrivateNetwork.from_dict(get_only_value(resp))

    @command
    def get(self, network_id: str) -> PrivateNetwork:
        """Get information about a Private Network.

        Args:
            network_id: The Network ID.

        Returns:
            PrivateNetwork: PrivateNetworkItem object.
        """
        resp = self._get(f"/{network_id}")
        return PrivateNetwork.from_dict(get_only_value(resp))

    @command
    def update(self, network_id: str, description: str):
        """Update information for a Private Network.

        Args:
            network_id: The Network ID.
            description: The Private Network description.

        Returns:
            STATUS CODE: 204
            /NO CONTENT/
        """
        _json = {
            "description": description,
        }
        return self._put(f"/{network_id}", json=_json)

    @command
    def delete(self, network_id: str):
        """Delete a Private Network.

        Args:
            network_id: The Network ID.

        Returns:
            STATUS CODE: 204
            /NO CONTENT/
        """
        return self._delete(f"/{network_id}")
