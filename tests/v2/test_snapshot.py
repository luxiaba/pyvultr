import uuid

from pyvultr.base_api import SupportHttpMethod
from pyvultr.v2 import Snapshot
from tests.v2 import BaseTestV2


class TestSnapshot(BaseTestV2):
    def test_list(self):
        """Test list snapshots."""
        with self._get("response/snapshots") as mock:
            _excepted_result = mock.python_body["snapshots"][0]
            excepted_result = Snapshot.from_dict(_excepted_result)

            _real_result = self.api_v2.snapshot.list(capacity=1)
            real_result: Snapshot = _real_result.first()

            self.assertEqual(mock.url, "https://api.vultr.com/v2/snapshots")
            self.assertEqual(mock.method, SupportHttpMethod.GET.value)
            self.assertEqual(real_result, excepted_result)

    def test_create(self):
        """Test create snapshot."""
        with self._post("response/snapshot", expected_returned=Snapshot, status_code=201) as mock:
            excepted_result = mock.python_body

            instance_id = str(uuid.uuid4())
            description = "test_description"
            real_result: Snapshot = self.api_v2.snapshot.create(instance_id=instance_id, description=description)

            self.assertEqual(mock.url, "https://api.vultr.com/v2/snapshots")
            self.assertEqual(mock.method, SupportHttpMethod.POST.value)
            self.assertEqual(mock.req_json["description"], description)
            self.assertEqual(mock.status_code, 201)
            self.assertEqual(real_result, excepted_result)

    def test_get(self):
        """Test get snapshot."""
        with self._get("response/snapshot", expected_returned=Snapshot) as mock:
            excepted_result = mock.python_body

            snapshot_id = str(uuid.uuid4())
            real_result: Snapshot = self.api_v2.snapshot.get(snapshot_id=snapshot_id)

            self.assertEqual(mock.url, f"https://api.vultr.com/v2/snapshots/{snapshot_id}")
            self.assertEqual(mock.method, SupportHttpMethod.GET.value)
            self.assertEqual(real_result, excepted_result)

    def test_update(self):
        """Test update snapshot."""
        with self._put(status_code=204) as mock:
            snapshot_id = str(uuid.uuid4())
            description = "test_description_1"
            real_result: Snapshot = self.api_v2.snapshot.update(snapshot_id, description=description)

            self.assertEqual(mock.url, f"https://api.vultr.com/v2/snapshots/{snapshot_id}")
            self.assertEqual(mock.method, SupportHttpMethod.PUT.value)
            self.assertEqual(mock.req_json["description"], description)
            self.assertEqual(mock.status_code, 204)
            self.assertIsNone(real_result)

    def test_delete(self):
        """Test delete snapshot."""
        with self._delete(status_code=204) as mock:
            snapshot_id = str(uuid.uuid4())
            self.api_v2.snapshot.delete(snapshot_id=snapshot_id)

            self.assertEqual(mock.url, f"https://api.vultr.com/v2/snapshots/{snapshot_id}")
            self.assertEqual(mock.method, SupportHttpMethod.DELETE.value)
            self.assertEqual(mock.status_code, 204)
