import uuid

from pyvultr.base_api import SupportHttpMethod
from pyvultr.v2 import UserInfo
from tests.v2 import BaseTestV2


class TestUser(BaseTestV2):
    def test_list(self):
        """Test list users."""
        with self._get("response/users") as mock:
            _excepted_result = mock.python_body["users"][0]
            excepted_result = UserInfo.from_dict(_excepted_result)

            _real_result = self.api_v2.user.list(capacity=1)
            real_result: UserInfo = _real_result.first()

            self.assertEqual(mock.url, "https://api.vultr.com/v2/users")
            self.assertEqual(mock.method, SupportHttpMethod.GET.value)
            self.assertEqual(real_result, excepted_result)

    def test_create(self):
        """Test create user."""
        with self._post("response/user", expected_returned=UserInfo, status_code=201) as mock:
            excepted_result = mock.python_body

            name = "test_name"
            email = "test@example.com"
            password = "abcde"  # nosec: false B105(hardcoded_password_string) by bandit
            real_result: UserInfo = self.api_v2.user.create(name=name, email=email, password=password)

            self.assertEqual(mock.url, "https://api.vultr.com/v2/users")
            self.assertEqual(mock.method, SupportHttpMethod.POST.value)
            self.assertEqual(mock.req_json["name"], name)
            self.assertEqual(mock.req_json["email"], email)
            self.assertEqual(mock.req_json["password"], password)
            self.assertEqual(mock.status_code, 201)
            self.assertEqual(real_result, excepted_result)

    def test_get(self):
        """Test get user."""
        with self._get("response/user", expected_returned=UserInfo) as mock:
            excepted_result = mock.python_body

            user_id = str(uuid.uuid4())
            real_result: UserInfo = self.api_v2.user.get(user_id=user_id)

            self.assertEqual(mock.url, f"https://api.vultr.com/v2/users/{user_id}")
            self.assertEqual(mock.method, SupportHttpMethod.GET.value)
            self.assertEqual(real_result, excepted_result)

    def test_update(self):
        """Test update user."""
        with self._patch(status_code=204) as mock:
            user_id = str(uuid.uuid4())
            password = "abe123"  # nosec: false B105(hardcoded_password_string) by bandit
            real_result: UserInfo = self.api_v2.user.update(user_id, password=password)

            self.assertEqual(mock.url, f"https://api.vultr.com/v2/users/{user_id}")
            self.assertEqual(mock.method, SupportHttpMethod.PATCH.value)
            self.assertEqual(mock.req_json["password"], password)
            self.assertEqual(mock.status_code, 204)
            self.assertIsNone(real_result)

    def test_delete(self):
        """Test delete user."""
        with self._delete(status_code=204) as mock:
            user_id = str(uuid.uuid4())
            self.api_v2.user.delete(user_id=user_id)

            self.assertEqual(mock.url, f"https://api.vultr.com/v2/users/{user_id}")
            self.assertEqual(mock.method, SupportHttpMethod.DELETE.value)
            self.assertEqual(mock.status_code, 204)
