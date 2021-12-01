import pytest

from pyvultr.exception import APIException
from pyvultr.v2 import AccountInfo
from tests.v2 import BaseTestV2


class TestAccount(BaseTestV2):
    def test_http(self):
        """Test api error."""
        with self._get(status_code=400) as mock:
            with pytest.raises(APIException) as err:
                self.api_v2.account.get()
            self.assertIn("APIException code=400", str(err.value))
            self.assertEqual(mock.status_code, 400)

    def test_get(self):
        """Test get account."""
        with self._get("response/account", expected_returned=AccountInfo) as mock:
            excepted_result: AccountInfo = mock.python_body

            real_result: AccountInfo = self.api_v2.account.get()

            self.assertEqual(real_result, excepted_result)
