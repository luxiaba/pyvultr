from pyvultr.base_api import SupportHttpMethod
from pyvultr.v2 import OS
from tests.v2 import BaseTestV2


class TestOperatingSystem(BaseTestV2):
    def test_list(self):
        """Test list os."""
        with self._get("response/operating_systems") as mock:
            _excepted_result = mock.python_body["os"][0]
            excepted_result = OS.from_dict(_excepted_result)

            _real_result = self.api_v2.operating_system.list(capacity=1)
            real_result: OS = _real_result.first()

            self.assertEqual(mock.url, "https://api.vultr.com/v2/os")
            self.assertEqual(mock.method, SupportHttpMethod.GET.value)
            self.assertEqual(real_result, excepted_result)
