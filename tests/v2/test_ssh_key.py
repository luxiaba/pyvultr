import uuid

from pyvultr.base_api import SupportHttpMethod
from pyvultr.v2 import SSHKey
from tests.v2 import BaseTestV2


class TestSSHKey(BaseTestV2):
    def test_list(self):
        """Test list ssh-keys."""
        with self._get("response/ssh_keys") as mock:
            _excepted_result = mock.python_body["ssh_keys"][0]
            excepted_result = SSHKey.from_dict(_excepted_result)

            _real_result = self.api_v2.ssh_key.list(capacity=1)
            real_result: SSHKey = _real_result.first()

            self.assertEqual(mock.url, "https://api.vultr.com/v2/ssh-keys")
            self.assertEqual(mock.method, SupportHttpMethod.GET.value)
            self.assertEqual(real_result, excepted_result)

    def test_create(self):
        """Test create ssh-key."""
        with self._post("response/ssh_key", expected_returned=SSHKey, status_code=201) as mock:
            excepted_result = mock.python_body

            name = "test_name"
            ssh_key = "test_ssh_key"
            real_result: SSHKey = self.api_v2.ssh_key.create(name=name, ssh_key=ssh_key)

            self.assertEqual(mock.url, "https://api.vultr.com/v2/ssh-keys")
            self.assertEqual(mock.method, SupportHttpMethod.POST.value)
            self.assertEqual(mock.req_json["name"], name)
            self.assertEqual(mock.req_json["ssh_key"], ssh_key)
            self.assertEqual(mock.status_code, 201)
            self.assertEqual(real_result, excepted_result)

    def test_get(self):
        """Test get ssh-key."""
        with self._get("response/ssh_key", expected_returned=SSHKey) as mock:
            excepted_result = mock.python_body

            ssh_key_id = str(uuid.uuid4())
            real_result: SSHKey = self.api_v2.ssh_key.get(ssh_key_id=ssh_key_id)

            self.assertEqual(mock.url, f"https://api.vultr.com/v2/ssh-keys/{ssh_key_id}")
            self.assertEqual(mock.method, SupportHttpMethod.GET.value)
            self.assertEqual(real_result, excepted_result)

    def test_update(self):
        """Test update ssh-key."""
        with self._patch(status_code=204) as mock:
            ssh_key_id = str(uuid.uuid4())
            ssh_key = "test_ssh_key_2"
            real_result: SSHKey = self.api_v2.ssh_key.update(ssh_key_id, ssh_key=ssh_key)

            self.assertEqual(mock.url, f"https://api.vultr.com/v2/ssh-keys/{ssh_key_id}")
            self.assertEqual(mock.method, SupportHttpMethod.PATCH.value)
            self.assertEqual(mock.req_json["ssh_key"], ssh_key)
            self.assertEqual(mock.status_code, 204)
            self.assertIsNone(real_result)

    def test_delete(self):
        """Test delete ssh-key."""
        with self._delete(status_code=204) as mock:
            ssh_key_id = str(uuid.uuid4())
            self.api_v2.ssh_key.delete(ssh_key_id=ssh_key_id)

            self.assertEqual(mock.url, f"https://api.vultr.com/v2/ssh-keys/{ssh_key_id}")
            self.assertEqual(mock.method, SupportHttpMethod.DELETE.value)
            self.assertEqual(mock.status_code, 204)
