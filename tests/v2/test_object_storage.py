import uuid

from pyvultr.base_api import SupportHttpMethod
from pyvultr.v2 import ObjectStorageClusterItem, ObjectStorageItem, ObjectStorageS3Credential
from tests.v2 import BaseTestV2


class TestObjectStorage(BaseTestV2):
    def test_list(self):
        """Test list object storages."""
        with self._get("response/object_storages") as mock:
            _excepted_result = mock.python_body["object_storages"][0]
            excepted_result = ObjectStorageItem.from_dict(_excepted_result)

            _real_result = self.api_v2.object_storage.list()
            real_result: ObjectStorageItem = _real_result.first()

            self.assertEqual(mock.url, "https://api.vultr.com/v2/object-storage")
            self.assertEqual(mock.method, SupportHttpMethod.GET.value)
            self.assertEqual(real_result, excepted_result)

    def test_create(self):
        """Test list object storages."""
        with self._post("response/object_storage", expected_returned=ObjectStorageItem, status_code=202) as mock:
            excepted_result = mock.python_body

            cluster_id = str(uuid.uuid4())
            label = "test_label"
            real_result: ObjectStorageItem = self.api_v2.object_storage.create(cluster_id=cluster_id, label=label)

            self.assertEqual(mock.url, "https://api.vultr.com/v2/object-storage")
            self.assertEqual(mock.method, SupportHttpMethod.POST.value)
            self.assertEqual(mock.req_json["cluster_id"], cluster_id)
            self.assertEqual(mock.req_json["label"], label)
            self.assertEqual(real_result, excepted_result)
            self.assertEqual(mock.status_code, 202)

    def test_get(self):
        """Test get object storage."""
        with self._get("response/object_storage", expected_returned=ObjectStorageItem) as mock:
            excepted_result = mock.python_body

            object_storage_id = str(uuid.uuid4())
            real_result: ObjectStorageItem = self.api_v2.object_storage.get(object_storage_id)

            self.assertEqual(mock.url, f"https://api.vultr.com/v2/object-storage/{object_storage_id}")
            self.assertEqual(mock.method, SupportHttpMethod.GET.value)
            self.assertEqual(real_result, excepted_result)

    def test_update(self):
        """Test update object storage."""
        with self._patch(status_code=204) as mock:
            object_storage_id = str(uuid.uuid4())
            label = "test_label_2"
            self.api_v2.object_storage.update(object_storage_id, label=label)

            self.assertEqual(mock.url, f"https://api.vultr.com/v2/object-storage/{object_storage_id}")
            self.assertEqual(mock.method, SupportHttpMethod.PATCH.value)
            self.assertEqual(mock.req_json["label"], label)
            self.assertEqual(mock.status_code, 204)

    def test_regenerate_keys(self):
        """Test regenerate keys."""
        r = ObjectStorageS3Credential
        with self._post("response/object_storage_regenerate_keys", expected_returned=r, status_code=201) as mock:
            excepted_result = mock.python_body

            object_storage_id = str(uuid.uuid4())
            real_result: ObjectStorageS3Credential = self.api_v2.object_storage.regenerate_keys(object_storage_id)

            self.assertEqual(mock.url, f"https://api.vultr.com/v2/object-storage/{object_storage_id}/regenerate-keys")
            self.assertEqual(mock.method, SupportHttpMethod.POST.value)
            self.assertEqual(real_result, excepted_result)
            self.assertEqual(mock.status_code, 201)

    def list_clusters(self):
        """Test list clusters."""
        with self._get("response/object_storages_clusters") as mock:
            _excepted_result = mock.python_body["clusters"][0]
            excepted_result = ObjectStorageItem.from_dict(_excepted_result)

            _real_result = self.api_v2.object_storage.list_clusters()
            real_result: ObjectStorageClusterItem = _real_result.first()

            self.assertEqual(mock.url, "https://api.vultr.com/v2/object-storage/clusters")
            self.assertEqual(mock.method, SupportHttpMethod.GET.value)
            self.assertEqual(real_result, excepted_result)

    def test_delete(self):
        """Test delete object storage."""
        with self._delete(status_code=204) as mock:
            object_storage_id = str(uuid.uuid4())
            self.api_v2.object_storage.delete(object_storage_id)

            self.assertEqual(mock.url, f"https://api.vultr.com/v2/object-storage/{object_storage_id}")
            self.assertEqual(mock.method, SupportHttpMethod.DELETE.value)
            self.assertEqual(mock.status_code, 204)
