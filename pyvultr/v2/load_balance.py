from dataclasses import dataclass
from functools import partial
from typing import Dict, List, Optional
from urllib.parse import urljoin

from pyvultr.utils import BaseDataclass, VultrPagination, get_only_value, merge_args

from .base import BaseVultrV2
from .enum import Protocol


@dataclass
class LoadBalanceGenericInfo(BaseDataclass):
    balancing_algorithm: str
    ssl_redirect: bool
    sticky_sessions: Dict
    proxy_protocol: bool
    private_network: str


@dataclass
class LoadBalanceHealthCheck(BaseDataclass):
    protocol: str
    port: int
    path: str
    check_interval: int
    response_timeout: int
    unhealthy_threshold: int
    healthy_threshold: int


@dataclass
class LoadBalanceForwardRule(BaseDataclass):
    id: str
    frontend_protocol: str
    frontend_port: int
    backend_protocol: str
    backend_port: int


@dataclass
class LoadBalanceFirewallRule(BaseDataclass):
    id: str
    port: int
    source: str
    ip_type: str


@dataclass
class LoadBalanceItem(BaseDataclass):
    id: str
    date_created: str
    region: str
    label: str
    status: str
    ipv4: str
    ipv6: str
    generic_info: LoadBalanceGenericInfo
    health_check: LoadBalanceHealthCheck
    has_ssl: bool
    forwarding_rules: List[LoadBalanceForwardRule]
    instances: List[str]
    firewall_rules: List[LoadBalanceFirewallRule]


class LoadBalance(BaseVultrV2):
    """Vultr LoanBalance API.

    Reference: https://www.vultr.com/zh/api/#tag/load-balancer

    Load Balancers sit in front of your application and distribute incoming traffic across multiple Instances.
    When you control the load balancer via the API, you can inspect the results in the customer portal.

    Attributes:
        api_key: Vultr API key, we get it from env variable `$ENV_TOKEN_NAME` if not provided.
    """

    def __init__(self, api_key: Optional[str] = None):
        super().__init__(api_key)

    @property
    def base_url(self):
        """Get base url for all API in this section."""
        return urljoin(super().base_url, "load-balancers")

    def list(self, per_page: int = None, cursor: str = None, capacity: int = None) -> VultrPagination[LoadBalanceItem]:
        """List the Load Balancers in your account.

        Args:
            per_page: Number of items requested per page. Default is 100 and Max is 500.
            cursor: Cursor for paging.
            capacity: The capacity of the VultrPagination[LoadBalanceItem], see `VultrPagination` for details.

        Returns:
            VultrPagination[LoadBalanceItem]: A list-like object of `LoadBalanceItem` object.
        """
        return VultrPagination[LoadBalanceItem](
            fetcher=self._get,
            cursor=cursor,
            page_size=per_page,
            return_type=LoadBalanceItem,
            capacity=capacity,
        )

    def create(self, region: str, **kwargs) -> LoadBalanceItem:
        """Create a new Load Balancer in a particular `region`.

        Args:
            region: The Region id to create this Load Balancer.
            **kwargs: New LoanBalance parameters.

        Returns:
            LoadBalanceItem: The LoadBalanceItem object.
        """
        _fixed_kwargs = {"region": region}
        resp = self._post(json=merge_args(kwargs, _fixed_kwargs))
        return LoadBalanceItem.from_dict(get_only_value(resp))

    def get(self, load_balancer_id: str) -> LoadBalanceItem:
        """Get information for a Load Balancer.

        Args:
            load_balancer_id: The Loan Balance id.

        Returns:
            LoadBalanceItem: The LoadBalanceItem object.
        """
        resp = self._get(f"/{load_balancer_id}")
        return LoadBalanceItem.from_dict(get_only_value(resp))

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

    def delete(self, load_balancer_id: str):
        """Delete a Load Balancer.

        Args:
            load_balancer_id: The Loan Balance id.

        Returns:
            STATUS CODE: 204
            /NO CONTENT/
        """
        return self._delete(f"/{load_balancer_id}")

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

    def create_forwarding_rule(
        self,
        load_balancer_id: str,
        frontend_protocol: Protocol,
        frontend_port: int,
        backend_protocol: Protocol,
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
