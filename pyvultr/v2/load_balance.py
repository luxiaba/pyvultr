from dataclasses import dataclass
from functools import partial
from typing import Dict, List, Optional
from urllib.parse import urljoin

from pyvultr.utils import BaseDataclass, VultrPagination, get_only_value, merge_args

from .base import BaseVultrV2, command
from .enums import LoadBalanceAlgorithm, LoadBalanceProtocol


@dataclass
class LoadBalanceGenericInfo(BaseDataclass):
    # If true, this will redirect all HTTP traffic to HTTPS.
    # You must have an HTTPS rule and SSL certificate installed on the load balancer to enable this option.
    ssl_redirect: bool
    sticky_sessions: Dict  # Array of sticky session cookies({'cookie_name': 'xxx'}).
    # ID of the private network you wish to use.
    # If private_network is omitted it will default to the public network.
    private_network: str
    # The balancing algorithm, see `enums.LoadBalanceAlgorithm` for possible values.
    balancing_algorithm: str = LoadBalanceAlgorithm.ROUND_ROBIN.value
    # If true, you must configure backend nodes to accept Proxy protocol. default is false.
    proxy_protocol: bool = False


@dataclass
class LoadBalanceHealthCheck(BaseDataclass):
    protocol: str  # The protocol to use for health checks, see `enums.LoadBalanceProtocol` for possible values.
    port: int  # The port to use for health checks.
    path: str  # HTTP Path to check. Only applies if Protocol is HTTP or HTTPS.
    check_interval: int  # Interval between health checks.
    response_timeout: int  # Timeout before health check fails.
    unhealthy_threshold: int  # Number times a check must fail before becoming unhealthy.
    healthy_threshold: int  # Number of times a check must succeed before returning to healthy status.


@dataclass
class LoadBalanceForwardRule(BaseDataclass):
    id: str  # A unique ID for the forwarding rule.
    # The protocol on the Load Balancer to forward to the backend.
    # see `enums.LoadBalanceProtocol` for possible values.
    frontend_protocol: str
    frontend_port: int  # The port number on the Load Balancer to forward to the backend.
    # The protocol destination on the backend server.
    # see `enums.LoadBalanceProtocol` for possible values.
    backend_protocol: str
    backend_port: int  # The port number destination on the backend server.


@dataclass
class LoadBalanceFirewallRule(BaseDataclass):
    id: str  # A unique ID for the firewall rule.
    port: int  # Port for this rule.
    # If the source string is given a value of "cloudflare" then cloudflare IPs will be supplied.
    # Otherwise enter a IP address with subnet size that you wish to permit through the firewall.
    # | Value            | Description
    # | ---------------- | -----------
    # | "192.168.1.1/16" | Ip address with a subnet size.
    # | "cloudflare"     | Allow all of Cloudflare's IP space through the firewall
    source: str
    ip_type: str  # The type of IP rule, see `enums.IPType` for possible values.


@dataclass
class LoadBalance(BaseDataclass):
    id: str  # A unique ID for the Load Balancer.
    date_created: str  # Date this Load Balancer was created.
    # The Region id where the instance is located, check `RegionAPI.list` and `RegionItem.id` for available regions.
    region: str
    label: str  # The user-supplied label for this load-balancer.
    status: str  # The current status, see `enums.LoadBalanceStatus` for possible values.
    ipv4: str  # The IPv4 address of this Load Balancer.
    ipv6: str  # The IPv6 address of this Load Balancer.
    generic_info: LoadBalanceGenericInfo  # An object containing additional options.
    health_check: LoadBalanceHealthCheck
    has_ssl: bool  # Indicates if this Load Balancer has an SSL certificate installed.
    forwarding_rules: List[LoadBalanceForwardRule]  # An array of forwarding rule objects.
    instances: List[str]  # Array of Instance ids attached to this Load Balancer.
    firewall_rules: List[LoadBalanceFirewallRule]  # An array of firewall rule objects.


