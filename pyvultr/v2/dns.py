from dataclasses import dataclass
from functools import partial
from typing import List, Optional
from urllib.parse import urljoin

import dacite

from pyvultr.utils import BaseDataclass, VultrPagination, get_only_value
from pyvultr.v2.base import BaseVultrV2
from pyvultr.v2.enum import DNSRecordType


@dataclass
class Domain(BaseDataclass):
    domain: str
    date_created: str
    dns_sec: str


@dataclass
class SOA(BaseDataclass):
    nsprimary: str
    email: str


@dataclass
class DNSRecord(BaseDataclass):
    id: str
    type: str
    name: str
    data: str
    priority: int
    ttl: int


class DNS(BaseVultrV2):
    """Vultr DNS API.

    Vultr offers free DNS hosting for customers' domains.
    The nameservers are on an AnyCAST network and ensure fast DNS resolution.
    When you manage your DNS through the API, you can view the results in your customer portal.

    Attributes:
        api_key: Vultr API key, we get it from env variable `VULTR_API_TOKEN` if not provided.
    """

    def __init__(self, api_key: Optional[str] = None):
        super().__init__(api_key)

    @property
    def base_url(self):
        """Get base url for all API in this section."""
        return urljoin(super().base_url, "domains")

    def list_domains(self, per_page: int = None, cursor: str = None, capacity: int = None) -> VultrPagination[Domain]:
        """List all DNS Domains in your account.

        Args:
            per_page: Number of items requested per page. Default is 100 and Max is 500.
            cursor: Cursor for paging.
            capacity: the capacity of the VultrPagination[Domain],
            see `pyvultr.utils.VultrPagination` for detail.

        Returns:
            VultrPagination[Domain]: a paginated list of `Domain`.
        """
        return VultrPagination[Domain](
            fetcher=self._get,
            cursor=cursor,
            page_size=per_page,
            return_type=Domain,
            capacity=capacity,
        )

    def create_domain(self, domain: str, ip: str = None, dns_sec: str = None) -> Domain:
        """Create a DNS Domain for `domain`. If no `ip` address is supplied a domain with no records will be created.

        Args:
            domain: Your registered DNS Domain name.
            ip: The default IP address for your DNS Domain. If omitted an empty domain zone will be created.
            dns_sec: Enable or disable DNSSEC.

        Returns:
            Domain: A `Domain` object.
        """
        _json = {
            "domain": domain,
            "ip": ip,
            "dns_sec": dns_sec,
        }
        resp = self._post(json=_json)
        return dacite.from_dict(data_class=Domain, data=get_only_value(resp))

    def get_domain(self, dns_domain: str) -> Domain:
        """Get information for the DNS Domain.

        Args:
            dns_domain: The DNS Domain.

        Returns:
            Domain: A `Domain` object.
        """
        resp = self._get(f"/{dns_domain}")
        return dacite.from_dict(data_class=Domain, data=get_only_value(resp))

    def update_domain(self, dns_domain: str, dns_sec: str):
        """Update the DNS Domain.

        Args:
            dns_domain: The DNS Domain.
            dns_sec: Enable or disable DNSSEC.

        Returns:
            STATUS CODE: 204
            /NO CONTENT/
        """
        _json = {
            "dns_sec": dns_sec,
        }
        return self._put(f"/{dns_domain}", json=_json)

    def delete_domain(self, dns_domain: str):
        """Delete the DNS Domain.

        Args:
            dns_domain: The DNS Domain.

        Returns:
            STATUS CODE: 204
            /NO CONTENT/
        """
        return self._delete(f"/{dns_domain}")

    def get_soa(self, dns_domain: str) -> SOA:
        """Get SOA information for the DNS Domain.

        Args:
            dns_domain: The DNS Domain.

        Returns:
            SOA: A `SOA` object.
        """
        resp = self._get(f"/{dns_domain}/soa")
        return dacite.from_dict(data_class=SOA, data=get_only_value(resp))

    def update_soa(self, dns_domain: str, ns_primary: str = None, email: str = None):
        """Update the SOA information for the DNS Domain.

        All attributes are optional. If not set, the attributes will retain their original values.

        Args:
            dns_domain: The DNS Domain.
            ns_primary: Set the primary nameserver.
            email: Set the contact email address.

        Returns:
            STATUS CODE: 204
            /NO CONTENT/
        """
        _json = {
            "nsprimary": ns_primary,
            "email": email,
        }
        return self._patch(f"/{dns_domain}/soa", json=_json)

    def get_dns_sec(self, dns_domain: str) -> List[str]:
        """Get the DNSSEC information for the DNS Domain.

        Args:
            dns_domain: The DNS Domain.

        Returns:
            List[str]: A list of DNSSEC information.
        """
        resp = self._get(f"/{dns_domain}/dnssec")
        return get_only_value(resp)

    def create_record(
        self,
        dns_domain: str,
        name: str,
        dns_type: DNSRecordType,
        data: str,
        ttl: int = None,
        priority: int = None,
    ) -> DNSRecord:
        """Create a DNS record.

        Args:
            dns_domain: The DNS Domain.
            name: The hostname for this DNS record.
            dns_type: The DNS record type.
            data: The DNS data for this record type.
            ttl: Time to Live in seconds.
            priority: DNS priority. Does not apply to all record types. (Only required for MX and SRV).

        Returns:
            DNSRecord: A `DNSRecord` object.
        """
        _json = {
            "name": name,
            "type": dns_type.value,
            "data": data,
            "ttl": ttl,
            "priority": priority,
        }
        resp = self._post(f"/{dns_domain}/records", json=_json)
        return dacite.from_dict(data_class=DNSRecord, data=get_only_value(resp))

    def list_records(
        self,
        dns_domain: str,
        per_page: int = None,
        cursor: str = None,
        capacity: int = None,
    ) -> VultrPagination[DNSRecord]:
        """Get the DNS records for the Domain.

        Args:
            dns_domain: The DNS Domain.
            per_page: Number of items requested per page. Default is 100 and Max is 500.
            cursor: Cursor for paging.
            capacity: the capacity of the VultrPagination[DNSRecord],
            see `pyvultr.utils.VultrPagination` for detail.

        Returns:
            VultrPagination[DNSRecord]: a paginated list of `DNSRecord`.
        """
        fetcher = partial(self._get, endpoint=f"/{dns_domain}/records")
        return VultrPagination[DNSRecord](
            fetcher=fetcher,
            cursor=cursor,
            page_size=per_page,
            return_type=DNSRecord,
            capacity=capacity,
        )

    def get_record(self, dns_domain: str, record_id: str) -> DNSRecord:
        """Get information for a DNS Record.

        Args:
            dns_domain: The DNS Domain.
            record_id: The DNS Record id.

        Returns:
            DNSRecord: A `DNSRecord` object.
        """
        reps = self._get(f"/{dns_domain}/records/{record_id}")
        return dacite.from_dict(data_class=DNSRecord, data=get_only_value(reps))

    def update_record(
        self,
        dns_domain: str,
        record_id: str,
        name: str = None,
        data: str = None,
        ttl: int = None,
        priority: int = None,
    ):
        """Update the information for a DNS record.

        All attributes are optional. If not set, the attributes will retain their original values.

        Args:
            dns_domain: The DNS Domain.
            record_id: The DNS Record id.
            name: The hostname for this DNS record.
            data: The DNS data for this record type.
            ttl: Time to Live in seconds.
            priority: DNS priority. Does not apply to all record types.

        Returns:
            STATUS CODE: 204
            /NO CONTENT/
        """
        _json = {
            "name": name,
            "data": data,
            "ttl": ttl,
            "priority": priority,
        }
        return self._patch(f"/{dns_domain}/records/{record_id}", json=_json)

    def delete_record(self, dns_domain: str, record_id: str):
        """Delete the DNS record.

        Args:
            dns_domain: The DNS Domain.
            record_id: The DNS Record id.

        Returns:
            STATUS CODE: 204
            /NO CONTENT/
        """
        return self._delete(f"/{dns_domain}/records/{record_id}")
