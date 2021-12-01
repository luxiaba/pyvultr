import uuid

from pyvultr.base_api import SupportHttpMethod
from pyvultr.v2 import BlockStorage
from tests.v2 import BaseTestV2


class TestBlockStorage(BaseTestV2):
    def test_list(self):
        """Test list block storages."""
        with self._get("response/blocks") as mock:
            _excepted_result = mock.python_body["blocks"][0]
            excepted_result = BlockStorage.from_dict(_excepted_result)

            _real_result = self.api_v2.block_storage.list()
            real_result: BlockStorage = _real_result.first()

            self.assertEqual(mock.url, "https://api.vultr.com/v2/blocks")
            self.assertEqual(mock.method, SupportHttpMethod.GET.value)
            self.assertEqual(real_result, excepted_result)

    def test_create(self):
        """Test list block storages."""
        with self._post("response/block", expected_returned=BlockStorage, status_code=202) as mock:
            excepted_result = mock.python_body

            region = "test_region"
            size_gb = 10
            real_result: BlockStorage = self.api_v2.block_storage.create(region=region, size_gb=size_gb)

            self.assertEqual(mock.url, "https://api.vultr.com/v2/blocks")
            self.assertEqual(mock.method, SupportHttpMethod.POST.value)
            self.assertEqual(mock.req_json["region"], region)
            self.assertEqual(mock.req_json["size_gb"], size_gb)
            self.assertEqual(real_result, excepted_result)
            self.assertEqual(mock.status_code, 202)

    def test_get(self):
        """Test get block storage."""
        with self._get("response/block", expected_returned=BlockStorage) as mock:
            excepted_result = mock.python_body

            block_storage_id = str(uuid.uuid4())
            real_result: BlockStorage = self.api_v2.block_storage.get(block_storage_id)

            self.assertEqual(mock.url, f"https://api.vultr.com/v2/blocks/{block_storage_id}")
            self.assertEqual(mock.method, SupportHttpMethod.GET.value)
            self.assertEqual(real_result, excepted_result)

    def test_update(self):
        """Test update block storage."""
        with self._patch(status_code=204) as mock:
            block_storage_id = str(uuid.uuid4())
            label = "test_label"
            size_gb = 10
            self.api_v2.block_storage.update(block_storage_id, size_gb=10, label=label)

            self.assertEqual(mock.url, f"https://api.vultr.com/v2/blocks/{block_storage_id}")
            self.assertEqual(mock.method, SupportHttpMethod.PATCH.value)
            self.assertEqual(mock.req_json["label"], label)
            self.assertEqual(mock.req_json["size_gb"], size_gb)
            self.assertEqual(mock.status_code, 204)

    def test_attach(self):
        """Test attach block storage."""
        with self._post(status_code=204) as mock:
            block_storage_id = str(uuid.uuid4())
            instance_id = str(uuid.uuid4())
            self.api_v2.block_storage.attach(block_storage_id, instance_id=instance_id, live=False)

            self.assertEqual(mock.url, f"https://api.vultr.com/v2/blocks/{block_storage_id}/attach")
            self.assertEqual(mock.method, SupportHttpMethod.POST.value)
            self.assertEqual(mock.req_json["instance_id"], instance_id)
            self.assertEqual(mock.req_json["live"], False)
            self.assertEqual(mock.status_code, 204)

    def test_detach(self):
        """Test detach block storage."""
        with self._post(status_code=204) as mock:
            block_storage_id = str(uuid.uuid4())
            self.api_v2.block_storage.detach(block_storage_id, live=True)

            self.assertEqual(mock.url, f"https://api.vultr.com/v2/blocks/{block_storage_id}/detach")
            self.assertEqual(mock.method, SupportHttpMethod.POST.value)
            self.assertEqual(mock.req_json["live"], True)
            self.assertEqual(mock.status_code, 204)

    def test_delete(self):
        """Test delete block storage."""
        with self._delete(status_code=204) as mock:
            block_storage_id = str(uuid.uuid4())
            self.api_v2.block_storage.delete(block_storage_id)

            self.assertEqual(mock.url, f"https://api.vultr.com/v2/blocks/{block_storage_id}")
            self.assertEqual(mock.method, SupportHttpMethod.DELETE.value)
            self.assertEqual(mock.status_code, 204)