class LoadBalanceAPI(BaseVultrV2):
    """Vultr LoanBalance API.

    Reference: https://www.vultr.com/api/#tag/load-balancer

    Load Balancers sit in front of your application and distribute incoming traffic across multiple Instances.
    When you control the load balancer via the API, you can inspect the results in the customer portal.

    Attributes:
        api_key: Vultr API key, we get it from env variable `$VULTR_API_KEY` if not provided.
    """

    def __init__(self, api_key: Optional[str] = None):
        super().__init__(api_key)

    @property
    def base_url(self):
        """Get base url for all API in this section."""
        return urljoin(super().base_url, "load-balancers")

    @command
    def list(self, per_page: int = None, cursor: str = None, capacity: int = None) -> VultrPagination[LoadBalance]:
        """List the Load Balancers in your account.

        Args:
            per_page: Number of items requested per page. Default is 100 and Max is 500.
            cursor: Cursor for paging.
            capacity: The capacity of the VultrPagination[LoadBalanceItem], see `VultrPagination` for details.

        Returns:
            VultrPagination[LoadBalance]: A list-like object of `LoadBalanceItem` object.
        """
        return VultrPagination[LoadBalance](
            fetcher=self._get,
            cursor=cursor,
            page_size=per_page,
            return_type=LoadBalance,
            capacity=capacity,
        )

    @command
    def create(self, region: str, **kwargs) -> LoadBalance:
        """Create a new Load Balancer in a particular `region`.

        Args:
            region: The Region id to create this Load Balancer.
            **kwargs: New LoanBalance parameters.

        Returns:
            LoadBalance: The LoadBalanceItem object.
        """
        _fixed_kwargs = {"region": region}
        resp = self._post(json=merge_args(kwargs, _fixed_kwargs))
        return LoadBalance.from_dict(get_only_value(resp))

    @command
    def get(self, load_balancer_id: str) -> LoadBalance:
        """Get information for a Load Balancer.

        Args:
            load_balancer_id: The Loan Balance id.

        Returns:
            LoadBalance: The LoadBalanceItem object.
        """
        resp = self._get(f"/{load_balancer_id}")
        return LoadBalance.from_dict(get_only_value(resp))

    @command
    def update(self, load_balancer_id: str, **kwargs):
        """Update information for a Load Balancer.

        All attributes are optional. If not set, the attributes will retain their original values.

        Args:
            load_balancer_id: The Loan Balance id.
            **kwargs: Updated LoanBalance parameters.

        Returns:
            STATUS CODE: 204
            /NO CONTENT/
        """
        return self._patch(f"/{load_balancer_id}", json=kwargs)

    @command
    def delete(self, load_balancer_id: str):
        """Delete a Load Balancer.

        Args:
            load_balancer_id: The Loan Balance id.

        Returns:
            STATUS CODE: 204
            /NO CONTENT/
        """
        return self._delete(f"/{load_balancer_id}")

    @command
    def list_forwarding_rules(
        self,
        load_balancer_id: str,
        per_page: int = None,
        cursor: str = None,
        capacity: int = None,
    ) -> VultrPagination[LoadBalanceForwardRule]:
        """List the forwarding rules for a Load Balancer.

        Args:
            load_balancer_id: The Loan Balance id.
            per_page: number of items requested per page. Default is 100 and Max is 500.
            cursor: cursor for paging.
            capacity: The capacity of the VultrPagination[LoadBalanceForwardRule], see `VultrPagination` for details.

        Returns:
            VultrPagination[LoadBalanceForwardRule]: A list-like object of `LoadBalanceForwardRule` object.
        """
        fetcher = partial(self._get, endpoint=f"/{load_balancer_id}/forwarding-rules")
        return VultrPagination[LoadBalanceForwardRule](
            fetcher=fetcher,
            cursor=cursor,
            page_size=per_page,
            return_type=LoadBalanceForwardRule,
            capacity=capacity,
        )

    @command
    def create_forwarding_rule(
        self,
        load_balancer_id: str,
        frontend_protocol: LoadBalanceProtocol,
        frontend_port: int,
        backend_protocol: LoadBalanceProtocol,
        backend_port: int,
    ) -> LoadBalanceForwardRule:
        """Create a new forwarding rule for a Load Balancer.

        Args:
            load_balancer_id: The Loan Balance id.
            frontend_protocol: The protocol on the Load Balancer to forward to the backend.
            frontend_port: The port number on the Load Balancer to forward to the backend.
            backend_protocol: The protocol destination on the backend server.
            backend_port: The port number destination on the backend server.

        Returns:
            LoadBalanceForwardRule: A `LoadBalanceForwardRule` object.
        """
        _json = {
            "frontend_protocol": frontend_protocol.value,
            "frontend_port": frontend_port,
            "backend_protocol": backend_protocol.value,
            "backend_port": backend_port,
        }
        resp = self._post(f"/{load_balancer_id}/forwarding-rules", json=_json)
        return LoadBalanceForwardRule.from_dict(get_only_value(resp))

    @command
    def get_forwarding_rule(self, load_balancer_id: str, forwarding_rule_id: str) -> LoadBalanceForwardRule:
        """Get information for a Forwarding Rule on a Load Balancer.

        Args:
            load_balancer_id: The Loan Balance id.
            forwarding_rule_id: The Forwarding Rule id.

        Returns:
            LoadBalanceForwardRule: A `LoadBalanceForwardRule` object.
        """
        resp = self._get(f"/{load_balancer_id}/forwarding-rules/{forwarding_rule_id}")
        return LoadBalanceForwardRule.from_dict(get_only_value(resp))

    @command
    def delete_forwarding_rule(self, load_balancer_id: str, forwarding_rule_id: str):
        """Delete a Forwarding Rule on a Load Balancer.

        Args:
            load_balancer_id: The Loan Balance id.
            forwarding_rule_id: The Forwarding Rule id.

        Returns:
            STATUS CODE: 204
            /NO CONTENT/
        """
        return self._delete(f"/{load_balancer_id}/forwarding-rules/{forwarding_rule_id}")

    @command
    def list_firewall_rules(
        self,
        load_balancer_id: str,
        per_page: int = None,
        cursor: str = None,
        capacity: int = None,
    ) -> VultrPagination[LoadBalanceFirewallRule]:
        """List the firewall rules for a Load Balancer.

        Args:
            load_balancer_id:
            per_page: number of items requested per page. Default is 100 and Max is 500.
            cursor: cursor for paging.
            capacity: The capacity of the VultrPagination[LoadBalanceFirewallRule], see `VultrPagination` for details.

        Returns:
            VultrPagination[LoadBalanceFirewallRule]: A list-like object of `LoadBalanceFirewallRule` object.
        """
        fetcher = partial(self._get, endpoint=f"/{load_balancer_id}/firewall-rules")
        return VultrPagination[LoadBalanceFirewallRule](
            fetcher=fetcher,
            cursor=cursor,
            page_size=per_page,
            return_type=LoadBalanceFirewallRule,
            capacity=capacity,
        )

    @command
    def get_firewall_rule(self, load_balancer_id: str, forwarding_rule_id: str) -> LoadBalanceFirewallRule:
        """Get a firewall rule for a Load Balancer.

        Args:
            load_balancer_id: The Loan Balance id.
            forwarding_rule_id: The firewall rule id.

        Returns:
            LoadBalanceFirewallRule: A `LoadBalanceFirewallRule` object.
        """
        resp = self._get(f"/{load_balancer_id}/firewall-rules/{forwarding_rule_id}")
        return LoadBalanceFirewallRule.from_dict(get_only_value(resp))
