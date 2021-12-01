import uuid

from pyvultr.base_api import SupportHttpMethod
from pyvultr.v2 import FirewallGroup, FirewallRule
from pyvultr.v2.enums import FirewallProtocol, IPType
from tests.v2 import BaseTestV2


class TestFirewall(BaseTestV2):
    def test_list_groups(self):
        """Test list groups."""
        with self._get("response/firewalls") as mock:
            _excepted_result = mock.python_body["firewall_groups"][0]
            excepted_result = FirewallGroup.from_dict(_excepted_result)

            _real_result = self.api_v2.firewall.list_groups()
            real_result: FirewallGroup = _real_result.first()

            self.assertEqual(mock.url, "https://api.vultr.com/v2/firewalls")
            self.assertEqual(mock.method, SupportHttpMethod.GET.value)
            self.assertEqual(real_result, excepted_result)

    def test_create_group(self):
        """Test create group."""
        with self._post("response/firewall", expected_returned=FirewallGroup, status_code=201) as mock:
            excepted_result = mock.python_body

            description = "test_description"
            real_result: FirewallGroup = self.api_v2.firewall.create_group(description=description)

            self.assertEqual(mock.url, "https://api.vultr.com/v2/firewalls")
            self.assertEqual(mock.method, SupportHttpMethod.POST.value)
            self.assertEqual(mock.status_code, 201)
            self.assertEqual(real_result, excepted_result)

    def test_get_group(self):
        """Test get group."""
        with self._get("response/firewall", expected_returned=FirewallGroup) as mock:
            excepted_result = mock.python_body

            firewall_group_id = str(uuid.uuid4())
            real_result: FirewallGroup = self.api_v2.firewall.get_group(firewall_group_id=firewall_group_id)

            self.assertEqual(mock.url, f"https://api.vultr.com/v2/firewalls/{firewall_group_id}")
            self.assertEqual(mock.method, SupportHttpMethod.GET.value)
            self.assertEqual(real_result, excepted_result)

    def test_update_group(self):
        """Test update group."""
        with self._put(status_code=204) as mock:
            description = "test_description_1"
            firewall_group_id = str(uuid.uuid4())
            real_result = self.api_v2.firewall.update_group(firewall_group_id, description=description)

            self.assertEqual(mock.url, f"https://api.vultr.com/v2/firewalls/{firewall_group_id}")
            self.assertEqual(mock.method, SupportHttpMethod.PUT.value)
            self.assertEqual(mock.status_code, 204)
            self.assertIsNone(real_result)

    def test_delete_group(self):
        """Test delete group."""
        with self._delete(status_code=204) as mock:
            firewall_group_id = str(uuid.uuid4())
            self.api_v2.firewall.delete_group(firewall_group_id=firewall_group_id)

            target_url = f"https://api.vultr.com/v2/firewalls/{firewall_group_id}"
            self.assertEqual(mock.url, target_url)
            self.assertEqual(mock.method, SupportHttpMethod.DELETE.value)
            self.assertEqual(mock.status_code, 204)

    def test_list_rules(self):
        """Test list rules."""
        with self._get("response/firewall_rules") as mock:
            _excepted_result = mock.python_body["firewall_rules"][0]
            excepted_result = FirewallRule.from_dict(_excepted_result)

            firewall_group_id = str(uuid.uuid4())
            _real_result = self.api_v2.firewall.list_rules(firewall_group_id=firewall_group_id)
            real_result: FirewallRule = _real_result.first()

            self.assertEqual(mock.url, f"https://api.vultr.com/v2/firewalls/{firewall_group_id}/rules")
            self.assertEqual(mock.method, SupportHttpMethod.GET.value)
            self.assertEqual(real_result, excepted_result)

    def test_create_rule(self):
        """Test create rule."""
        with self._post("response/firewall_rule", expected_returned=FirewallRule, status_code=201) as mock:
            excepted_result = mock.python_body

            firewall_group_id = str(uuid.uuid4())
            protocol = FirewallProtocol.AH
            ip_type = IPType.V4
            subnet = "192.0.2.0"
            subnet_size = 24
            real_result: FirewallRule = self.api_v2.firewall.create_rule(
                firewall_group_id=firewall_group_id,
                protocol=protocol,
                ip_type=ip_type,
                subnet=subnet,
                subnet_size=subnet_size,
            )

            self.assertEqual(mock.url, f"https://api.vultr.com/v2/firewalls/{firewall_group_id}/rules")
            self.assertEqual(mock.method, SupportHttpMethod.POST.value)
            self.assertEqual(mock.req_json["protocol"], protocol.value)
            self.assertEqual(mock.req_json["ip_type"], ip_type.value)
            self.assertEqual(mock.req_json["subnet"], subnet)
            self.assertEqual(mock.req_json["subnet_size"], subnet_size)
            self.assertEqual(mock.status_code, 201)
            self.assertEqual(real_result, excepted_result)

    def test_get_rule(self):
        """Test get rule."""
        with self._get("response/firewall_rule", expected_returned=FirewallRule) as mock:
            excepted_result = mock.python_body

            firewall_group_id = str(uuid.uuid4())
            firewall_rule_id = str(uuid.uuid4())
            real_result: FirewallRule = self.api_v2.firewall.get_rule(
                firewall_group_id=firewall_group_id,
                firewall_rule_id=firewall_rule_id,
            )

            target_url = f"https://api.vultr.com/v2/firewalls/{firewall_group_id}/rules/{firewall_rule_id}"
            self.assertEqual(mock.url, target_url)
            self.assertEqual(mock.method, SupportHttpMethod.GET.value)
            self.assertEqual(real_result, excepted_result)

    def test_delete_rule(self):
        """Test delete rule."""
        with self._delete(status_code=204) as mock:
            firewall_group_id = str(uuid.uuid4())
            firewall_rule_id = str(uuid.uuid4())
            self.api_v2.firewall.delete_rule(firewall_group_id=firewall_group_id, firewall_rule_id=firewall_rule_id)

            target_url = f"https://api.vultr.com/v2/firewalls/{firewall_group_id}/rules/{firewall_rule_id}"
            self.assertEqual(mock.url, target_url)
            self.assertEqual(mock.method, SupportHttpMethod.DELETE.value)
            self.assertEqual(mock.status_code, 204)
