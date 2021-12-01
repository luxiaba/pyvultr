import uuid

from pyvultr.base_api import SupportHttpMethod
from pyvultr.v2 import PrivateNetworkItem
from tests.v2 import BaseTestV2


class TestPrivateNetwork(BaseTestV2):
    def test_list(self):
        """Test list networks."""
        with self._get("response/private_networks") as mock:
            _excepted_result = mock.python_body["networks"][0]
            excepted_result = PrivateNetworkItem.from_dict(_excepted_result)

            _real_result = self.api_v2.private_network.list(capacity=1)
            real_result: PrivateNetworkItem = _real_result.first()

            self.assertEqual(mock.url, "https://api.vultr.com/v2/private-networks")
            self.assertEqual(mock.method, SupportHttpMethod.GET.value)
            self.assertEqual(real_result, excepted_result)

    def test_create(self):
        """Test create network."""
        with self._post("response/private_network", expected_returned=PrivateNetworkItem, status_code=201) as mock:
            excepted_result = mock.python_body

            region = "ams"
            description = "test_description"
            real_result: PrivateNetworkItem = self.api_v2.private_network.create(region=region, description=description)

            self.assertEqual(mock.url, "https://api.vultr.com/v2/private-networks")
            self.assertEqual(mock.method, SupportHttpMethod.POST.value)
            self.assertEqual(mock.req_json["region"], region)
            self.assertEqual(mock.req_json["description"], description)
            self.assertEqual(mock.status_code, 201)
            self.assertEqual(real_result, excepted_result)

    def test_get(self):
        """Test get network."""
        with self._get("response/private_network", expected_returned=PrivateNetworkItem) as mock:
            excepted_result = mock.python_body

            network_id = str(uuid.uuid4())
            real_result: PrivateNetworkItem = self.api_v2.private_network.get(network_id=network_id)

            self.assertEqual(mock.url, f"https://api.vultr.com/v2/private-networks/{network_id}")
            self.assertEqual(mock.method, SupportHttpMethod.GET.value)
            self.assertEqual(real_result, excepted_result)

    def test_update(self):
        """Test update network."""
        with self._patch(status_code=204) as mock:
            network_id = str(uuid.uuid4())
            description = "test_description_1"
            real_result: PrivateNetworkItem = self.api_v2.private_network.update(network_id, description=description)

            self.assertEqual(mock.url, f"https://api.vultr.com/v2/private-networks/{network_id}")
            self.assertEqual(mock.method, SupportHttpMethod.PATCH.value)
            self.assertEqual(mock.req_json["description"], description)
            self.assertEqual(mock.status_code, 204)
            self.assertIsNone(real_result)

    def test_delete(self):
        """Test delete network."""
        with self._delete(status_code=204) as mock:
            network_id = str(uuid.uuid4())
            self.api_v2.private_network.delete(network_id=network_id)

            self.assertEqual(mock.url, f"https://api.vultr.com/v2/private-networks/{network_id}")
            self.assertEqual(mock.method, SupportHttpMethod.DELETE.value)
            self.assertEqual(mock.status_code, 204)
