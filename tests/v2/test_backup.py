from pyvultr.base_api import SupportHttpMethod
from pyvultr.v2 import BackupItem
from tests.v2 import BaseTestV2


class TestBackup(BaseTestV2):
    def test_list(self):
        """Test list backups."""
        with self._get("response/backup_list") as mock:
            _excepted_result = mock.python_body["backups"][0]
            excepted_result = BackupItem.from_dict(_excepted_result)

            _real_result = self.api_v2.backup.list(capacity=1)
            real_result: BackupItem = _real_result.first()

            self.assertEqual(mock.url, "https://api.vultr.com/v2/backups")
            self.assertEqual(mock.method, SupportHttpMethod.GET.value)
            self.assertEqual(real_result, excepted_result)

    def test_get(self):
        """Test get backup."""
        with self._get("response/backup", expected_returned=BackupItem) as mock:
            excepted_result: BackupItem = mock.python_body

            real_result: BackupItem = self.api_v2.backup.get("test_back_ip_1987573")

            self.assertEqual(mock.url, "https://api.vultr.com/v2/backups/test_back_ip_1987573")
            self.assertEqual(mock.method, SupportHttpMethod.GET.value)
            self.assertEqual(real_result, excepted_result)
