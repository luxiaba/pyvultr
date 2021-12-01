import uuid

from pyvultr.base_api import SupportHttpMethod
from pyvultr.v2 import ISOItem, PublicISOItem
from tests.v2 import BaseTestV2


class TestISO(BaseTestV2):
    def test_list(self):
        """Test list iso list."""
        with self._get("response/iso_list") as mock:
            _excepted_result = mock.python_body["isos"][0]
            excepted_result = ISOItem.from_dict(_excepted_result)

            _real_result = self.api_v2.iso.list(capacity=1)
            real_result: ISOItem = _real_result.first()

            self.assertEqual(mock.url, "https://api.vultr.com/v2/iso")
            self.assertEqual(mock.method, SupportHttpMethod.GET.value)
            self.assertEqual(real_result, excepted_result)

    def test_create(self):
        """Test create iso."""
        with self._post("response/iso", expected_returned=ISOItem, status_code=201) as mock:
            excepted_result = mock.python_body

            url = "test_url"
            real_result: ISOItem = self.api_v2.iso.create(url=url)

            self.assertEqual(mock.url, "https://api.vultr.com/v2/iso")
            self.assertEqual(mock.method, SupportHttpMethod.POST.value)
            self.assertEqual(mock.req_json["url"], url)
            self.assertEqual(mock.status_code, 201)
            self.assertEqual(real_result, excepted_result)

    def test_get(self):
        """Test get iso."""
        with self._get("response/iso", expected_returned=ISOItem) as mock:
            excepted_result = mock.python_body

            iso_id = str(uuid.uuid4())
            real_result: ISOItem = self.api_v2.iso.get(iso_id=iso_id)

            self.assertEqual(mock.url, f"https://api.vultr.com/v2/iso/{iso_id}")
            self.assertEqual(mock.method, SupportHttpMethod.GET.value)
            self.assertEqual(real_result, excepted_result)

    def test_delete(self):
        """Test delete iso."""
        with self._delete(status_code=204) as mock:
            iso_id = str(uuid.uuid4())
            self.api_v2.iso.delete(iso_id=iso_id)

            self.assertEqual(mock.url, f"https://api.vultr.com/v2/iso/{iso_id}")
            self.assertEqual(mock.method, SupportHttpMethod.DELETE.value)
            self.assertEqual(mock.status_code, 204)

    def test_list_public(self):
        """Test list public iso list."""
        with self._get("response/iso_public_list") as mock:
            _excepted_result = mock.python_body["public_isos"][0]
            excepted_result = PublicISOItem.from_dict(_excepted_result)

            _real_result = self.api_v2.iso.list_public(capacity=1)
            real_result: PublicISOItem = _real_result.first()

            self.assertEqual(mock.url, "https://api.vultr.com/v2/iso-public")
            self.assertEqual(mock.method, SupportHttpMethod.GET.value)
            self.assertEqual(real_result, excepted_result)
