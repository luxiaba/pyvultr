import uuid
from typing import Dict

from pyvultr.base_api import SupportHttpMethod
from pyvultr.v2 import BandwidthItem, BareMetal, BareMetalAvailableUpgrade, BareMetalVNC, IPv4Item, IPv6Item, UserData
from tests.v2 import BaseTestV2


class TestBareMetal(BaseTestV2):
    def test_list(self):
        """Test list bare metal."""
        with self._get("response/bare_metal_list") as mock:
            _excepted_result = mock.python_body["bare_metals"][0]
            excepted_result = BareMetal.from_dict(_excepted_result)

            _real_result = self.api_v2.bare_metal.list(capacity=1)
            real_result: BareMetal = _real_result.first()

            self.assertEqual(mock.url, "https://api.vultr.com/v2/bare-metals")
            self.assertEqual(mock.method, SupportHttpMethod.GET.value)
            self.assertEqual(real_result, excepted_result)

    def test_get(self):
        """Test get bare metal."""
        with self._get("response/bare_metal", expected_returned=BareMetal) as mock:
            excepted_result = mock.python_body

            real_result: BareMetal = self.api_v2.bare_metal.get(excepted_result.id)

            self.assertEqual(mock.url, f"https://api.vultr.com/v2/bare-metals/{excepted_result.id}")
            self.assertEqual(mock.method, SupportHttpMethod.GET.value)
            self.assertEqual(real_result, excepted_result)

    def test_update(self):
        """Test update bare metal."""
        with self._patch("response/bare_metal", expected_returned=BareMetal) as mock:
            excepted_result = mock.python_body

            real_result: BareMetal = self.api_v2.bare_metal.update(excepted_result.id, label="Example Bare Metal")

            self.assertEqual(mock.url, f"https://api.vultr.com/v2/bare-metals/{excepted_result.id}")
            self.assertEqual(mock.method, SupportHttpMethod.PATCH.value)
            self.assertEqual(real_result, excepted_result)

    def test_delete(self):
        """Test delete bare metal."""
        with self._delete(status_code=204) as mock:
            bare_metal_id = str(uuid.uuid4())
            resp = self.api_v2.bare_metal.delete(bare_metal_id)

            self.assertEqual(mock.url, f"https://api.vultr.com/v2/bare-metals/{bare_metal_id}")
            self.assertEqual(mock.method, SupportHttpMethod.DELETE.value)
            self.assertEqual(mock.status_code, 204)
            self.assertIsNone(resp)

    def test_list_ipv4s(self):
        """Test list IPv4 of bare metal."""
        with self._get("response/bare_metal_ipv4s") as mock:
            _excepted_result = mock.python_body["ipv4s"][0]
            excepted_result = IPv4Item.from_dict(_excepted_result)

            bare_metal_id = str(uuid.uuid4())
            _real_result = self.api_v2.bare_metal.list_ipv4s(bare_metal_id, capacity=1)
            real_result = _real_result.first()

            self.assertEqual(mock.url, f"https://api.vultr.com/v2/bare-metals/{bare_metal_id}/ipv4")
            self.assertEqual(mock.method, SupportHttpMethod.GET.value)
            self.assertEqual(real_result, excepted_result)

    def test_list_ipv6s(self):
        """Test list IPv6 of bare metal."""
        with self._get("response/bare_metal_ipv6s") as mock:
            _excepted_result = mock.python_body["ipv6s"][0]
            excepted_result = IPv6Item.from_dict(_excepted_result)

            bare_metal_id = str(uuid.uuid4())
            _real_result = self.api_v2.bare_metal.list_ipv6s(bare_metal_id, capacity=1)
            real_result = _real_result.first()

            self.assertEqual(mock.url, f"https://api.vultr.com/v2/bare-metals/{bare_metal_id}/ipv6")
            self.assertEqual(mock.method, SupportHttpMethod.GET.value)
            self.assertEqual(real_result, excepted_result)

    def test_get_bandwidth(self):
        """Test get bandwidth of bare metal."""
        with self._get("response/bare_metal_bandwidth") as mock:
            _excepted_result: Dict = mock.python_body["bandwidth"]
            excepted_result = {_date: BandwidthItem.from_dict(item) for _date, item in _excepted_result.items()}

            bare_metal_id = str(uuid.uuid4())
            real_result: Dict[str, BandwidthItem] = self.api_v2.bare_metal.get_bandwidth(bare_metal_id)

            self.assertEqual(mock.url, f"https://api.vultr.com/v2/bare-metals/{bare_metal_id}/bandwidth")
            self.assertEqual(mock.method, SupportHttpMethod.GET.value)
            self.assertEqual(real_result, excepted_result)

    def test_start(self):
        """Test start a bare metal."""
        with self._post(status_code=204) as mock:

            bare_metal_id = str(uuid.uuid4())
            resp = self.api_v2.bare_metal.start(bare_metal_id)

            self.assertEqual(mock.url, f"https://api.vultr.com/v2/bare-metals/{bare_metal_id}/start")
            self.assertEqual(mock.method, SupportHttpMethod.POST.value)
            self.assertEqual(mock.status_code, 204)
            self.assertIsNone(resp)

    def test_reboot(self):
        """Test reboot a bare metal."""
        with self._post(status_code=204) as mock:

            bare_metal_id = str(uuid.uuid4())
            resp = self.api_v2.bare_metal.reboot(bare_metal_id)

            self.assertEqual(mock.url, f"https://api.vultr.com/v2/bare-metals/{bare_metal_id}/reboot")
            self.assertEqual(mock.method, SupportHttpMethod.POST.value)
            self.assertEqual(mock.status_code, 204)
            self.assertIsNone(resp)

    def test_halt(self):
        """Test halt a bare metal."""
        with self._post(status_code=204) as mock:

            bare_metal_id = str(uuid.uuid4())
            resp = self.api_v2.bare_metal.halt(bare_metal_id)

            self.assertEqual(mock.url, f"https://api.vultr.com/v2/bare-metals/{bare_metal_id}/halt")
            self.assertEqual(mock.method, SupportHttpMethod.POST.value)
            self.assertEqual(mock.status_code, 204)
            self.assertIsNone(resp)

    def test_reinstall(self):
        """Test reinstall a bare metal."""
        with self._post("response/bare_metal", status_code=202, expected_returned=BareMetal) as mock:
            excepted_result: BareMetal = mock.python_body

            real_result: BareMetal = self.api_v2.bare_metal.reinstall(excepted_result.id)

            self.assertEqual(mock.url, f"https://api.vultr.com/v2/bare-metals/{excepted_result.id}/reinstall")
            self.assertEqual(mock.method, SupportHttpMethod.POST.value)
            self.assertEqual(mock.status_code, 202)
            self.assertEqual(real_result, excepted_result)

    def test_batch_start(self):
        """Test batch start bare metals."""
        with self._post(status_code=204) as mock:

            bare_metal_ids = [str(uuid.uuid4()) for _ in range(10)]
            resp = self.api_v2.bare_metal.batch_start(bare_metal_ids)

            self.assertEqual(mock.url, "https://api.vultr.com/v2/bare-metals/start")
            self.assertEqual(mock.method, SupportHttpMethod.POST.value)
            self.assertEqual(mock.req_json, {"baremetal_ids": bare_metal_ids})
            self.assertEqual(mock.status_code, 204)
            self.assertIsNone(resp)

    def test_batch_reboot(self):
        """Test reboot start bare metals."""
        with self._post(status_code=204) as mock:

            bare_metal_ids = [str(uuid.uuid4()) for _ in range(10)]
            resp = self.api_v2.bare_metal.batch_reboot(bare_metal_ids)

            self.assertEqual(mock.url, "https://api.vultr.com/v2/bare-metals/reboot")
            self.assertEqual(mock.method, SupportHttpMethod.POST.value)
            self.assertEqual(mock.req_json, {"baremetal_ids": bare_metal_ids})
            self.assertEqual(mock.status_code, 204)
            self.assertIsNone(resp)

    def test_batch_halt(self):
        """Test halt start bare metals."""
        with self._post(status_code=204) as mock:

            bare_metal_ids = [str(uuid.uuid4()) for _ in range(10)]
            resp = self.api_v2.bare_metal.batch_halt(bare_metal_ids)

            self.assertEqual(mock.url, "https://api.vultr.com/v2/bare-metals/halt")
            self.assertEqual(mock.method, SupportHttpMethod.POST.value)
            self.assertEqual(mock.req_json, {"baremetal_ids": bare_metal_ids})
            self.assertEqual(mock.status_code, 204)
            self.assertIsNone(resp)

    def test_get_user_data(self):
        """Test get user data of bare metal."""
        with self._get("response/bare_metal_user_data", expected_returned=UserData) as mock:
            excepted_result: UserData = mock.python_body

            bare_metal_id = str(uuid.uuid4())
            real_result: UserData = self.api_v2.bare_metal.get_user_data(bare_metal_id)

            self.assertEqual(mock.url, f"https://api.vultr.com/v2/bare-metals/{bare_metal_id}/user-data")
            self.assertEqual(mock.method, SupportHttpMethod.GET.value)
            self.assertEqual(real_result, excepted_result)

    def test_list_upgrades(self):
        """Test list available upgrades of bare metal."""
        with self._get("response/bare_metal_upgrades", expected_returned=BareMetalAvailableUpgrade) as mock:
            excepted_result: BareMetalAvailableUpgrade = mock.python_body

            bare_metal_id = str(uuid.uuid4())
            real_result: BareMetalAvailableUpgrade = self.api_v2.bare_metal.list_upgrades(bare_metal_id)

            self.assertEqual(mock.url, f"https://api.vultr.com/v2/bare-metals/{bare_metal_id}/upgrades")
            self.assertEqual(mock.method, SupportHttpMethod.GET.value)
            self.assertEqual(real_result, excepted_result)

    def test_get_vnc(self):
        """Test get VNC of bare metal."""
        with self._get("response/bare_metal_vnc", expected_returned=BareMetalVNC) as mock:
            excepted_result: BareMetalVNC = mock.python_body

            bare_metal_id = str(uuid.uuid4())
            real_result: BareMetalVNC = self.api_v2.bare_metal.get_vnc(bare_metal_id)

            self.assertEqual(mock.url, f"https://api.vultr.com/v2/bare-metals/{bare_metal_id}/vnc")
            self.assertEqual(mock.method, SupportHttpMethod.GET.value)
            self.assertEqual(real_result, excepted_result)
