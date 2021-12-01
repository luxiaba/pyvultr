import uuid
from typing import List

from pyvultr.base_api import SupportHttpMethod
from pyvultr.utils import get_only_value
from pyvultr.v2 import SOA, DNSRecord, Domain
from pyvultr.v2.enum import DNSRecordType
from tests.v2 import BaseTestV2


class TestDNS(BaseTestV2):
    def test_list_domains(self):
        """Test list domains."""
        with self._get("response/domains") as mock:
            _excepted_result = mock.python_body["domains"][0]
            excepted_result = Domain.from_dict(_excepted_result)

            _real_result = self.api_v2.dns.list_domains()
            real_result: Domain = _real_result.first()

            self.assertEqual(mock.url, "https://api.vultr.com/v2/domains")
            self.assertEqual(mock.method, SupportHttpMethod.GET.value)
            self.assertEqual(real_result, excepted_result)

    def test_create_domain(self):
        """Test create domain."""
        with self._post("response/domain", expected_returned=Domain) as mock:
            excepted_result = mock.python_body

            domain = "a.example.com"
            dns_sec = "disabled"
            real_result: Domain = self.api_v2.dns.create_domain(domain=domain, dns_sec=dns_sec)

            self.assertEqual(mock.url, "https://api.vultr.com/v2/domains")
            self.assertEqual(mock.method, SupportHttpMethod.POST.value)
            self.assertEqual(mock.req_json["domain"], domain)
            self.assertEqual(mock.req_json["dns_sec"], dns_sec)
            self.assertEqual(real_result, excepted_result)

    def test_get_domain(self):
        """Test get domain."""
        with self._get("response/domain", expected_returned=Domain) as mock:
            excepted_result = mock.python_body

            dns_domain = "a.example.com"
            real_result: Domain = self.api_v2.dns.get_domain(dns_domain=dns_domain)

            self.assertEqual(mock.url, f"https://api.vultr.com/v2/domains/{dns_domain}")
            self.assertEqual(mock.method, SupportHttpMethod.GET.value)
            self.assertEqual(real_result, excepted_result)

    def test_update_domain(self):
        """Test update domain."""
        with self._put(status_code=204) as mock:
            dns_domain = "a.example.com"
            dns_sec = "enabled"
            self.api_v2.dns.update_domain(dns_domain=dns_domain, dns_sec=dns_sec)

            self.assertEqual(mock.url, f"https://api.vultr.com/v2/domains/{dns_domain}")
            self.assertEqual(mock.method, SupportHttpMethod.PUT.value)
            self.assertEqual(mock.req_json["dns_sec"], dns_sec)
            self.assertEqual(mock.status_code, 204)

    def test_delete_domain(self):
        """Test delete domain."""
        with self._delete(status_code=204) as mock:
            dns_domain = "b.example.com"
            self.api_v2.dns.delete_domain(dns_domain=dns_domain)

            self.assertEqual(mock.url, f"https://api.vultr.com/v2/domains/{dns_domain}")
            self.assertEqual(mock.method, SupportHttpMethod.DELETE.value)
            self.assertEqual(mock.status_code, 204)

    def test_get_soa(self):
        """Test get soa."""
        with self._get("response/domain_soa", expected_returned=SOA) as mock:
            excepted_result = mock.python_body

            dns_domain = "f.example.com"
            real_result: DNSRecord = self.api_v2.dns.get_soa(dns_domain=dns_domain)

            self.assertEqual(mock.url, f"https://api.vultr.com/v2/domains/{dns_domain}/soa")
            self.assertEqual(mock.method, SupportHttpMethod.GET.value)
            self.assertEqual(real_result, excepted_result)

    def test_update_soa(self):
        """Test update soa."""
        with self._patch(status_code=204) as mock:
            dns_domain = "b.example.com"
            email = "me@example.com"
            self.api_v2.dns.update_soa(dns_domain=dns_domain, email=email)

            self.assertEqual(mock.url, f"https://api.vultr.com/v2/domains/{dns_domain}/soa")
            self.assertEqual(mock.method, SupportHttpMethod.PATCH.value)
            self.assertEqual(mock.req_json["email"], email)
            self.assertEqual(mock.status_code, 204)

    def test_get_dns_sec(self):
        """Test get dns_sec."""
        with self._get("response/domain_dns_sec") as mock:
            excepted_result: List[str] = get_only_value(mock.python_body)

            dns_domain = "b.example.com"
            real_result: List[str] = self.api_v2.dns.get_dns_sec(dns_domain=dns_domain)

            self.assertEqual(mock.url, f"https://api.vultr.com/v2/domains/{dns_domain}/dnssec")
            self.assertEqual(mock.method, SupportHttpMethod.GET.value)
            self.assertEqual(real_result, excepted_result)

    def test_create_record(self):
        """Test create record."""
        with self._post("response/domain_record", expected_returned=DNSRecord) as mock:
            excepted_result = mock.python_body

            dns_domain = "d.example.com"
            name = "test_name"
            dns_type = DNSRecordType.A
            data = "127.0.0.1"
            real_result: DNSRecord = self.api_v2.dns.create_record(
                dns_domain=dns_domain,
                name=name,
                dns_type=dns_type,
                data=data,
            )

            self.assertEqual(mock.url, f"https://api.vultr.com/v2/domains/{dns_domain}/records")
            self.assertEqual(mock.method, SupportHttpMethod.POST.value)
            self.assertEqual(mock.req_json["name"], name)
            self.assertEqual(mock.req_json["type"], dns_type.value)
            self.assertEqual(mock.req_json["data"], data)
            self.assertEqual(real_result, excepted_result)

    def test_list_records(self):
        """Test list records."""
        with self._get("response/domains_records") as mock:
            _excepted_result = mock.python_body["records"][0]
            excepted_result = DNSRecord.from_dict(_excepted_result)

            dns_domain = "e.example.com"
            _real_result = self.api_v2.dns.list_records(dns_domain=dns_domain)
            real_result: DNSRecord = _real_result.first()

            self.assertEqual(mock.url, f"https://api.vultr.com/v2/domains/{dns_domain}/records")
            self.assertEqual(mock.method, SupportHttpMethod.GET.value)
            self.assertEqual(real_result, excepted_result)

    def test_get_record(self):
        """Test get record."""
        with self._get("response/domain_record", expected_returned=DNSRecord) as mock:
            excepted_result = mock.python_body

            dns_domain = "c.example.com"
            record_id = str(uuid.uuid4())
            real_result: DNSRecord = self.api_v2.dns.get_record(dns_domain=dns_domain, record_id=record_id)

            self.assertEqual(mock.url, f"https://api.vultr.com/v2/domains/{dns_domain}/records/{record_id}")
            self.assertEqual(mock.method, SupportHttpMethod.GET.value)
            self.assertEqual(real_result, excepted_result)

    def test_update_record(self):
        """Test update record."""
        with self._patch(status_code=204) as mock:
            dns_domain = "b.example.com"
            record_id = str(uuid.uuid4())
            ttl = 1800
            self.api_v2.dns.update_record(dns_domain=dns_domain, record_id=record_id, ttl=ttl)

            self.assertEqual(mock.url, f"https://api.vultr.com/v2/domains/{dns_domain}/records/{record_id}")
            self.assertEqual(mock.method, SupportHttpMethod.PATCH.value)
            self.assertEqual(mock.req_json["ttl"], ttl)
            self.assertEqual(mock.status_code, 204)

    def test_delete_record(self):
        """Test delete record."""
        with self._delete(status_code=204) as mock:
            dns_domain = "b.example.com"
            record_id = str(uuid.uuid4())
            self.api_v2.dns.delete_record(dns_domain=dns_domain, record_id=record_id)

            self.assertEqual(mock.url, f"https://api.vultr.com/v2/domains/{dns_domain}/records/{record_id}")
            self.assertEqual(mock.method, SupportHttpMethod.DELETE.value)
            self.assertEqual(mock.status_code, 204)
