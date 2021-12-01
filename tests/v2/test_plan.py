from pyvultr.base_api import SupportHttpMethod
from pyvultr.v2 import BareMetalPlanItem, Plan
from tests.v2 import BaseTestV2


class TestPlan(BaseTestV2):
    def test_list(self):
        """Test list plan."""
        with self._get("response/plans") as mock:
            _excepted_result = mock.python_body["plans"][0]
            excepted_result = Plan.from_dict(_excepted_result)

            _real_result = self.api_v2.plan.list()
            real_result: Plan = _real_result.first()

            self.assertEqual(mock.url, "https://api.vultr.com/v2/plans")
            self.assertEqual(mock.method, SupportHttpMethod.GET.value)
            self.assertEqual(real_result, excepted_result)

    def test_list_bare_metal(self):
        """Test list bare metal plan."""
        with self._get("response/plans_bare_metal") as mock:
            _excepted_result = mock.python_body["plans_metal"][0]
            excepted_result = BareMetalPlanItem.from_dict(_excepted_result)

            _real_result = self.api_v2.plan.list_bare_metal()
            real_result: BareMetalPlanItem = _real_result.first()

            self.assertEqual(mock.url, "https://api.vultr.com/v2/plans-metal")
            self.assertEqual(mock.method, SupportHttpMethod.GET.value)
            self.assertEqual(real_result, excepted_result)
