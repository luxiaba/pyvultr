from dataclasses import dataclass
from functools import partial
from typing import Optional
from urllib.parse import urljoin

import dacite

from pyvultr.utils import BaseDataclass, VultrPagination, get_only_value
from pyvultr.v2.base import BaseVultrV2
from pyvultr.v2.enum import FirewallProtocol, IPType


@dataclass
class FirewallGroup(BaseDataclass):
    id: str
    description: str
    date_created: str
    date_modified: str
    instance_count: int
    rule_count: int
    max_rule_count: int


@dataclass
class FirewallRule(BaseDataclass):
    id: int
    type: str
    action: str
    protocol: str
    port: str
    subnet: str
    subnet_size: int
    source: str
    notes: str


class Firewall(BaseVultrV2):
    """Vultr Firewall API.

    Vultr offers a web-based firewall solution to protect one or more compute instances.
    Firewall groups can manage multiple servers with a standard ruleset. You can control multiple groups with the API.

    Attributes:
        api_key: Vultr API key, we get it from env variable `VULTR_API_TOKEN` if not provided.
    """

    def __init__(self, api_key: Optional[str] = None):
        super().__init__(api_key)

    @property
    def base_url(self):
        """Get base url for all API in this section."""
        return urljoin(super().base_url, "firewalls")

    def list_groups(
        self,
        per_page: int = None,
        cursor: str = None,
        capacity: int = None,
    ) -> VultrPagination[FirewallGroup]:
        """Get a list of all Firewall Groups.

        Args:
            per_page: number of items requested per page. Default is 100 and Max is 500.
            cursor: cursor for paging.
            capacity: the capacity of the VultrPagination[FirewallGroup],
            see `pyvultr.utils.VultrPagination` for detail.

        Returns:
            VultrPagination[FirewallGroup]: A paginated list of `FirewallGroup`.
        """
        return VultrPagination[FirewallGroup](
            fetcher=self._get,
            cursor=cursor,
            page_size=per_page,
            return_type=FirewallGroup,
            capacity=capacity,
        )

    def create_group(self, description: str = None) -> FirewallGroup:
        """Create a new Firewall Group.

        Args:
            description: User-supplied description of this Firewall Group.

        Returns:
            FirewallGroup: A `FirewallGroup` object.
        """
        _json = {
            "description": description,
        }
        resp = self._post(json=_json)
        return dacite.from_dict(data_class=FirewallGroup, data=get_only_value(resp))

    def get_group(self, firewall_group_id: str) -> FirewallGroup:
        """Get information for a Firewall Group.

        Args:
            firewall_group_id: The firewall group id.

        Returns:
            FirewallGroup: A `FirewallGroup` object.
        """
        resp = self._get(f"/{firewall_group_id}")
        return dacite.from_dict(data_class=FirewallGroup, data=get_only_value(resp))

    def update_group(self, firewall_group_id: str, description: str):
        """Update information for a Firewall Group.

        Args:
            firewall_group_id: The firewall group id.
            description: User-supplied description of this Firewall Group.

        Returns:
            STATUS CODE: 204
            /NO CONTENT/
        """
        _json = {
            "description": description,
        }
        return self._post(f"/{firewall_group_id}", json=_json)

    def delete_group(self, firewall_group_id: str):
        """Delete a Firewall Group.

        Args:
            firewall_group_id: The firewall group id.

        Returns:
            STATUS CODE: 204
            /NO CONTENT/
        """
        return self._delete(f"/{firewall_group_id}")

    def list_rules(
        self,
        firewall_group_id: str,
        per_page: int = None,
        cursor: str = None,
        capacity: int = None,
    ) -> VultrPagination[FirewallRule]:
        """Get a list of all Firewall Groups.

        Args:
            firewall_group_id:  The firewall group id.
            per_page: number of items requested per page. Default is 100 and Max is 500.
            cursor: cursor for paging.
            capacity: the capacity of the VultrPagination[FirewallRule],
            see `pyvultr.utils.VultrPagination` for detail.

        Returns:
            VultrPagination[FirewallRule]: A paginated list of `FirewallRule`.
        """
        fetcher = partial(self._get, endpoint=f"/{firewall_group_id}/rules")
        return VultrPagination[FirewallRule](
            fetcher=fetcher,
            cursor=cursor,
            page_size=per_page,
            return_type=FirewallRule,
            capacity=capacity,
        )

    def create_rule(
        self,
        firewall_group_id: str,
        ip_type: IPType,
        protocol: FirewallProtocol,
        subnet: str,
        subnet_size: int,
        port: str = None,
        source: str = None,
        notes: str = None,
    ) -> FirewallRule:
        """Create a Firewall Rule for a Firewall Group.

        The attributes `ip_type`, `protocol`, `subnet`, and `subnet_size` are required.

        Args:
            firewall_group_id: The firewall group id.
            ip_type: The type of IP rule.
            protocol: The protocol for this rule.
            subnet: The IPv4 network in CIDR notation. Example: 192.0.2.123.
            subnet_size: The number of bits for the netmask in CIDR notation. Example: 32.
            port: TCP/UDP only. This field can be a specific port or a colon separated port range.
            source: If the source string is given a value of "cloudflare" subnet and subnet_size will both be ignored.
            notes: User-supplied notes for this rule.

        Returns:
            FirewallRule: A `FirewallRule` object.
        """
        _json = {
            "ip_type": ip_type.value,
            "protocol": protocol.value,
            "subnet": subnet,
            "subnet_size": subnet_size,
            "port": port,
            "source": source,
            "notes": notes,
        }
        resp = self._post(f"/{firewall_group_id}/rules", json=_json)
        return dacite.from_dict(data_class=FirewallRule, data=get_only_value(resp))

    def get_rule(self, firewall_group_id: str, firewall_rule_id: str) -> FirewallRule:
        """Get a Firewall Rule.

        Args:
            firewall_group_id: The firewall group id.
            firewall_rule_id: The firewall rule id.

        Returns:
            FirewallRule: A `FirewallRule` object.
        """
        resp = self._get(f"/{firewall_group_id}/rules/{firewall_rule_id}")
        return dacite.from_dict(data_class=FirewallRule, data=get_only_value(resp))

    def delete_rule(self, firewall_group_id: str, firewall_rule_id: str):
        """Delete a Firewall Rule.

        Args:
            firewall_group_id: The firewall group id.
            firewall_rule_id: The firewall rule id.

        Returns:
            STATUS CODE: 204
            /NO CONTENT/
        """
        return self._delete(f"/{firewall_group_id}/rules/{firewall_rule_id}")
