import uuid

from pyvultr.base_api import SupportHttpMethod
from pyvultr.v2 import ReservedIP
from pyvultr.v2.enums import IPType
from tests.v2 import BaseTestV2


class TestReservedIP(BaseTestV2):
    def test_list(self):
        """Test list reserved ips."""
        with self._get("response/reserved_ips") as mock:
            _excepted_result = mock.python_body["reserved_ips"][0]
            excepted_result = ReservedIP.from_dict(_excepted_result)

            _real_result = self.api_v2.reserved_ip.list(capacity=1)
            real_result: ReservedIP = _real_result.first()

            self.assertEqual(mock.url, "https://api.vultr.com/v2/reserved-ips")
            self.assertEqual(mock.method, SupportHttpMethod.GET.value)
            self.assertEqual(real_result, excepted_result)

    def test_create(self):
        """Test create reserved ip."""
        with self._post("response/reserved_ip", expected_returned=ReservedIP, status_code=201) as mock:
            excepted_result = mock.python_body

            region = "ams"
            ip_type = IPType.V4
            label = "test_label"
            real_result: ReservedIP = self.api_v2.reserved_ip.create(region=region, ip_type=ip_type, label=label)

            self.assertEqual(mock.url, "https://api.vultr.com/v2/reserved-ips")
            self.assertEqual(mock.method, SupportHttpMethod.POST.value)
            self.assertEqual(mock.req_json["region"], region)
            self.assertEqual(mock.req_json["ip_type"], ip_type.value)
            self.assertEqual(mock.status_code, 201)
            self.assertEqual(real_result, excepted_result)

    def test_get(self):
        """Test get reserved ip."""
        with self._get("response/reserved_ip", expected_returned=ReservedIP) as mock:
            excepted_result = mock.python_body

            reserved_ip = "127.0.0.1"
            real_result: ReservedIP = self.api_v2.reserved_ip.get(reserved_ip=reserved_ip)

            self.assertEqual(mock.url, f"https://api.vultr.com/v2/reserved-ips/{reserved_ip}")
            self.assertEqual(mock.method, SupportHttpMethod.GET.value)
            self.assertEqual(real_result, excepted_result)

    def test_attach(self):
        """Test attach reserved ip."""
        with self._post(status_code=204) as mock:
            reserved_ip = "127.0.0.1"
            instance_id = str(uuid.uuid4())
            self.api_v2.reserved_ip.attach(reserved_ip=reserved_ip, instance_id=instance_id)

            self.assertEqual(mock.url, f"https://api.vultr.com/v2/reserved-ips/{reserved_ip}/attach")
            self.assertEqual(mock.method, SupportHttpMethod.POST.value)
            self.assertEqual(mock.req_json["instance_id"], instance_id)
            self.assertEqual(mock.status_code, 204)

    def test_detach(self):
        """Test detach reserved ip."""
        with self._post(status_code=204) as mock:
            reserved_ip = "127.0.0.1"
            self.api_v2.reserved_ip.detach(reserved_ip)

            self.assertEqual(mock.url, f"https://api.vultr.com/v2/reserved-ips/{reserved_ip}/detach")
            self.assertEqual(mock.method, SupportHttpMethod.POST.value)
            self.assertEqual(mock.status_code, 204)

    def test_delete(self):
        """Test delete reserved ip."""
        with self._delete(status_code=204) as mock:
            reserved_ip = "127.0.0.1"
            self.api_v2.reserved_ip.delete(reserved_ip=reserved_ip)

            self.assertEqual(mock.url, f"https://api.vultr.com/v2/reserved-ips/{reserved_ip}")
            self.assertEqual(mock.method, SupportHttpMethod.DELETE.value)
            self.assertEqual(mock.status_code, 204)
