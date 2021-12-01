import uuid

from pyvultr.base_api import SupportHttpMethod
from pyvultr.v2 import LoadBalance, LoadBalanceFirewallRule, LoadBalanceForwardRule
from pyvultr.v2.enums import LoadBalanceProtocol
from tests.v2 import BaseTestV2


class TestLoanBalance(BaseTestV2):
    def test_list(self):
        """Test list loan balance."""
        with self._get("response/load_balances") as mock:
            _excepted_result = mock.python_body["load_balancers"][0]
            excepted_result = LoadBalance.from_dict(_excepted_result)

            _real_result = self.api_v2.load_balance.list(capacity=1)
            real_result: LoadBalance = _real_result.first()

            self.assertEqual(mock.url, "https://api.vultr.com/v2/load-balancers")
            self.assertEqual(mock.method, SupportHttpMethod.GET.value)
            self.assertEqual(real_result, excepted_result)

    def test_create(self):
        """Test create loan balance."""
        with self._post("response/load_balance", expected_returned=LoadBalance, status_code=201) as mock:
            excepted_result = mock.python_body

            region = "ams"
            real_result: LoadBalance = self.api_v2.load_balance.create(region=region)

            self.assertEqual(mock.url, "https://api.vultr.com/v2/load-balancers")
            self.assertEqual(mock.method, SupportHttpMethod.POST.value)
            self.assertEqual(mock.req_json["region"], region)
            self.assertEqual(mock.status_code, 201)
            self.assertEqual(real_result, excepted_result)

    def test_get(self):
        """Test get loan balance."""
        with self._get("response/load_balance", expected_returned=LoadBalance) as mock:
            excepted_result = mock.python_body

            load_balancer_id = str(uuid.uuid4())
            real_result: LoadBalance = self.api_v2.load_balance.get(load_balancer_id=load_balancer_id)

            self.assertEqual(mock.url, f"https://api.vultr.com/v2/load-balancers/{load_balancer_id}")
            self.assertEqual(mock.method, SupportHttpMethod.GET.value)
            self.assertEqual(real_result, excepted_result)

    def test_update(self):
        """Test update loan balance."""
        with self._patch(status_code=204) as mock:
            load_balancer_id = str(uuid.uuid4())
            real_result: LoadBalance = self.api_v2.load_balance.update(load_balancer_id=load_balancer_id)

            self.assertEqual(mock.url, f"https://api.vultr.com/v2/load-balancers/{load_balancer_id}")
            self.assertEqual(mock.method, SupportHttpMethod.PATCH.value)
            self.assertEqual(mock.status_code, 204)
            self.assertIsNone(real_result)

    def test_delete(self):
        """Test delete loan balance."""
        with self._delete(status_code=204) as mock:
            load_balancer_id = str(uuid.uuid4())
            self.api_v2.load_balance.delete(load_balancer_id=load_balancer_id)

            self.assertEqual(mock.url, f"https://api.vultr.com/v2/load-balancers/{load_balancer_id}")
            self.assertEqual(mock.method, SupportHttpMethod.DELETE.value)
            self.assertEqual(mock.status_code, 204)

    def test_list_forwarding_rules(self):
        """Test list forwarding rules."""
        with self._get("response/loan_balances_forwarding_rules") as mock:
            _excepted_result = mock.python_body["forwarding_rules"][0]
            excepted_result = LoadBalanceForwardRule.from_dict(_excepted_result)

            load_balancer_id = str(uuid.uuid4())
            _real_result = self.api_v2.load_balance.list_forwarding_rules(load_balancer_id, capacity=1)
            real_result: LoadBalanceForwardRule = _real_result.first()

            self.assertEqual(mock.url, f"https://api.vultr.com/v2/load-balancers/{load_balancer_id}/forwarding-rules")
            self.assertEqual(mock.method, SupportHttpMethod.GET.value)
            self.assertEqual(real_result, excepted_result)

    def test_create_forwarding_rule(self):
        """Test create forwarding rule."""
        with self._get("response/loan_balances_forwarding_rule", expected_returned=LoadBalanceForwardRule) as mock:
            excepted_result = mock.python_body

            load_balancer_id = str(uuid.uuid4())
            frontend_protocol = LoadBalanceProtocol.HTTP
            frontend_port = 80
            backend_protocol = LoadBalanceProtocol.HTTP
            backend_port = 8080
            real_result: LoadBalanceForwardRule = self.api_v2.load_balance.create_forwarding_rule(
                load_balancer_id=load_balancer_id,
                frontend_protocol=frontend_protocol,
                frontend_port=frontend_port,
                backend_protocol=backend_protocol,
                backend_port=backend_port,
            )

            self.assertEqual(mock.url, f"https://api.vultr.com/v2/load-balancers/{load_balancer_id}/forwarding-rules")
            self.assertEqual(mock.method, SupportHttpMethod.GET.value)
            self.assertEqual(mock.req_json["backend_port"], backend_port)
            self.assertEqual(mock.req_json["frontend_protocol"], frontend_protocol.value)
            self.assertEqual(real_result, excepted_result)

    def test_get_forwarding_rule(self):
        """Test get forwarding rule."""
        with self._get("response/loan_balances_forwarding_rule", expected_returned=LoadBalanceForwardRule) as mock:
            excepted_result = mock.python_body

            load_balancer_id = str(uuid.uuid4())
            forwarding_rule_id = str(uuid.uuid4())
            real_result: LoadBalanceForwardRule = self.api_v2.load_balance.get_forwarding_rule(
                load_balancer_id=load_balancer_id,
                forwarding_rule_id=forwarding_rule_id,
            )

            _url = f"https://api.vultr.com/v2/load-balancers/{load_balancer_id}/forwarding-rules/{forwarding_rule_id}"
            self.assertEqual(mock.url, _url)
            self.assertEqual(mock.method, SupportHttpMethod.GET.value)
            self.assertEqual(real_result, excepted_result)

    def test_delete_forwarding_rule(self):
        """Test delete forwarding rule."""
        with self._delete(status_code=204) as mock:
            load_balancer_id = str(uuid.uuid4())
            forwarding_rule_id = str(uuid.uuid4())
            self.api_v2.load_balance.delete_forwarding_rule(load_balancer_id, forwarding_rule_id)

            _url = f"https://api.vultr.com/v2/load-balancers/{load_balancer_id}/forwarding-rules/{forwarding_rule_id}"
            self.assertEqual(mock.url, _url)
            self.assertEqual(mock.method, SupportHttpMethod.DELETE.value)
            self.assertEqual(mock.status_code, 204)

    def test_list_firewall_rules(self):
        """Test list firewall rules."""
        with self._get("response/loan_balances_firewall_rules") as mock:
            _excepted_result = mock.python_body["firewall_rules"][0]
            excepted_result = LoadBalanceFirewallRule.from_dict(_excepted_result)

            load_balancer_id = str(uuid.uuid4())
            _real_result = self.api_v2.load_balance.list_firewall_rules(load_balancer_id, capacity=1)
            real_result: LoadBalanceFirewallRule = _real_result.first()

            self.assertEqual(mock.url, f"https://api.vultr.com/v2/load-balancers/{load_balancer_id}/firewall-rules")
            self.assertEqual(mock.method, SupportHttpMethod.GET.value)
            self.assertEqual(real_result, excepted_result)

    def test_get_firewall_rule(self):
        """Test get firewall rule."""
        with self._get("response/loan_balances_firewall_rule", expected_returned=LoadBalanceFirewallRule) as mock:
            excepted_result = mock.python_body

            load_balancer_id = str(uuid.uuid4())
            forwarding_rule_id = str(uuid.uuid4())
            real_result: LoadBalanceFirewallRule = self.api_v2.load_balance.get_firewall_rule(
                load_balancer_id=load_balancer_id,
                forwarding_rule_id=forwarding_rule_id,
            )

            _url = f"https://api.vultr.com/v2/load-balancers/{load_balancer_id}/firewall-rules/{forwarding_rule_id}"
            self.assertEqual(mock.url, _url)
            self.assertEqual(mock.method, SupportHttpMethod.GET.value)
            self.assertEqual(real_result, excepted_result)
